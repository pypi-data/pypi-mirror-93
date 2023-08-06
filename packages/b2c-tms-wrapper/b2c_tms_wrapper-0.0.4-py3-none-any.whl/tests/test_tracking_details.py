from http import HTTPStatus

import pytest
import responses
from shuttlis.utils import uuid4_str

from b2c_tms_wrapper.models import TripTrackingDetails
from b2c_tms_wrapper.services.b2c_tms import B2CTMS
from tests.factories import trip_tracking_details_response


fake_b2c_tms_url = "http://b2c_tms"
b2c_tms_service = B2CTMS(b2c_tms_url=fake_b2c_tms_url)


@responses.activate
def test_get_tracking_details_for_trip_is_successful():
    trip_id = uuid4_str()
    tracking_details_json = trip_tracking_details_response(trip_id=trip_id)
    tracking_details = TripTrackingDetails.from_dict(tracking_details_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/tracking_details",
        status=HTTPStatus.OK,
        json={"data": tracking_details_json},
    )

    result = b2c_tms_service.get_tracking_details_for_trip(trip_id)
    assert result == tracking_details


@responses.activate
def test_get_tracking_details_for_trip_raises_runtime_error_when_status_is_internal_error():
    trip_id = uuid4_str()

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/{trip_id}/tracking_details",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_tracking_details_for_trip(trip_id)


@responses.activate
def test_get_tracking_details_for_trips_is_successful():
    trip_id = uuid4_str()
    tracking_details_json = trip_tracking_details_response(trip_id=trip_id)
    tracking_details = TripTrackingDetails.from_dict(tracking_details_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/tracking_details",
        status=HTTPStatus.OK,
        json={"data": [tracking_details_json]},
    )

    result = b2c_tms_service.get_tracking_details_for_trips([trip_id])
    assert result == [tracking_details]


@responses.activate
def test_get_tracking_details_for_trips_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/trips/tracking_details",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_tracking_details_for_trips([uuid4_str()])
