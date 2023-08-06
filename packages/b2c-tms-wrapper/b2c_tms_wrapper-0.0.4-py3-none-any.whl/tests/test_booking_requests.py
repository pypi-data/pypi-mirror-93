import json
from datetime import timedelta
from http import HTTPStatus
from typing import Tuple

import pytest
import responses
from requests import PreparedRequest
from shuttl_time.time import time_now
from shuttlis.serialization import serialize
from shuttlis.utils import uuid4_str

from b2c_tms_wrapper.error import (
    BookingNotFound,
    BookingNotFoundOnTrip,
    TripNotFound,
    InvalidOperation,
    BookingAlreadyExists,
    NoSeatsAvailable,
    CancellationNotAllowedForMissedBooking,
    CancellationNotAllowedForBoardedBooking,
    ReservationAlreadyConsumed,
    ResourceNotFound,
)
from b2c_tms_wrapper.models import BoardingMode, BookingRequest, BookingState
from b2c_tms_wrapper.services.b2c_tms import B2CTMS
from tests.factories import (
    random_location,
    booking_request_api_response,
    trip_dm,
    boarding_mode_dm,
)

fake_b2c_tms_url = "http://b2c_tms"
b2c_tms_service = B2CTMS(b2c_tms_url=fake_b2c_tms_url)


@responses.activate
def test_create_booking_is_successful():
    booking_request_json = booking_request_api_response()
    booking_request = BookingRequest.from_dict(booking_request_json)

    responses.add(
        responses.POST,
        url=f"{fake_b2c_tms_url}/api/v1/booking_requests",
        status=HTTPStatus.CREATED,
        json={"data": booking_request_json},
    )

    result = b2c_tms_service.create_booking(
        user_id=uuid4_str(),
        trip_id=booking_request.trip_id,
        pickup_stop_id=uuid4_str(),
        drop_stop_id=uuid4_str(),
        booking_request_id=uuid4_str(),
    )
    assert result == booking_request


@responses.activate
def test_create_booking_raises_runtime_error_when_booking_already_exists():
    responses.add(
        responses.POST,
        url=f"{fake_b2c_tms_url}/api/v1/booking_requests",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "BOOKING_ALREADY_EXISTS",
                "message": "Booking already exists",
            }
        },
    )

    with pytest.raises(BookingAlreadyExists):
        b2c_tms_service.create_booking(
            user_id=uuid4_str(),
            trip_id=uuid4_str(),
            pickup_stop_id=uuid4_str(),
            drop_stop_id=uuid4_str(),
            booking_request_id=uuid4_str(),
        )


@responses.activate
def test_create_booking_raises_runtime_error_when_invalid_operation():
    responses.add(
        responses.POST,
        url=f"{fake_b2c_tms_url}/api/v1/booking_requests",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "CLIENT_ERROR",
                "message": "Invalid Operation",
            }
        },
    )

    with pytest.raises(InvalidOperation):
        b2c_tms_service.create_booking(
            user_id=uuid4_str(),
            trip_id=uuid4_str(),
            pickup_stop_id=uuid4_str(),
            drop_stop_id=uuid4_str(),
            booking_request_id=uuid4_str(),
        )


@responses.activate
def test_create_booking_raises_runtime_error_when_no_seats_available():
    responses.add(
        responses.POST,
        url=f"{fake_b2c_tms_url}/api/v1/booking_requests",
        status=HTTPStatus.CONFLICT,
        json={
            "error": {
                "type": "NO_SEATS_AVAILABLE",
                "message": "No seats available",
            }
        },
    )

    with pytest.raises(NoSeatsAvailable):
        b2c_tms_service.create_booking(
            user_id=uuid4_str(),
            trip_id=uuid4_str(),
            pickup_stop_id=uuid4_str(),
            drop_stop_id=uuid4_str(),
            booking_request_id=uuid4_str(),
        )


@responses.activate
def test_create_booking_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.POST,
        url=f"{fake_b2c_tms_url}/api/v1/booking_requests",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.create_booking(
            user_id=uuid4_str(),
            trip_id=uuid4_str(),
            pickup_stop_id=uuid4_str(),
            drop_stop_id=uuid4_str(),
            booking_request_id=uuid4_str(),
        )


