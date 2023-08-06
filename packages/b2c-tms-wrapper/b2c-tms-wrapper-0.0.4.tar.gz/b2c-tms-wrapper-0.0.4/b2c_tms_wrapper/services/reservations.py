from datetime import datetime
from http import HTTPStatus

from shuttlis.serialization import serialize

from b2c_tms_wrapper.error import NoSeatsAvailable, TripNotFound
from b2c_tms_wrapper.models import Reservation
from b2c_tms_wrapper.timeout import SessionWithTimeOut
from b2c_tms_wrapper.utils import mk_exc


class ReservationsService:
    def __init__(self, url: str, session: SessionWithTimeOut):
        self._url = url
        self._session = session

    def create_reservation(
        self,
        reservation_id: str,
        trip_id: str,
        pickup_stop_id: str,
        drop_stop_id: str,
        expires_at: datetime,
    ) -> Reservation:
        json = {
            "reservation_id": reservation_id,
            "trip_id": trip_id,
            "pickup_stop_id": pickup_stop_id,
            "drop_stop_id": drop_stop_id,
            "expires_at": expires_at,
        }
        response = self._session.post(
            f"{self._url}/api/v1/reservations",
            json=serialize(json),
        )

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise TripNotFound(response.json()["error"]["message"])

        if response.status_code == HTTPStatus.CONFLICT:
            raise NoSeatsAvailable(response.json()["error"]["message"])

        if response.status_code != HTTPStatus.CREATED:
            raise mk_exc(response)

        return Reservation.from_dict(response.json()["data"])
