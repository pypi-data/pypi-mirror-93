import json
from datetime import timedelta
from http import HTTPStatus
from typing import Tuple

import pytest
import responses
from requests import PreparedRequest
from shuttl_time.time import time_now
from shuttlis.time import TimeWindow
from shuttlis.utils import uuid4_str

from b2c_tms_wrapper.error import (
    TripInfoAlreadyExists,
    InvalidOperation,
    TripNotFound,
    VehicleNonOperational,
    AllocationConflict,
    VehicleNotAttached,
    TripVehicleMismatch,
)
from b2c_tms_wrapper.models import Trip, TripState, TripType, TripAllocationAssociation
from b2c_tms_wrapper.services.b2c_tms import B2CTMS
from tests.factories import (
    trip_api_v1_response,
    trip_api_v2_response,
    random_location,
    trip_allocation_association_response,
)

fake_b2c_tms_url = "http://b2c_tms"
b2c_tms_service = B2CTMS(b2c_tms_url=fake_b2c_tms_url)


@responses.activate
def test_create_trip_is_successful():
    trip_json = trip_api_v1_response()
    trip = Trip.from_dict(trip_json)

    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips",
        status=HTTPStatus.OK,
        json={"data": trip_json},
    )

    assert b2c_tms_service.create_trip(trip_json) == trip


@responses.activate
def test_create_trip_raises_error_when_trip_info_already_exists():
    trip_json = trip_api_v1_response()

    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips",
        status=HTTPStatus.CONFLICT,
        json={
            "error": {
                "type": "TRIP_INFO_ALREADY_EXISTS",
                "message": "A trip already exists at the selected time.",
            }
        },
    )

    with pytest.raises(TripInfoAlreadyExists):
        b2c_tms_service.create_trip(trip_json)


@responses.activate
def test_create_trip_raises_error_when_invalid_operation():
    trip_json = trip_api_v1_response()

    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "INVALID_OPERATION",
                "message": f"Route with id: {uuid4_str()} is in planned state, so only DRY_RUN trips can be created",
            }
        },
    )

    with pytest.raises(InvalidOperation):
        b2c_tms_service.create_trip(trip_json)


@responses.activate
def test_create_trip_raises_runtime_error_when_status_is_internal_error():
    trip_json = trip_api_v1_response()

    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.create_trip(trip_json)


@responses.activate
def test_get_trip_by_id_is_successful():
    trip_json = trip_api_v1_response()
    trip = Trip.from_dict(trip_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip.id}",
        status=HTTPStatus.OK,
        json={"data": trip_json},
    )

    assert b2c_tms_service.get_trip_by_id(trip_id=trip.id) == trip


@responses.activate
def test_get_trip_by_id_returns_none_when_trip_does_not_exist():
    trip_id = uuid4_str()

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}",
        status=HTTPStatus.NOT_FOUND,
    )

    trip = b2c_tms_service.get_trip_by_id(trip_id=trip_id)
    assert trip is None


@responses.activate
def test_get_trip_by_id_raises_runtime_error_when_status_is_internal_error():
    trip_id = uuid4_str()

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_trip_by_id(trip_id=trip_id)


@responses.activate
def test_get_next_trip_for_vehicle_is_successful():
    trip_json = trip_api_v1_response()
    trip = Trip.from_dict(trip_json)
    vehicle_id = uuid4_str()

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/next/{vehicle_id}",
        status=HTTPStatus.OK,
        json={"data": trip_json},
    )

    assert b2c_tms_service.get_next_trip_for_vehicle(vehicle_id) == trip


@responses.activate
def test_get_next_trip_for_vehicle_returns_none_when_trip_does_not_exist():
    vehicle_id = uuid4_str()

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/next/{vehicle_id}",
        status=HTTPStatus.NOT_FOUND,
    )

    trip = b2c_tms_service.get_next_trip_for_vehicle(vehicle_id)
    assert trip is None


@responses.activate
def test_get_next_trip_for_vehicle_raises_runtime_error_when_status_is_internal_error():
    vehicle_id = uuid4_str()

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/next/{vehicle_id}",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_next_trip_for_vehicle(vehicle_id)


@responses.activate
def test_get_trips_by_ids_is_successful():
    trip_json = trip_api_v1_response()
    trip = Trip.from_dict(trip_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/by_ids",
        status=HTTPStatus.OK,
        json={"data": [trip_json]},
    )

    trips = b2c_tms_service.get_trips_by_ids(trip_ids=[trip.id, uuid4_str()])
    assert trips == [trip]