@responses.activate
def test_create_booking_through_reservation_is_successful():
    booking_request_json = booking_request_api_response()
    booking_request = BookingRequest.from_dict(booking_request_json)

    responses.add(
        responses.POST,
        url=f"{fake_b2c_tms_url}/api/v1/booking_requests/for_reservation",
        status=HTTPStatus.CREATED,
        json={"data": booking_request_json},
    )

    result = b2c_tms_service.create_booking_through_reservation(
        reservation_id=uuid4_str(), user_id=uuid4_str()
    )
    assert result == booking_request


@responses.activate
def test_create_booking_through_reservation_raises_error_when_resource_not_found():
    responses.add(
        responses.POST,
        url=f"{fake_b2c_tms_url}/api/v1/booking_requests/for_reservation",
        status=HTTPStatus.NOT_FOUND,
        json={
            "error": {
                "type": "NOT_FOUND",
                "message": "Not found",
            }
        },
    )

    with pytest.raises(ResourceNotFound):
        b2c_tms_service.create_booking_through_reservation(
            reservation_id=uuid4_str(), user_id=uuid4_str()
        )


@responses.activate
def test_create_booking_through_reservation_raises_error_when_no_seats_available():
    responses.add(
        responses.POST,
        url=f"{fake_b2c_tms_url}/api/v1/booking_requests/for_reservation",
        status=HTTPStatus.CONFLICT,
        json={
            "error": {
                "type": "NO_SEATS_AVAILABLE",
                "message": "No seats available",
            }
        },
    )

    with pytest.raises(NoSeatsAvailable):
        b2c_tms_service.create_booking_through_reservation(
            reservation_id=uuid4_str(), user_id=uuid4_str()
        )


@responses.activate
def test_create_booking_through_reservation_raises_error_when_reservation_already_consumed():
    responses.add(
        responses.POST,
        url=f"{fake_b2c_tms_url}/api/v1/booking_requests/for_reservation",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "RESERVATION_ALREADY_CONSUMED",
                "message": "Reservation already consumed",
            }
        },
    )

    with pytest.raises(ReservationAlreadyConsumed):
        b2c_tms_service.create_booking_through_reservation(
            reservation_id=uuid4_str(), user_id=uuid4_str()
        )


@responses.activate
def test_create_booking_through_reservation_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.POST,
        url=f"{fake_b2c_tms_url}/api/v1/booking_requests/for_reservation",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.create_booking_through_reservation(
            reservation_id=uuid4_str(), user_id=uuid4_str()
        )


@responses.activate
def test_get_booking_request_by_mode_is_successful():
    booking_request_json = booking_request_api_response()
    booking_request = BookingRequest.from_dict(booking_request_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/by_mode",
        status=HTTPStatus.OK,
        json={"data": booking_request_json},
    )

    result = b2c_tms_service.get_booking_request_by_mode(boarding_mode_dm())
    assert result == booking_request


@responses.activate
def test_get_booking_request_by_mode_returns_none_when_not_found():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/by_mode",
        status=HTTPStatus.NOT_FOUND,
    )

    booking_request = b2c_tms_service.get_booking_request_by_mode(boarding_mode_dm())
    assert booking_request is None


@responses.activate
def test_get_booking_request_by_mode_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/by_mode",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_booking_request_by_mode(boarding_mode_dm())


@responses.activate
def test_get_booking_requests_by_ids_is_successful():
    booking_request_json = booking_request_api_response()
    booking_request = BookingRequest.from_dict(booking_request_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/by_ids",
        status=HTTPStatus.OK,
        json={"data": [booking_request_json]},
    )

    result = b2c_tms_service.get_booking_requests_by_ids(ids=[booking_request.id])
    assert result == [booking_request]


def test_get_booking_requests_by_ids_when_no_ids_given():
    result = b2c_tms_service.get_booking_requests_by_ids(ids=[])
    assert result == []


@responses.activate
def test_get_booking_requests_by_ids_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/by_ids",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_booking_requests_by_ids(ids=[uuid4_str()])


@responses.activate
def get_booking_requests_for_trip_is_successful():
    trip_id = uuid4_str()
    booking_request_json = booking_request_api_response()
    booking_request = BookingRequest.from_dict(booking_request_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/by_trip/{trip_id}",
        status=HTTPStatus.OK,
        json={"data": [booking_request_json]},
    )

    result = b2c_tms_service.get_booking_requests_for_trip(trip_id)
    assert result == [booking_request]


