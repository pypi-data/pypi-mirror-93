from http import HTTPStatus

import pytest
import responses
from shuttlis.utils import uuid4_str

from b2c_tms_wrapper.models import Booking
from b2c_tms_wrapper.services.b2c_tms import B2CTMS
from tests.factories import booking_history_api_response

fake_b2c_tms_url = "http://b2c_tms"
b2c_tms = B2CTMS(b2c_tms_url=fake_b2c_tms_url)


@responses.activate
def test_get_booking_history_by_booking_request_ids_is_successful():
    booking_request_1_id, booking_request_2_id = uuid4_str(), uuid4_str()
    booking_1_json = booking_history_api_response(
        booking_request_id=booking_request_1_id
    )
    booking_2_json = booking_history_api_response(
        booking_request_id=booking_request_2_id
    )

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_history/by_booking_requests",
        status=HTTPStatus.OK,
        json={"data": [[booking_1_json], [booking_2_json]]},
    )

    booking_history = b2c_tms.get_booking_history_by_booking_request_ids(
        booking_request_ids=[booking_request_1_id, booking_request_2_id]
    )
    assert booking_history == [
        Booking.from_dict(booking_1_json),
        Booking.from_dict(booking_2_json),
    ]


def test_get_booking_history_by_booking_request_ids_when_no_ids_given():
    booking_history = b2c_tms.get_booking_history_by_booking_request_ids(
        booking_request_ids=[]
    )
    assert booking_history == []


@responses.activate
def test_get_booking_history_by_booking_request_ids_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/booking_history/by_booking_requests",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms.get_booking_history_by_booking_request_ids(
            booking_request_ids=[uuid4_str()]
        )
