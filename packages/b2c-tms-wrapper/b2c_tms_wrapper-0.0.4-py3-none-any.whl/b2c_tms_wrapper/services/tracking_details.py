from http import HTTPStatus
from typing import List

from b2c_tms_wrapper.models import TripTrackingDetails
from b2c_tms_wrapper.timeout import SessionWithTimeOut
from b2c_tms_wrapper.utils import mk_exc


class TripTrackingDetailsService:
    def __init__(self, url: str, session: SessionWithTimeOut):
        self._url = url
        self._session = session

    def get_tracking_details_for_trip(self, trip_id: str) -> TripTrackingDetails:
        response = self._session.get(
            f"{self._url}/api/v1/trips/{trip_id}/tracking_details"
        )

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return TripTrackingDetails.from_dict(response.json()["data"])

    def get_tracking_details_for_trips(
        self, trip_ids: List[str]
    ) -> List[TripTrackingDetails]:
        if not trip_ids:
            return []

        response = self._session.get(
            f"{self._url}/api/v1/trips/tracking_details",
            json={"trip_ids": trip_ids},
        )

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return [
            TripTrackingDetails.from_dict(dikt) if dikt else None
            for dikt in response.json()["data"]
        ]
