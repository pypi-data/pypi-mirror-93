from http import HTTPStatus

import pytest
import responses
from shuttlis.utils import uuid4_str

from b2c_tms_wrapper.error import (
    TripNotFound,
    NotAtLocation,
    EarlyForEventAction,
    InvalidOperation,
)
from b2c_tms_wrapper.models import TripEvent
from b2c_tms_wrapper.services.b2c_tms import B2CTMS
from tests.factories import trip_event_api_response

fake_b2c_tms_url = "http://b2c_tms"
b2c_tms_service = B2CTMS(b2c_tms_url=fake_b2c_tms_url)


@responses.activate
def test_get_trip_events_is_successful():
    trip_id = uuid4_str()
    trip_event_json = trip_event_api_response(trip_id=trip_id)
    trip_event = TripEvent.from_dict(trip_event_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/events",
        status=HTTPStatus.OK,
        json={"data": [trip_event_json]},
    )

    trip_events = b2c_tms_service.get_trip_events(trip_id=trip_id)
    assert trip_events == [trip_event]


@responses.activate
def test_get_trip_events_raises_error_when_trip_not_found():
    trip_id = uuid4_str()

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/events",
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(TripNotFound):
        b2c_tms_service.get_trip_events(trip_id=trip_id)


@responses.activate
def test_get_trip_events_raises_runtime_error_when_status_is_internal_error():
    trip_id = uuid4_str()

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/events",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_trip_events(trip_id=trip_id)


@responses.activate
def test_get_trip_events_by_trip_ids_is_successful():
    trip_id_1 = uuid4_str()
    trip_event_json_1 = trip_event_api_response(trip_id=trip_id_1)
    trip_event_1 = TripEvent.from_dict(trip_event_json_1)

    trip_id_2 = uuid4_str()
    trip_event_json_2 = trip_event_api_response(trip_id=trip_id_2)
    trip_event_2 = TripEvent.from_dict(trip_event_json_2)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/events/by_trip_ids",
        status=HTTPStatus.OK,
        json={"data": [trip_event_json_1, trip_event_json_2]},
    )

    trip_id_to_events_map = b2c_tms_service.get_trip_events_by_trip_ids(
        trip_ids=[trip_id_1, trip_id_2]
    )
    assert trip_id_to_events_map == {
        trip_id_1: [trip_event_1],
        trip_id_2: [trip_event_2],
    }


def test_get_trip_events_by_trip_ids_when_no_trip_ids_given():
    trip_id_to_events_map = b2c_tms_service.get_trip_events_by_trip_ids(trip_ids=[])
    assert trip_id_to_events_map == {}


@responses.activate
def test_get_trip_events_by_trip_ids_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/events/by_trip_ids",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_trip_events_by_trip_ids(trip_ids=[uuid4_str()])


@responses.activate
def test_capture_trip_event_is_successful():
    trip_id = uuid4_str()
    trip_event_json = trip_event_api_response(trip_id=trip_id)
    trip_event = TripEvent.from_dict(trip_event_json)

    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/events",
        status=HTTPStatus.OK,
        json={"data": [trip_event_json]},
    )

    captured_events = b2c_tms_service.capture_trip_event(
        trip_id=trip_id,
        type=trip_event.type,
        details=trip_event.details,
        generated_by=trip_event.generated_by,
        generated_at=trip_event.generated_at,
    )

    assert captured_events == [trip_event]


@responses.activate
def test_test_capture_trip_event_raises_error_when_trip_not_found():
    trip_event_json = trip_event_api_response()
    trip_event = TripEvent.from_dict(trip_event_json)

    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_event.id}/events",
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(TripNotFound):
        b2c_tms_service.capture_trip_event(
            trip_id=trip_event.id,
            type=trip_event.type,
            details=trip_event.details,
            generated_by=trip_event.generated_by,
            generated_at=trip_event.generated_at,
        )


@responses.activate
def test_test_capture_trip_event_raises_error_when_not_at_location():
    trip_event_json = trip_event_api_response()
    trip_event = TripEvent.from_dict(trip_event_json)

    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_event.id}/events",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "NOT_AT_LOCATION",
                "message": "Vehicle not in 2 km range of trip's starting location!!",
            }
        },
    )

    with pytest.raises(NotAtLocation):
        b2c_tms_service.capture_trip_event(
            trip_id=trip_event.id,
            type=trip_event.type,
            details=trip_event.details,
            generated_by=trip_event.generated_by,
            generated_at=trip_event.generated_at,
        )


@responses.activate
def test_test_capture_trip_event_raises_error_when_early_for_event_action():
    trip_event_json = trip_event_api_response()
    trip_event = TripEvent.from_dict(trip_event_json)

    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_event.id}/events",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "EARLY_FOR_EVENT_ACTION",
                "message": "Reach event can only be triggered 60 minutes before the trip start time",
            }
        },
    )

    with pytest.raises(EarlyForEventAction):
        b2c_tms_service.capture_trip_event(
            trip_id=trip_event.id,
            type=trip_event.type,
            details=trip_event.details,
            generated_by=trip_event.generated_by,
            generated_at=trip_event.generated_at,
        )


@responses.activate
def test_test_capture_trip_event_raises_error_when_invalid_operation():
    trip_event_json = trip_event_api_response()
    trip_event = TripEvent.from_dict(trip_event_json)

    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_event.id}/events",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "CLIENT_ERROR",
                "message": "Invalid Operation",
            }
        },
    )

    with pytest.raises(InvalidOperation):
        b2c_tms_service.capture_trip_event(
            trip_id=trip_event.id,
            type=trip_event.type,
            details=trip_event.details,
            generated_by=trip_event.generated_by,
            generated_at=trip_event.generated_at,
        )


@responses.activate
def test_capture_trip_event_raises_runtime_error_when_status_is_internal_error():
    trip_event_json = trip_event_api_response()
    trip_event = TripEvent.from_dict(trip_event_json)

    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_event.id}/events",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.capture_trip_event(
            trip_id=trip_event.id,
            type=trip_event.type,
            details=trip_event.details,
            generated_by=trip_event.generated_by,
            generated_at=trip_event.generated_at,
        )
