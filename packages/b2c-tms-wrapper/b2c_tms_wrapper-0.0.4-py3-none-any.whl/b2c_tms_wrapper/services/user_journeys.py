from http import HTTPStatus
from typing import List

from shuttl_time import TimeWindow
from shuttlis.serialization import serialize

from b2c_tms_wrapper.models import UserJourneyRequest, UserJourney
from b2c_tms_wrapper.timeout import SessionWithTimeOut
from b2c_tms_wrapper.utils import mk_exc


class UserJourneysService:
    def __init__(self, url: str, session: SessionWithTimeOut):
        self._url = url
        self._session = session

    def get_user_journeys(
        self, user_journey_requests: List[UserJourneyRequest], time_window: TimeWindow
    ) -> List[UserJourney]:
        json = {
            "user_journey_requests": user_journey_requests,
            "time_window": {
                "from_time": time_window.from_date,
                "to_time": time_window.to_date,
            },
        }

        response = self._session.get(
            f"{self._url}/api/v1/user_journeys", json=serialize(json)
        )

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return [
            UserJourney.from_dict(user_journey)
            for user_journey in response.json()["data"]
        ]
