from http import HTTPStatus

import pytest
import responses
from shuttlis.utils import uuid4_str

from b2c_tms_wrapper.models import BookingOpeningTime
from b2c_tms_wrapper.services.b2c_tms import B2CTMS
from tests.factories import booking_opening_time_api_response

fake_b2c_tms_url = "http://b2c_tms"
b2c_tms_service = B2CTMS(b2c_tms_url=fake_b2c_tms_url)


@responses.activate
def test_get_booking_opening_time_is_successful():
    line_id = uuid4_str()
    booking_opening_time_json = booking_opening_time_api_response(line_id=line_id)
    booking_opening_time = BookingOpeningTime.from_dict(booking_opening_time_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_opening_times/{line_id}",
        status=HTTPStatus.OK,
        json={"data": booking_opening_time_json},
    )

    result = b2c_tms_service.get_booking_opening_time(line_id=line_id)
    assert result == booking_opening_time


@responses.activate
def test_get_booking_opening_time_returns_none_when_not_found():
    line_id = uuid4_str()

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_opening_times/{line_id}",
        status=HTTPStatus.NOT_FOUND,
    )

    booking_opening_time = b2c_tms_service.get_booking_opening_time(line_id=line_id)
    assert booking_opening_time is None


@responses.activate
def test_get_booking_opening_time_raises_runtime_error_when_status_is_internal_error():
    line_id = uuid4_str()

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_opening_times/{line_id}",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms_service.get_booking_opening_time(line_id=line_id)