def test_get_trips_by_ids_when_no_trip_ids_given():
    trips = b2c_tms_service.get_trips_by_ids(trip_ids=[])
    assert trips == []


@responses.activate
def test_get_trips_by_ids_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/by_ids",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_trips_by_ids(trip_ids=[uuid4_str()])


@responses.activate
def test_get_trips_by_vehicle_ids_is_successful():
    trip_json = trip_api_v1_response()
    trip = Trip.from_dict(trip_json)
    vehicle_id = trip.vehicle_id

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/by_vehicle_ids",
        status=HTTPStatus.OK,
        json={"data": [trip_json]},
    )

    trips = b2c_tms_service.get_trips_by_vehicle_ids(
        vehicle_ids=[vehicle_id], time_window=TimeWindow()
    )
    assert trips == [trip]


def test_get_trips_by_vehicle_ids_when_no_vehicle_ids_given():
    trips = b2c_tms_service.get_trips_by_vehicle_ids(
        vehicle_ids=[], time_window=TimeWindow()
    )
    assert trips == []


@responses.activate
def test_get_trips_by_vehicle_ids_raises_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/by_vehicle_ids",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
    with pytest.raises(TypeError):
        b2c_tms_service.get_trips_by_vehicle_ids(
            vehicle_ids=[uuid4_str(), uuid4_str()], time_window=TimeWindow()
        )


@responses.activate
def test_get_trips_by_driver_ids_is_successful():
    trip_json = trip_api_v1_response()
    trip = Trip.from_dict(trip_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/by_driver_ids",
        status=HTTPStatus.OK,
        json={"data": [trip_json]},
    )

    trips = b2c_tms_service.get_trips_by_driver_ids(
        driver_ids=[uuid4_str()], time_window=TimeWindow()
    )
    assert trips == [trip]


def test_get_trips_by_driver_ids_when_no_drivers_ids_given():
    trips = b2c_tms_service.get_trips_by_driver_ids(
        driver_ids=[], time_window=TimeWindow()
    )
    assert trips == []


@responses.activate
def test_get_trips_by_driver_ids_raises_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/by_driver_ids",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
    with pytest.raises(RuntimeError):
        b2c_tms_service.get_trips_by_driver_ids(
            driver_ids=[uuid4_str(), uuid4_str()], time_window=TimeWindow()
        )


@responses.activate
def test_get_completed_trips_is_successful():
    trip_json = trip_api_v1_response()
    trip = Trip.from_dict(trip_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/completed",
        status=HTTPStatus.OK,
        json={"data": [trip_json], "meta": {"cursor": {"last": None}}},
    )

    trips = b2c_tms_service.get_completed_trips(from_time=time_now())
    assert trips == [trip]


@responses.activate
def test_get_completed_trips_raises_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/completed",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
    with pytest.raises(RuntimeError):
        b2c_tms_service.get_completed_trips(from_time=time_now())


@responses.activate
def test_get_trips_by_updated_time_is_successful():
    from_time = time_now()
    trip_json = trip_api_v1_response()
    trip = Trip.from_dict(trip_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/by_updated_time",
        status=HTTPStatus.OK,
        json={"data": [trip_json], "meta": {"cursor": {"last": None}}},
    )

    trips = b2c_tms_service.get_trips_by_updated_time(from_time=from_time)
    assert trips == [trip]


@responses.activate
def test_get_trips_by_updated_time_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/by_updated_time",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_trips_by_updated_time(from_time=time_now())


@responses.activate
def test_get_trips_is_successful():
    route_id_1 = uuid4_str()
    route_id_2 = uuid4_str()
    trip_json = trip_api_v1_response()
    trip = Trip.from_dict(trip_json)

    def request_callback(request: PreparedRequest) -> Tuple:
        assert route_id_1 in request.url
        assert route_id_2 in request.url
        return (
            HTTPStatus.OK,
            {},
            json.dumps({"data": [trip_json], "meta": {"cursor": {"last": None}}}),
        )

    responses.add_callback(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips",
        callback=request_callback,
    )

    trips = b2c_tms_service.get_trips(
        route_ids=[route_id_1, route_id_2],
        from_time=time_now(),
        to_time=time_now(),
        states=[TripState.PLANNED],
        types=[TripType.MANUAL],
    )
    assert trips == [trip]


@responses.activate
def test_get_trips_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_trips()


