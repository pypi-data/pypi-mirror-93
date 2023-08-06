from http import HTTPStatus

import pytest
import responses

from b2c_tms_wrapper.error import NoSeatsAvailable, TripNotFound
from b2c_tms_wrapper.models import Reservation
from b2c_tms_wrapper.services.b2c_tms import B2CTMS
from tests.factories import reservation_api_response


fake_b2c_tms_url = "http://b2c_tms"
b2c_tms = B2CTMS(b2c_tms_url=fake_b2c_tms_url)


@responses.activate
def test_create_reservation_is_successful():
    reservation_json = reservation_api_response()
    reservation = Reservation.from_dict(reservation_json)

    responses.add(
        responses.POST,
        url=f"{fake_b2c_tms_url}/api/v1/reservations",
        status=HTTPStatus.CREATED,
        json={"data": reservation_json},
    )

    result = b2c_tms.create_reservation(
        reservation_id=reservation.id,
        trip_id=reservation.trip_id,
        pickup_stop_id=reservation.pickup_stop_id,
        drop_stop_id=reservation.drop_stop_id,
        expires_at=reservation.expires_at,
    )
    assert result == reservation


@responses.activate
def test_create_reservation_raises_runtime_error_when_trip_not_found():
    reservation_json = reservation_api_response()
    reservation = Reservation.from_dict(reservation_json)

    responses.add(
        responses.POST,
        url=f"{fake_b2c_tms_url}/api/v1/reservations",
        status=HTTPStatus.NOT_FOUND,
        json={
            "error": {
                "type": "RESOURCE_NOT_FOUND",
                "message": f"Trip {reservation.trip_id} not found",
            }
        },
    )

    with pytest.raises(TripNotFound):
        b2c_tms.create_reservation(
            reservation_id=reservation.id,
            trip_id=reservation.trip_id,
            pickup_stop_id=reservation.pickup_stop_id,
            drop_stop_id=reservation.drop_stop_id,
            expires_at=reservation.expires_at,
        )


@responses.activate
def test_create_reservation_raises_runtime_error_when_no_seats_available():
    reservation_json = reservation_api_response()
    reservation = Reservation.from_dict(reservation_json)

    responses.add(
        responses.POST,
        url=f"{fake_b2c_tms_url}/api/v1/reservations",
        status=HTTPStatus.CONFLICT,
        json={
            "error": {
                "type": "NO_SEATS_AVAILABLE",
                "message": "No seats available",
            }
        },
    )

    with pytest.raises(NoSeatsAvailable):
        b2c_tms.create_reservation(
            reservation_id=reservation.id,
            trip_id=reservation.trip_id,
            pickup_stop_id=reservation.pickup_stop_id,
            drop_stop_id=reservation.drop_stop_id,
            expires_at=reservation.expires_at,
        )


@responses.activate
def test_create_reservation_raises_runtime_error_when_status_is_internal_error():
    reservation_json = reservation_api_response()
    reservation = Reservation.from_dict(reservation_json)

    responses.add(
        responses.POST,
        url=f"{fake_b2c_tms_url}/api/v1/reservations",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    with pytest.raises(RuntimeError):
        b2c_tms.create_reservation(
            reservation_id=reservation.id,
            trip_id=reservation.trip_id,
            pickup_stop_id=reservation.pickup_stop_id,
            drop_stop_id=reservation.drop_stop_id,
            expires_at=reservation.expires_at,
        )
