from http import HTTPStatus

import pytest
import responses
from shuttl_time import TimeWindow

from b2c_tms_wrapper.models import UserJourney
from b2c_tms_wrapper.services.b2c_tms import B2CTMS
from tests.factories import user_journey_request_dm, user_journey_response

fake_b2c_tms_url = "http://b2c_tms"
b2c_tms = B2CTMS(b2c_tms_url=fake_b2c_tms_url)


@responses.activate
def test_get_user_journeys_is_successful():
    user_journey_request = user_journey_request_dm()
    user_journey_json = user_journey_response()
    user_journey = UserJourney.from_dict(user_journey_json)

    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/user_journeys",
        status=HTTPStatus.OK,
        json={"data": [user_journey_json]},
    )

    user_journeys = b2c_tms.get_user_journeys(
        user_journey_requests=[user_journey_request], time_window=TimeWindow()
    )
    assert user_journeys == [user_journey]


@responses.activate
def test_get_user_journeys_raises_runtime_error_when_status_is_internal_error():
    responses.add(
        responses.GET,
        f"{fake_b2c_tms_url}/api/v1/user_journeys",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms.get_user_journeys(
            user_journey_requests=[user_journey_request_dm()], time_window=TimeWindow()
        )