@responses.activate
def test_get_trips_with_tracked_way_points_is_successful():
    route_id_1 = uuid4_str()
    route_id_2 = uuid4_str()
    trip_json = trip_api_v2_response()
    trip = Trip.from_dict(trip_json)

    def request_callback(request: PreparedRequest) -> Tuple:
        assert route_id_1 in request.url
        assert route_id_2 in request.url
        return (
            HTTPStatus.OK,
            {},
            json.dumps({"data": [trip_json], "meta": {"cursor": {"last": None}}}),
        )

    responses.add_callback(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v2/trips",
        callback=request_callback,
    )

    trips = b2c_tms_service.get_trips_with_tracked_way_points(
        route_ids=[route_id_1, route_id_2],
        from_time=time_now(),
        to_time=time_now(),
        states=[TripState.PLANNED],
    )
    assert trips == [trip]


@responses.activate
def test_get_trips_with_tracked_way_points_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v2/trips",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_trips_with_tracked_way_points()


@responses.activate
def test_attach_vehicle_on_trip_is_successful():
    trip_json = trip_api_v1_response()
    trip = Trip.from_dict(trip_json)
    vehicle_id = trip.vehicle_id

    def request_callback(request: PreparedRequest) -> Tuple:
        payload = json.loads(request.body)
        assert payload["id"] == vehicle_id
        return (
            HTTPStatus.OK,
            {},
            json.dumps({"data": trip_json}),
        )

    responses.add_callback(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip.id}/vehicle",
        callback=request_callback,
        content_type="application/json",
    )

    trip = b2c_tms_service.attach_vehicle_to_trip(
        trip_id=trip.id, vehicle_id=vehicle_id
    )
    assert trip == trip


@responses.activate
def test_attach_vehicle_on_trip_raises_error_when_vehicle_non_operational():
    trip_id = uuid4_str()
    vehicle_id = uuid4_str()

    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/vehicle",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "VEHICLE_NON_OPERATIONAL",
                "message": f"Allocation failed for vehicle: {vehicle_id} on trip: {trip_id} as vehicle non-operational",
            }
        },
    )

    with pytest.raises(VehicleNonOperational):
        b2c_tms_service.attach_vehicle_to_trip(trip_id=trip_id, vehicle_id=vehicle_id)


@responses.activate
def test_attach_vehicle_on_trip_raises_error_when_allocation_conflict():
    trip_id = uuid4_str()
    vehicle_id = uuid4_str()

    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/vehicle",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "ALLOCATION_CONFLICT",
                "message": f"Allocation with vehicle {vehicle_id} failed for trip {trip_id} as vehicle was allocated elsewhere",
            }
        },
    )

    with pytest.raises(AllocationConflict):
        b2c_tms_service.attach_vehicle_to_trip(trip_id=trip_id, vehicle_id=vehicle_id)


@responses.activate
def test_attach_vehicle_on_trip_raises_error_when_invalid_operation():
    trip_id = uuid4_str()
    vehicle_id = uuid4_str()

    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/vehicle",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "CLIENT_ERROR",
                "message": "Allocation failure",
            }
        },
    )

    with pytest.raises(InvalidOperation):
        b2c_tms_service.attach_vehicle_to_trip(trip_id=trip_id, vehicle_id=vehicle_id)


@responses.activate
def test_attach_vehicle_on_trip_raises_runtime_error_when_status_is_internal_error():
    trip_id = uuid4_str()
    vehicle_id = uuid4_str()

    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/vehicle",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.attach_vehicle_to_trip(trip_id=trip_id, vehicle_id=vehicle_id)


@responses.activate
def test_detach_vehicle_from_trip():
    trip_json = trip_api_v1_response()
    trip = Trip.from_dict(trip_json)

    def request_callback(request: PreparedRequest) -> Tuple:
        assert not request.body
        return (
            HTTPStatus.OK,
            {},
            json.dumps({"data": trip_json}),
        )

    responses.add_callback(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip.id}/vehicle/detach",
        callback=request_callback,
        content_type="application/json",
    )

    trip = b2c_tms_service.detach_vehicle_from_trip(trip_id=trip.id)
    assert trip == trip