@responses.activate
def test_get_booking_requests_by_trip_id_raises_runtime_error_when_status_is_internal_error():
    trip_id = uuid4_str()
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/by_trip/{trip_id}",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_booking_requests_for_trip(trip_id)


@responses.activate
def test_get_booking_requests_for_trips_is_successful():
    trip = trip_dm()
    booking_request_json = booking_request_api_response(trip_id=trip.id)
    booking_request = BookingRequest.from_dict(booking_request_json)

    def request_callback(request: PreparedRequest) -> Tuple:
        payload = json.loads(request.body)
        assert payload == {"trip_ids": [trip.id]}
        return (
            HTTPStatus.OK,
            {},
            json.dumps({"data": [booking_request_json]}),
        )

    responses.add_callback(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/by_trips",
        callback=request_callback,
        content_type="application/json",
    )

    result = b2c_tms_service.get_booking_requests_for_trips(trips_ids=[trip.id])
    assert result == {trip.id: [booking_request]}


def test_get_booking_requests_for_trips_when_no_trip_ids_given():
    result = b2c_tms_service.get_booking_requests_for_trips(trips_ids=[])
    assert result == {}


@responses.activate
def test_get_booking_requests_for_trips_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/by_trips",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_booking_requests_for_trips(trips_ids=[uuid4_str()])


@responses.activate
def test_get_booking_requests_for_user_is_successful():
    booking_request_json = booking_request_api_response()
    booking_request = BookingRequest.from_dict(booking_request_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_requests",
        status=HTTPStatus.OK,
        json={"data": [booking_request_json], "meta": {"cursor": {"last": None}}},
    )

    booking_requests = b2c_tms_service.get_booking_requests_for_user(
        user_id=uuid4_str(),
        from_time=time_now() - timedelta(hours=6),
        to_time=time_now(),
        states=[BookingState.CONFIRMED],
    )
    assert booking_requests == [booking_request]


@responses.activate
def test_get_booking_requests_for_user_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_requests",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_booking_requests_for_user(user_id=uuid4_str())


@responses.activate
def test_get_cancelled_booking_requests_is_successful():
    booking_request_json = booking_request_api_response()
    booking_request = BookingRequest.from_dict(booking_request_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v2/booking_requests/by_cancellations",
        status=HTTPStatus.OK,
        json={"data": [booking_request_json], "meta": {"cursor": {"last": None}}},
    )

    booking_requests = b2c_tms_service.get_cancelled_booking_requests()
    assert booking_requests == [booking_request]


@responses.activate
def test_get_cancelled_booking_requests_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v2/booking_requests/by_cancellations",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_cancelled_booking_requests()


@responses.activate
def test_get_cancelled_booking_requests_by_reasons_is_successful():
    booking_request_json = booking_request_api_response()
    booking_request = BookingRequest.from_dict(booking_request_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/cancellations_by_reasons",
        status=HTTPStatus.OK,
        json={"data": [booking_request_json], "meta": {"cursor": {"last": None}}},
    )

    booking_requests = b2c_tms_service.get_cancelled_booking_requests_by_reasons(
        cancellation_reasons=["PASSENGER_CANCELLED", "SYSTEM_CANCELLED"]
    )
    assert booking_requests == [booking_request]


@responses.activate
def test_get_cancelled_booking_requests_by_reasons_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/cancellations_by_reasons",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_cancelled_booking_requests_by_reasons(
            cancellation_reasons=["PASSENGER_CANCELLED", "SYSTEM_CANCELLED"]
        )


@responses.activate
def test_reschedule_booking_is_successful():
    booking_request_json = booking_request_api_response()
    booking_request = BookingRequest.from_dict(booking_request_json)

    responses.add(
        responses.PATCH,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/{booking_request.id}/reschedule",
        status=HTTPStatus.OK,
        json={"data": booking_request_json},
    )

    result = b2c_tms_service.reschedule_booking(
        booking_id=booking_request.id, trip_id=uuid4_str()
    )
    assert result == booking_request


