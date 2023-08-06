from datetime import datetime
from http import HTTPStatus
from typing import List, Dict

from shuttlis.serialization import serialize
from shuttlis.utils import group_by

from b2c_tms_wrapper.error import (
    TripNotFound,
    NotAtLocation,
    EarlyForEventAction,
    InvalidOperation,
)
from b2c_tms_wrapper.models import TripEvent, TripEventType
from b2c_tms_wrapper.timeout import SessionWithTimeOut
from b2c_tms_wrapper.utils import mk_exc


class TripEventsService:
    def __init__(self, url: str, session: SessionWithTimeOut):
        self._url = url
        self._session = session

    def get_trip_events(self, trip_id: str) -> List[TripEvent]:
        response = self._session.get(f"{self._url}/api/v1/trips/{str(trip_id)}/events")

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise TripNotFound("No trip found for the requested id")

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return [
            TripEvent.from_dict(event_json) for event_json in response.json()["data"]
        ]

    def get_trip_events_by_trip_ids(
        self, trip_ids: List[str], types: List[TripEventType] = None
    ) -> Dict[str, List[TripEvent]]:
        if not trip_ids:
            return {}

        params = {"ids": ",".join(trip_ids)}
        if types:
            params["event_types"] = ",".join([type.value for type in types])

        response = self._session.get(
            f"{self._url}/api/v1/trips/events/by_trip_ids", params=params
        )

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        events = [
            TripEvent.from_dict(event_json) for event_json in response.json()["data"]
        ]
        return group_by(events, lambda event: event.trip_id)

    def capture_trip_event(
        self,
        trip_id: str,
        type: TripEventType,
        details: Dict,
        generated_at: datetime,
        generated_by: str,
    ) -> List[TripEvent]:
        event = {
            "type": type,
            "generated_at": generated_at,
            "details": details,
            "generated_by": generated_by,
        }
        response = self._session.post(
            f"{self._url}/api/v1/trips/{trip_id}/events",
            json=serialize(event),
        )

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise TripNotFound("No trip found for the requested id")

        if response.status_code == HTTPStatus.BAD_REQUEST:
            if response.json()["error"]["type"] == "NOT_AT_LOCATION":
                raise NotAtLocation(response.json()["error"]["message"])
            if response.json()["error"]["type"] == "EARLY_FOR_EVENT_ACTION":
                raise EarlyForEventAction(response.json()["error"]["message"])
            raise InvalidOperation(f"Invalid operation: {response.json()}")

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return [
            TripEvent.from_dict(event_json) for event_json in response.json()["data"]
        ]