@responses.activate
def test_update_vehicle_on_trip_is_sucessful():
    trip_json = trip_api_v1_response()
    trip = Trip.from_dict(trip_json)

    new_vehicle_id = uuid4_str()

    def request_callback(request: PreparedRequest) -> Tuple:
        payload = json.loads(request.body)
        assert payload == {
            "trip_id": trip.id,
            "from_vehicle_id": trip.vehicle_id,
            "to_vehicle_id": new_vehicle_id,
        }
        return (
            HTTPStatus.OK,
            {},
            json.dumps({"data": trip_json}),
        )

    responses.add_callback(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/vehicle/update",
        callback=request_callback,
        content_type="application/json",
    )

    trip = b2c_tms_service.update_vehicle_on_trip(
        trip_id=trip.id,
        current_vehicle_id=trip.vehicle_id,
        new_vehicle_id=new_vehicle_id,
    )

    assert trip == trip


@responses.activate
def test_update_vehicle_on_trip_raises_error_when_trip_not_found():
    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/vehicle/update",
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(TripNotFound):
        b2c_tms_service.update_vehicle_on_trip(
            trip_id=uuid4_str(),
            current_vehicle_id=uuid4_str(),
            new_vehicle_id=uuid4_str(),
        )


@responses.activate
def test_update_vehicle_on_trip_raises_error_when_vehicle_not_attached():
    trip_id = uuid4_str()
    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/vehicle/update",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "VEHICLE_NOT_ATTACHED",
                "message": f"Trip has does not have any vehicle attached {trip_id}",
            }
        },
    )

    with pytest.raises(VehicleNotAttached):
        b2c_tms_service.update_vehicle_on_trip(
            trip_id=trip_id,
            current_vehicle_id=uuid4_str(),
            new_vehicle_id=uuid4_str(),
        )


@responses.activate
def test_update_vehicle_on_trip_raises_error_when_vehicle_mismatch():
    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/vehicle/update",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "TRIP_VEHICLE_MISMATCH",
                "message": f"Trip has a different vehicle attached :{uuid4_str()}",
            }
        },
    )

    with pytest.raises(TripVehicleMismatch):
        b2c_tms_service.update_vehicle_on_trip(
            trip_id=uuid4_str(),
            current_vehicle_id=uuid4_str(),
            new_vehicle_id=uuid4_str(),
        )


@responses.activate
def test_update_vehicle_on_trip_raises_error_when_invalid_operation():
    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/vehicle/update",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "INVALID_OPERATION",
                "message": f"Trip is already in {TripState.COMPLETED}, cannot update vehicle",
            }
        },
    )

    with pytest.raises(InvalidOperation):
        b2c_tms_service.update_vehicle_on_trip(
            trip_id=uuid4_str(),
            current_vehicle_id=uuid4_str(),
            new_vehicle_id=uuid4_str(),
        )


@responses.activate
def test_update_vehicle_on_trip_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/vehicle/update",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.update_vehicle_on_trip(
            trip_id=uuid4_str(),
            current_vehicle_id=uuid4_str(),
            new_vehicle_id=uuid4_str(),
        )


@responses.activate
def test_cancel_trip_is_successful():
    trip_json = trip_api_v1_response()
    trip = Trip.from_dict(trip_json)
    generated_by = uuid4_str()
    meta_info = {"reason": "Dummy Reason"}

    def request_callback(request: PreparedRequest) -> Tuple:
        payload = json.loads(request.body)
        assert payload["from_state"] == "PLANNED"
        assert payload["meta_info"] == meta_info
        assert payload["generated_by"] == generated_by
        return (
            HTTPStatus.OK,
            {},
            json.dumps({"data": trip_json}),
        )

    responses.add_callback(
        responses.DELETE,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip.id}",
        callback=request_callback,
        content_type="application/json",
    )

    returned_trip = b2c_tms_service.cancel_trip(
        trip_id=trip.id,
        trip_state=TripState.PLANNED,
        generated_by=generated_by,
        meta_info=meta_info,
    )

    assert returned_trip == trip


@responses.activate
def test_cancel_trip_raises_error_when_trip_not_found():
    trip_id = uuid4_str()
    responses.add(
        responses.DELETE,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}",
        status=HTTPStatus.NOT_FOUND,
        json={
            "error": {
                "type": "TRIP_NOT_FOUND",
                "message": "No trip found for the requested id",
            }
        },
    )

    with pytest.raises(TripNotFound):
        b2c_tms_service.cancel_trip(
            trip_id=trip_id,
            trip_state=TripState.PLANNED,
            generated_by=uuid4_str(),
            meta_info={},
        )