@responses.activate
def test_reschedule_booking_raises_error_when_no_seats_available():
    booking_id = uuid4_str()
    responses.add(
        responses.PATCH,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/{booking_id}/reschedule",
        status=HTTPStatus.CONFLICT,
        json={
            "error": {
                "type": "NO_SEATS_AVAILABLE",
                "message": "No Seats Available",
            }
        },
    )

    with pytest.raises(NoSeatsAvailable):
        b2c_tms_service.reschedule_booking(booking_id=booking_id, trip_id=uuid4_str())


@responses.activate
def test_reschedule_booking_raises_error_when_booking_already_exists():
    booking_id = uuid4_str()
    responses.add(
        responses.PATCH,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/{booking_id}/reschedule",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "BOOKING_ALREADY_EXISTS",
                "message": "Booking Already Exists",
            }
        },
    )

    with pytest.raises(BookingAlreadyExists):
        b2c_tms_service.reschedule_booking(booking_id=booking_id, trip_id=uuid4_str())


@responses.activate
def test_reschedule_booking_raises_runtime_error_when_status_is_internal_error():
    booking_id = uuid4_str()
    responses.add(
        responses.PATCH,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/{booking_id}/reschedule",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.reschedule_booking(booking_id=booking_id, trip_id=uuid4_str())


@responses.activate
def test_cancel_booking_by_mode_is_successful():
    booking_request_json = booking_request_api_response()
    booking_request = BookingRequest.from_dict(booking_request_json)

    responses.add(
        responses.DELETE,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/cancel/by_mode",
        status=HTTPStatus.OK,
        json={"data": booking_request_json},
    )

    result = b2c_tms_service.cancel_booking_by_mode(mode=boarding_mode_dm())
    assert result == booking_request


@responses.activate
def test_cancel_booking_by_mode_raises_error_when_missed_booking():
    responses.add(
        responses.DELETE,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/cancel/by_mode",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "CANNOT_CANCEL_AFTER_MISSED_BOOKING",
                "message": "Cannot cancel after missed booking",
            }
        },
    )

    with pytest.raises(CancellationNotAllowedForMissedBooking):
        b2c_tms_service.cancel_booking_by_mode(mode=boarding_mode_dm())


@responses.activate
def test_cancel_booking_by_mode_raises_error_when_boarded_booking():
    responses.add(
        responses.DELETE,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/cancel/by_mode",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "CANNOT_CANCEL_AFTER_BOARDED_BOOKING",
                "message": "Cannot cancel after boarded booking",
            }
        },
    )

    with pytest.raises(CancellationNotAllowedForBoardedBooking):
        b2c_tms_service.cancel_booking_by_mode(mode=boarding_mode_dm())


@responses.activate
def test_cancel_booking_by_mode_raises_error_when_invalid_operation():
    responses.add(
        responses.DELETE,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/cancel/by_mode",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "CLIENT_ERROR",
                "message": "Invalid Operation",
            }
        },
    )

    with pytest.raises(InvalidOperation):
        b2c_tms_service.cancel_booking_by_mode(mode=boarding_mode_dm())


@responses.activate
def test_cancel_booking_by_mode_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.DELETE,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/cancel/by_mode",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.cancel_booking_by_mode(mode=boarding_mode_dm())


@responses.activate
def test_board_is_successful():
    time = time_now()
    location = random_location()
    mode = BoardingMode(type="MANUAL", id=uuid4_str())
    booking_request_json = booking_request_api_response()
    trip = trip_dm()
    booking_request = BookingRequest.from_dict(booking_request_json)

    def request_callback(request: PreparedRequest) -> Tuple:
        payload = json.loads(request.body)
        assert payload == serialize(
            dict(
                trip_id=trip.id,
                time=time,
                location=location,
                mode=mode,
            )
        )
        return (
            HTTPStatus.OK,
            {},
            json.dumps({"data": booking_request_json}),
        )

    responses.add_callback(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/board",
        callback=request_callback,
        content_type="application/json",
    )

    result = b2c_tms_service.board(
        trip_id=trip.id,
        time=time,
        location=location,
        mode=mode,
    )
    assert result == booking_request


@responses.activate
def test_board_raises_error_when_booking_not_found():
    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/board",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "BOOKING_NOT_FOUND",
                "message": "Booking not found",
            }
        },
    )

    with pytest.raises(BookingNotFound):
        b2c_tms_service.board(
            trip_id=uuid4_str(),
            time=time_now(),
            location=random_location(),
            mode=boarding_mode_dm(),
        )


