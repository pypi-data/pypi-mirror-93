import itertools
from http import HTTPStatus
from typing import List

from b2c_tms_wrapper.models import Booking
from b2c_tms_wrapper.timeout import SessionWithTimeOut
from b2c_tms_wrapper.utils import mk_exc


class BookingHistoryService:
    def __init__(self, url: str, session: SessionWithTimeOut):
        self._url = url
        self._session = session

    def get_booking_history_by_booking_request_ids(
        self, booking_request_ids: List[str]
    ) -> List[Booking]:
        if not booking_request_ids:
            return []

        response = self._session.get(
            f"{self._url}/api/v1/booking_history/by_booking_requests",
            json={"booking_request_ids": booking_request_ids},
        )

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return [
            Booking.from_dict(booking)
            for booking in list(itertools.chain.from_iterable(response.json()["data"]))
        ]