@responses.activate
def test_cancel_trip_raises_error_when_invalid_operation():
    trip_id = uuid4_str()
    responses.add(
        responses.DELETE,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "CLIENT_ERROR",
                "message": f"Invalid state transition attempted- from_state : {TripState.COMPLETED},to_state: {TripState.CANCELLED}",
            }
        },
    )

    with pytest.raises(InvalidOperation):
        b2c_tms_service.cancel_trip(
            trip_id=trip_id,
            trip_state=TripState.COMPLETED,
            generated_by=uuid4_str(),
            meta_info={},
        )


@responses.activate
def test_cancel_trip_raises_runtime_error_when_status_is_internal_error():
    trip_id = uuid4_str()

    responses.add(
        responses.DELETE,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.cancel_trip(
            trip_id=trip_id,
            trip_state=TripState.PLANNED,
            generated_by=uuid4_str(),
            meta_info={},
        )


@responses.activate
def test_get_trip_path_is_successful():
    path = [random_location(), random_location()]
    path_json = [{"lat": loc.lat, "lng": loc.lng} for loc in path]
    trip_id = uuid4_str()

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/path",
        status=HTTPStatus.OK,
        json={"data": path_json},
    )

    assert b2c_tms_service.get_trip_path(trip_id) == path


@responses.activate
def test_get_trip_path_raises_runtime_error_when_status_is_internal_error():
    trip_id = uuid4_str()

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/path",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_trip_path(trip_id)


@responses.activate
def test_start_trip_is_successful():
    trip_json = trip_api_v1_response()
    trip = Trip.from_dict(trip_json)

    responses.add(
        responses.PATCH,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip.id}/start",
        status=HTTPStatus.OK,
        json={"data": trip_json},
    )

    started_trip = b2c_tms_service.start_trip(
        trip_id=trip.id, reason="Dummy reason", generated_by=uuid4_str()
    )
    assert started_trip == trip


@responses.activate
def test_start_trip_raises_error_when_trip_not_found():
    trip_id = uuid4_str()

    responses.add(
        responses.PATCH,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/start",
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(TripNotFound):
        b2c_tms_service.start_trip(
            trip_id=trip_id, reason="Dummy reason", generated_by=uuid4_str()
        )


@responses.activate
def test_start_trip_raises_error_when_invalid_operation():
    trip_id = uuid4_str()

    responses.add(
        responses.PATCH,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/start",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "CLIENT_ERROR",
                "message": f"Invalid state transition attempted- from_state : {TripState.CANCELLED},to_state: {TripState.ACTIVE}",
            }
        },
    )

    with pytest.raises(InvalidOperation):
        b2c_tms_service.start_trip(
            trip_id=trip_id, reason="Dummy reason", generated_by=uuid4_str()
        )


@responses.activate
def test_start_trip_raises_runtime_error_when_status_is_internal_error():
    trip_id = uuid4_str()

    responses.add(
        responses.PATCH,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/start",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.start_trip(
            trip_id=trip_id, reason="Dummy reason", generated_by=uuid4_str()
        )


@responses.activate
def test_end_trip_is_successful():
    trip_json = trip_api_v1_response()
    trip = Trip.from_dict(trip_json)

    responses.add(
        responses.PATCH,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip.id}/end",
        status=HTTPStatus.OK,
        json={"data": trip_json},
    )

    started_trip = b2c_tms_service.end_trip(
        trip_id=trip.id, reason="Dummy reason", generated_by=uuid4_str()
    )
    assert started_trip == trip


@responses.activate
def test_end_trip_raises_error_when_trip_not_found():
    trip_id = uuid4_str()

    responses.add(
        responses.PATCH,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/end",
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(TripNotFound):
        b2c_tms_service.end_trip(
            trip_id=trip_id, reason="Dummy reason", generated_by=uuid4_str()
        )


@responses.activate
def test_end_trip_raises_error_when_invalid_operation():
    trip_id = uuid4_str()

    responses.add(
        responses.PATCH,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/end",
        status=HTTPStatus.BAD_REQUEST,
        json={
            "error": {
                "type": "CLIENT_ERROR",
                "message": f"Invalid state transition attempted- from_state : {TripState.CANCELLED},to_state: {TripState.ACTIVE}",
            }
        },
    )

    with pytest.raises(InvalidOperation):
        b2c_tms_service.end_trip(
            trip_id=trip_id, reason="Dummy reason", generated_by=uuid4_str()
        )


@responses.activate
def test_end_trip_raises_runtime_error_when_status_is_internal_error():
    trip_id = uuid4_str()

    responses.add(
        responses.PATCH,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/end",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.end_trip(
            trip_id=trip_id, reason="Dummy reason", generated_by=uuid4_str()
        )


@responses.activate
def test_get_trip_paths_in_bulk_is_successful():
    path = [random_location(), random_location()]
    path_json = [{"lat": loc.lat, "lng": loc.lng} for loc in path]
    trip_id = uuid4_str()

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/path",
        status=HTTPStatus.OK,
        json={"data": {trip_id: path_json}},
    )

    assert b2c_tms_service.get_trip_paths_in_bulk(trip_ids=[trip_id]) == {trip_id: path}