@responses.activate
def test_board_raises_error_when_booking_not_found_on_trip():
    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/board",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "BOOKING_NOT_FOUND_ON_TRIP",
                "message": "Booking not found on trip",
            }
        },
    )

    with pytest.raises(BookingNotFoundOnTrip):
        b2c_tms_service.board(
            trip_id=uuid4_str(),
            time=time_now(),
            location=random_location(),
            mode=boarding_mode_dm(),
        )


@responses.activate
def test_board_raises_error_when_trip_not_found():
    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/board",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "TRIP_NOT_FOUND",
                "message": "Trip not found",
            }
        },
    )

    with pytest.raises(TripNotFound):
        b2c_tms_service.board(
            trip_id=uuid4_str(),
            time=time_now(),
            location=random_location(),
            mode=boarding_mode_dm(),
        )


@responses.activate
def test_board_raises_error_when_invalid_operation():
    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/board",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "CLIENT_ERROR",
                "message": "Invalid Operation",
            }
        },
    )

    with pytest.raises(InvalidOperation):
        b2c_tms_service.board(
            trip_id=uuid4_str(),
            time=time_now(),
            location=random_location(),
            mode=boarding_mode_dm(),
        )


@responses.activate
def test_board_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/board",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.board(
            trip_id=uuid4_str(),
            time=time_now(),
            location=random_location(),
            mode=boarding_mode_dm(),
        )


@responses.activate
def test_deboard_is_successful():
    time = time_now()
    location = random_location()
    mode = BoardingMode(type="MANUAL", id=uuid4_str())
    booking_request_json = booking_request_api_response()
    trip = trip_dm()
    booking_request = BookingRequest.from_dict(booking_request_json)

    def request_callback(request: PreparedRequest) -> Tuple:
        payload = json.loads(request.body)
        assert payload == serialize(
            dict(
                trip_id=trip.id,
                time=time,
                location=location,
                mode=mode,
            )
        )
        return (
            HTTPStatus.OK,
            {},
            json.dumps({"data": booking_request_json}),
        )

    responses.add_callback(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/deboard",
        callback=request_callback,
        content_type="application/json",
    )

    result = b2c_tms_service.deboard(
        trip_id=trip.id,
        time=time,
        location=location,
        mode=mode,
    )
    assert result == booking_request


@responses.activate
def test_deboard_raises_error_when_booking_not_found():
    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/deboard",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "BOOKING_NOT_FOUND",
                "message": "Booking not found",
            }
        },
    )

    with pytest.raises(BookingNotFound):
        b2c_tms_service.deboard(
            trip_id=uuid4_str(),
            time=time_now(),
            location=random_location(),
            mode=boarding_mode_dm(),
        )


@responses.activate
def test_deboard_raises_error_when_booking_not_found_on_trip():
    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/deboard",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "BOOKING_NOT_FOUND_ON_TRIP",
                "message": "Booking not found on trip",
            }
        },
    )

    with pytest.raises(BookingNotFoundOnTrip):
        b2c_tms_service.deboard(
            trip_id=uuid4_str(),
            time=time_now(),
            location=random_location(),
            mode=boarding_mode_dm(),
        )


@responses.activate
def test_deboard_raises_error_when_trip_not_found():
    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/deboard",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "TRIP_NOT_FOUND",
                "message": "Trip not found",
            }
        },
    )

    with pytest.raises(TripNotFound):
        b2c_tms_service.deboard(
            trip_id=uuid4_str(),
            time=time_now(),
            location=random_location(),
            mode=boarding_mode_dm(),
        )


@responses.activate
def test_deboard_raises_error_when_invalid_operation():
    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/deboard",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "CLIENT_ERROR",
                "message": "Invalid Operation",
            }
        },
    )

    with pytest.raises(InvalidOperation):
        b2c_tms_service.deboard(
            trip_id=uuid4_str(),
            time=time_now(),
            location=random_location(),
            mode=boarding_mode_dm(),
        )


@responses.activate
def test_deboard_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/booking_requests/deboard",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.deboard(
            trip_id=uuid4_str(),
            time=time_now(),
            location=random_location(),
            mode=boarding_mode_dm(),
        )
