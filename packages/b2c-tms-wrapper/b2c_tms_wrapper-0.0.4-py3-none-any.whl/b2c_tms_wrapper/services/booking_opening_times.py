from http import HTTPStatus
from typing import Optional

from b2c_tms_wrapper.models import BookingOpeningTime
from b2c_tms_wrapper.timeout import SessionWithTimeOut
from b2c_tms_wrapper.utils import mk_exc


class BookingOpeningTimesService:
    def __init__(self, url: str, session: SessionWithTimeOut):
        self._url = url
        self._session = session

    def get_booking_opening_time(self, line_id: str) -> Optional[BookingOpeningTime]:
        response = self._session.get(
            f"{self._url}/api/v1/booking_opening_times/{line_id}"
        )

        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return BookingOpeningTime.from_dict(response.json()["data"])