def test_get_trip_paths_in_bulk_when_no_trip_ids_given():
    assert b2c_tms_service.get_trip_paths_in_bulk(trip_ids=[]) == {}


@responses.activate
def test_get_trip_paths_in_bulk_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/path",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_trip_paths_in_bulk([uuid4_str()])


@responses.activate
def test_get_trip_reschedule_window_is_successful():
    now = time_now()
    from_date = now - timedelta(hours=1)
    to_date = now + timedelta(hours=1)
    window = TimeWindow(from_date=from_date, to_date=to_date)
    window_json = {
        "from_date": window.from_date.isoformat(),
        "to_date": window.to_date.isoformat(),
    }
    trip_id = uuid4_str()

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/reschedule_window",
        status=HTTPStatus.OK,
        json={"data": window_json},
    )

    result = b2c_tms_service.get_trip_reschedule_window(trip_id)
    assert result.from_date == window.from_date
    assert result.to_date == window.to_date


@responses.activate
def test_get_trip_reschedule_window_raises_error_when_trip_not_found():
    trip_id = uuid4_str()

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/reschedule_window",
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(TripNotFound):
        b2c_tms_service.get_trip_reschedule_window(trip_id)


@responses.activate
def test_get_trip_reschedule_window_raises_runtime_error_when_status_is_internal_error():
    trip_id = uuid4_str()

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/reschedule_window",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_trip_reschedule_window(trip_id)


@responses.activate
def test_mark_vehicle_breakdown_for_trip_is_successful():
    trip_json = trip_api_v1_response()
    trip = Trip.from_dict(trip_json)

    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip.id}/mark_vehicle_breakdown",
        status=HTTPStatus.OK,
        json={"data": trip_json},
    )

    returned_trip = b2c_tms_service.mark_vehicle_breakdown_for_trip(
        trip_id=trip.id,
        vehicle_id_on_trip=trip.vehicle_id,
        updated_by=uuid4_str(),
        reason_info={"reason_info": {"category": "test category", "is_genuine": True}},
        vehicle_id_to_attach=uuid4_str(),
    )
    assert returned_trip == trip


@responses.activate
def test_mark_vehicle_breakdown_for_trip_raises_runtime_error_when_status_is_internal_error():
    trip_id = uuid4_str()

    responses.add(
        responses.POST,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/mark_vehicle_breakdown",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.mark_vehicle_breakdown_for_trip(
            trip_id=trip_id,
            vehicle_id_on_trip=uuid4_str(),
            updated_by=uuid4_str(),
            reason_info={
                "reason_info": {"category": "test category", "is_genuine": True}
            },
            vehicle_id_to_attach=uuid4_str(),
        )


@responses.activate
def test_get_trip_allocation_associations_is_successful():
    trip_id = uuid4_str()
    association_json = trip_allocation_association_response(trip_id=trip_id)
    association = TripAllocationAssociation.from_dict(association_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/allocation_associations",
        status=HTTPStatus.OK,
        json={
            "data": [association_json],
            "meta": {"cursor": {"last": None}},
        },
    )

    result = b2c_tms_service.get_trip_allocation_associations()
    assert result == [association]


@responses.activate
def test_get_trip_allocation_associations_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/allocation_associations",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_trip_allocation_associations()


@responses.activate
def test_get_trips_with_overlapping_allocations_is_successful():
    trip_json = trip_api_v1_response()
    trip = Trip.from_dict(trip_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/overlapping_allocations",
        status=HTTPStatus.OK,
        json={"data": [trip_json]},
    )

    trips = b2c_tms_service.get_trips_with_overlapping_allocations(
        vehicle_ids=[uuid4_str()], time_window=TimeWindow()
    )
    assert trips == [trip]


@responses.activate
def test_get_trips_with_overlapping_allocations_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/overlapping_allocations",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_trips_with_overlapping_allocations(
            vehicle_ids=[uuid4_str()], time_window=TimeWindow()
        )
