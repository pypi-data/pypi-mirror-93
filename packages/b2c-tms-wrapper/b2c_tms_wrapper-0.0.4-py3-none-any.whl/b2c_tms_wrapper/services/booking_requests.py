from datetime import datetime
from http import HTTPStatus
from typing import Dict, List, Optional

from shuttl_geo import Location
from shuttlis.serialization import serialize
from shuttlis.utils import group_by

from b2c_tms_wrapper.error import (
    BookingNotFound,
    BookingNotFoundOnTrip,
    TripNotFound,
    InvalidOperation,
    BookingAlreadyExists,
    NoSeatsAvailable,
    CancellationNotAllowedForMissedBooking,
    CancellationNotAllowedForBoardedBooking,
    ResourceNotFound,
    ReservationAlreadyConsumed,
)
from b2c_tms_wrapper.utils import mk_exc, auto_paginate
from b2c_tms_wrapper.models import BookingRequest, BoardingMode, BookingState
from b2c_tms_wrapper.timeout import SessionWithTimeOut


class BookingRequestsService:
    def __init__(self, url: str, session: SessionWithTimeOut):
        self._url = url
        self._session = session

    def create_booking(
        self,
        user_id: str,
        trip_id: str,
        pickup_stop_id: str,
        drop_stop_id: str,
        booking_request_id: str,
    ) -> BookingRequest:
        json = {
            "user_id": user_id,
            "trip_id": trip_id,
            "pickup_stop_id": pickup_stop_id,
            "drop_stop_id": drop_stop_id,
            "booking_request_id": booking_request_id,
        }
        response = self._session.post(
            url=f"{self._url}/api/v1/booking_requests",
            json=json,
        )

        if response.status_code == HTTPStatus.CONFLICT:
            raise NoSeatsAvailable(response.json()["error"]["message"])

        if response.status_code == HTTPStatus.BAD_REQUEST:
            if response.json()["error"]["type"] == "BOOKING_ALREADY_EXISTS":
                raise BookingAlreadyExists(response.json()["error"]["message"])
            raise InvalidOperation(f"Could not perform operation: {response.json()}")

        if response.status_code != HTTPStatus.CREATED:
            raise mk_exc(response)

        return BookingRequest.from_dict(response.json()["data"])

    def create_booking_through_reservation(
        self, reservation_id: str, user_id: str
    ) -> BookingRequest:
        json = {"reservation_id": reservation_id, "user_id": user_id}
        response = self._session.post(
            url=f"{self._url}/api/v1/booking_requests/for_reservation",
            json=json,
        )

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise ResourceNotFound(response.json()["error"]["message"])

        if response.status_code == HTTPStatus.CONFLICT:
            raise NoSeatsAvailable(response.json()["error"]["message"])

        if response.status_code == HTTPStatus.BAD_REQUEST:
            if response.json()["error"]["type"] == "RESERVATION_ALREADY_CONSUMED":
                raise ReservationAlreadyConsumed(response.json()["error"]["message"])
            raise InvalidOperation(f"Could not perform operation: {response.json()}")

        if response.status_code != HTTPStatus.CREATED:
            raise mk_exc(response)

        return BookingRequest.from_dict(response.json()["data"])

    def get_booking_request_by_mode(
        self, mode: BoardingMode
    ) -> Optional[BookingRequest]:
        response = self._session.get(
            f"{self._url}/api/v1/booking_requests/by_mode",
            params={"mode_id": mode.id, "mode_type": mode.type},
        )

        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return BookingRequest.from_dict(response.json()["data"])

    def get_booking_requests_by_ids(self, ids: List[str]) -> List[BookingRequest]:
        if not ids:
            return []

        response = self._session.get(
            url=f"{self._url}/api/v1/booking_requests/by_ids",
            params={"ids": ",".join(ids)},
        )

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return [BookingRequest.from_dict(br) for br in response.json()["data"]]

    def get_booking_requests_for_trip(self, trip_id: str) -> List[BookingRequest]:
        response = self._session.get(
            url=f"{self._url}/api/v1/booking_requests/by_trip/{trip_id}"
        )

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return [BookingRequest.from_dict(br) for br in response.json()["data"]]

    def get_booking_requests_for_trips(
        self, trips_ids: List[str], states: List[BookingState] = None
    ) -> Dict[str, List[BookingRequest]]:
        if not trips_ids:
            return {}

        json = {"trip_ids": trips_ids}
        if states:
            json["states"] = ",".join([state.value for state in states])
        response = self._session.get(
            url=f"{self._url}/api/v1/booking_requests/by_trips",
            json=json,
        )

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        booking_requests = [
            BookingRequest.from_dict(br) for br in response.json()["data"]
        ]
        return group_by(booking_requests, lambda br: br.trip_id)

    def get_booking_requests_for_user(
        self,
        user_id: str,
        from_time: datetime = None,
        to_time: datetime = None,
        states: List[BookingState] = None,
    ) -> List[BookingRequest]:
        params = {"user_id": user_id}
        if from_time:
            params["created_after"] = from_time
        if to_time:
            params["to_time"] = to_time
        if states:
            params["states"] = ",".join([state.value for state in states])

        booking_requests = auto_paginate(
            session=self._session,
            url=f"{self._url}/api/v1/booking_requests",
            params=serialize(params),
        )

        return [BookingRequest.from_dict(br) for br in booking_requests]

    def get_cancelled_booking_requests(self, after: str = None) -> List[BookingRequest]:
        booking_requests = auto_paginate(
            session=self._session,
            url=f"{self._url}/api/v2/booking_requests/by_cancellations",
            after=after,
        )

        return [BookingRequest.from_dict(br) for br in booking_requests]

    def get_cancelled_booking_requests_by_reasons(
        self,
        cancellation_reasons: List[str],
        after: str = None,
        from_time: str = None,
    ) -> List[BookingRequest]:
        if not cancellation_reasons:
            return []

        params = {"cancellation_reasons": ",".join(cancellation_reasons)}

        if from_time:
            params["from_time"] = from_time

        booking_requests = auto_paginate(
            session=self._session,
            url=f"{self._url}/api/v1/booking_requests/cancellations_by_reasons",
            params=serialize(params),
            after=after,
        )

        return [BookingRequest.from_dict(br) for br in booking_requests]

    def reschedule_booking(self, booking_id: str, trip_id: str) -> BookingRequest:
        response = self._session.patch(
            f"{self._url}/api/v1/booking_requests/{booking_id}/reschedule",
            json={"trip_id": trip_id},
        )

        if response.status_code == HTTPStatus.CONFLICT:
            raise NoSeatsAvailable(response.text)

        if response.status_code == HTTPStatus.BAD_REQUEST:
            if response.json()["error"]["type"] == "BOOKING_ALREADY_EXISTS":
                raise BookingAlreadyExists(response.text)
            raise InvalidOperation(f"Could not perform operation: {response.json()}")

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return BookingRequest.from_dict(response.json()["data"])

    def cancel_booking_by_mode(self, mode: BoardingMode) -> BookingRequest:
        params = {"mode_type": mode.type, "mode_id": mode.id}
        response = self._session.delete(
            f"{self._url}/api/v1/booking_requests/cancel/by_mode", params=params
        )

        if response.status_code == HTTPStatus.BAD_REQUEST:
            error_type = response.json()["error"]["type"]
            error_message = response.json()["error"]["message"]
            if error_type == "CANNOT_CANCEL_AFTER_MISSED_BOOKING":
                raise CancellationNotAllowedForMissedBooking(error_message)
            if error_type == "CANNOT_CANCEL_AFTER_BOARDED_BOOKING":
                raise CancellationNotAllowedForBoardedBooking(error_message)
            raise InvalidOperation(f"Could not perform operation: {response.json()}")

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return BookingRequest.from_dict(response.json()["data"])

    def board(
        self, trip_id: str, time: datetime, location: Location, mode: BoardingMode
    ) -> BookingRequest:
        params = {"trip_id": trip_id, "time": time, "location": location, "mode": mode}
        response = self._session.post(
            f"{self._url}/api/v1/booking_requests/board", json=serialize(params)
        )

        if response.status_code == HTTPStatus.BAD_REQUEST:
            error_type = response.json()["error"]["type"]
            error_message = response.json()["error"]["message"]
            if error_type == "BOOKING_NOT_FOUND":
                raise BookingNotFound(error_message)
            if error_type == "BOOKING_NOT_FOUND_ON_TRIP":
                raise BookingNotFoundOnTrip(error_message)
            if error_type == "TRIP_NOT_FOUND":
                raise TripNotFound(error_message)
            raise InvalidOperation(f"Could not perform operation: {response.json()}")

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return BookingRequest.from_dict(response.json()["data"])

    def deboard(
        self, trip_id: str, time: datetime, location: Location, mode: BoardingMode
    ) -> BookingRequest:
        json = {
            "trip_id": trip_id,
            "time": time,
            "location": {"lat": location.lat, "lng": location.lng},
            "mode": {
                "id": mode.id,
                "type": mode.type,
            },
        }
        response = self._session.post(
            f"{self._url}/api/v1/booking_requests/deboard", json=serialize(json)
        )

        if response.status_code == HTTPStatus.BAD_REQUEST:
            error_type = response.json()["error"]["type"]
            error_message = response.json()["error"]["message"]
            if error_type == "BOOKING_NOT_FOUND":
                raise BookingNotFound(error_message)
            if error_type == "BOOKING_NOT_FOUND_ON_TRIP":
                raise BookingNotFoundOnTrip(error_message)
            if error_type == "TRIP_NOT_FOUND":
                raise TripNotFound(error_message)
            raise InvalidOperation(f"Could not perform operation: {response.json()}")

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return BookingRequest.from_dict(response.json()["data"])
