import random
from datetime import timedelta

from shuttl_geo import Location
from shuttl_time.time import time_now
from shuttlis.utils import uuid4_str

from b2c_tms_wrapper.models import (
    Trip,
    TripEventType,
    BoardingMode,
    UserJourneyRequest,
    TripState,
)


def random_location() -> Location:
    lat = random.uniform(-90, 90)
    lng = random.uniform(-180, 180)
    return Location(lat, lng)


def boarding_mode_dm(id: str = None, type: str = None) -> BoardingMode:
    return BoardingMode(id=id or uuid4_str(), type=type or "MANUAL")


def trip_dm() -> Trip:
    return Trip.from_dict(trip_api_v1_response())


def user_journey_request_dm(
    route_id: str = None, from_stop_id: str = None, to_stop_id: str = None
) -> UserJourneyRequest:
    return UserJourneyRequest(
        route_id=route_id or uuid4_str(),
        from_stop_id=from_stop_id or uuid4_str(),
        to_stop_id=to_stop_id or uuid4_str(),
    )


def trip_api_v1_response() -> dict:
    return {
        "allocation": {
            "id": "a39c16a5-e362-4ba3-8199-9c31bb1c3f8a",
            "type": "allocation",
        },
        "booking_opening_time": "2020-06-22T02:30:00+00:00",
        "bookings": {"type": "bookings"},
        "created_at": "2020-06-23T18:31:29.726233+00:00",
        "departures": {"type": "departures"},
        "driver": None,
        "escort": None,
        "helper": None,
        "id": "259cc1b8-5a86-4e1b-be44-2954f6ec7c49",
        "max_bookings": 20,
        "path": {"type": "path"},
        "route": {"id": "4a2a0e8d-ee20-4cf8-9827-94e8f52c4af3", "type": "route"},
        "start_time": "2020-06-25T16:50:00+00:00",
        "state": "PLANNED",
        "type": "AUTOMATIC",
        "updated_at": "2020-06-23T18:31:29.726233+00:00",
        "vehicle": {"id": "d824dbd6-3036-41f6-9d1e-25ea710b9d27", "type": "vehicle"},
        "way_points": [
            {
                "departure_time": "2020-06-25T16:50:00+00:00",
                "id": "8bca0e6f-b4c1-4002-abd1-e9b3ce88cfe2",
                "stop": {
                    "id": "5752b57f-fd85-4c3a-9f67-6b1f30e2e7d4",
                    "location": {"lat": 28.58368506583371, "lng": 77.21241725488308},
                },
                "type": "PICKUP",
            },
            {
                "departure_time": "2020-06-25T16:56:00+00:00",
                "id": "caf9b191-8660-4cfe-9e88-d64267369f7e",
                "stop": {
                    "id": "c8894713-07a8-4bb0-bb49-219f545bc377",
                    "location": {"lat": 28.56636061941184, "lng": 77.20755711353199},
                },
                "type": "DROP",
            },
        ],
    }


def trip_api_v2_response() -> dict:
    return {
        "booking_opening_time": "2020-04-11T18:30:00+00:00",
        "driver": None,
        "id": "039601aa-3608-419a-9b8d-b60fd8c80105",
        "max_bookings": 20,
        "route": {"id": "22f1ccd6-e7b8-4426-b67a-4c74009b8c80", "type": "route"},
        "start_time": "2020-04-13T05:30:00+00:00",
        "state": "PLANNED",
        "vehicle": {
            "id": "d824dbd6-3036-41f6-9d1e-25ea710b9d27",
            "registration_number": "30-3456",
        },
        "way_points": [
            {
                "departed_at": None,
                "estimated_departure_time": "2020-04-13T05:30:00+00:00",
                "id": "b92a30d4-8f61-45e5-8038-fb76c9c43541",
                "stop": {
                    "id": "e8d614eb-fd76-4ba5-b6ea-943a10b2fd5b",
                    "location": {"lat": 19.1176, "lng": 72.906},
                },
                "type": "PICKUP",
            },
            {
                "departed_at": None,
                "estimated_departure_time": "2020-04-13T05:31:00+00:00",
                "id": "4d44ea74-24d3-4e69-bf78-348e521b24e0",
                "stop": {
                    "id": "58ad12c1-12fb-49f7-9c32-11c2491ff7fa",
                    "location": {"lat": 19.1364, "lng": 72.8296},
                },
                "type": "DROP",
            },
        ],
    }


def trip_event_api_response(
    trip_id: str = None,
    type: TripEventType = None,
    reason: str = None,
) -> dict:
    return {
        "created_at": time_now().isoformat(),
        "details": {
            "from_state": "PLANNED",
            "reason": reason or "Network Issue",
            "state": "ACTIVE",
        },
        "generated_at": time_now().isoformat(),
        "generated_by": uuid4_str(),
        "id": uuid4_str(),
        "trip_id": trip_id or uuid4_str(),
        "type": type.value if type else "ACTIVE",
    }


def trip_tracking_details_response(trip_id: str = None) -> dict:
    now = time_now()
    return {
        "eta_updated_at": now.isoformat(),
        "state": TripState.ACTIVE.value,
        "trip_id": trip_id or uuid4_str(),
        "upcoming_stop_distance": [
            {
                "distance": 966.2422425849713,
                "stop_id": "b40d7717-7eb5-41a1-ac10-86d364b92580",
            },
            {
                "distance": 1626.2383488940982,
                "stop_id": "dfc929f6-e42e-4d1d-86fd-6e5e0052529b",
            },
            {
                "distance": 2598.744995749665,
                "stop_id": "9f1bc76a-a09c-477a-a01d-1c3c2dd00737",
            },
        ],
        "vehicle": {
            "id": "4d7e8ac0-b95b-427a-93d0-d4fd8ce20495",
            "location": {"lat": 28.57556, "lng": 77.1443},
            "updated_at": now.isoformat(),
        },
        "way_points": [
            {
                "departed_at": (now - timedelta(minutes=5)).isoformat(),
                "stop": {
                    "id": "1c18d284-3fb8-490d-aacb-1a340005b3bf",
                    "location": {"lat": 28.57556540465579, "lng": 77.14430331449142},
                },
                "type": "PICKUP",
            },
            {
                "estimated_departure_time": (now + timedelta(minutes=5)).isoformat(),
                "stop": {
                    "id": "b40d7717-7eb5-41a1-ac10-86d364b92580",
                    "location": {"lat": 28.57488177654272, "lng": 77.15459673513308},
                },
                "type": "PICKUP",
            },
            {
                "estimated_departure_time": (now + timedelta(minutes=10)).isoformat(),
                "stop": {
                    "id": "dfc929f6-e42e-4d1d-86fd-6e5e0052529b",
                    "location": {"lat": 28.57496289468635, "lng": 77.16007098032235},
                },
                "type": "PICKUP",
            },
            {
                "estimated_departure_time": (now + timedelta(minutes=20)).isoformat(),
                "stop": {
                    "id": "9f1bc76a-a09c-477a-a01d-1c3c2dd00737",
                    "location": {"lat": 28.56757537851266, "lng": 77.16540360355837},
                },
                "type": "PICKUP",
            },
        ],
    }


def trip_allocation_association_response(trip_id: str = None) -> dict:
    return {
        "trip_id": trip_id or uuid4_str(),
        "allocation_id": uuid4_str(),
        "created_at": "2020-08-16T11:34:12.548540",
        "updated_at": "2020-08-16T11:34:12.481778+00:00",
    }


def booking_request_api_response(trip_id: str = None) -> dict:
    return {
        "id": uuid4_str(),
        "user": {"id": uuid4_str(), "type": "user"},
        "modes": [{"type": "MANUAL", "id": uuid4_str()}],
        "created_at": "2020-04-13T05:30:00+00:00",
        "updated_at": "2020-04-13T05:30:00+00:00",
        "booking": {
            "pickup_stop": {"id": uuid4_str(), "type": "stop"},
            "drop_stop": {"id": uuid4_str(), "type": "stop"},
            "trip": {"id": trip_id or uuid4_str(), "type": "trip"},
            "boarding_time": "2020-04-13T08:30:00+00:00",
            "status": "CONFIRMED",
            "cancellation_reason": None,
            "cancelled_at": None,
            "created_at": "2020-04-13T05:30:00+00:00",
            "updated_at": "2020-04-13T05:30:00+00:00",
            "boarding_info": None,
            "deboarding_info": None,
            "vehicle": {"id": uuid4_str(), "type": "vehicle"},
        },
        "missed_bookings_count": 0,
    }


def reservation_api_response() -> dict:
    return {
        "id": uuid4_str(),
        "pickup_stop_id": uuid4_str(),
        "drop_stop_id": uuid4_str(),
        "seat_id": uuid4_str(),
        "trip_id": uuid4_str(),
        "created_at": "2021-01-22T12:01:15.667443+00:00",
        "expires_at": "2021-01-22T12:06:15.565689+00:00",
        "is_deleted": True,
        "seat_constraints": [],
    }


def booking_history_api_response(
    trip_id: str = None, booking_request_id: str = None
) -> dict:
    return {
        "boarding_info": {
            "location": {"lat": 13.7658117, "lng": 100.537684},
            "mode": {"id": "1100025253", "type": "MANUAL"},
            "time": "2021-01-21T12:01:21.286842+00:00",
        },
        "boarding_time": "2021-01-21T12:01:00+00:00",
        "boarding_time_window": {
            "end": "2021-01-21T12:01:00+00:00",
            "start": "2021-01-21T12:01:00+00:00",
        },
        "booking_request_id": booking_request_id or uuid4_str(),
        "cancellation_reason": None,
        "created_at": "2021-01-21T12:01:09.536110+00:00",
        "deboarding_info": None,
        "drop_stop": {"id": uuid4_str(), "type": "stop"},
        "modes": [
            {"id": "1100025253", "type": "CHIRP"},
            {"id": "1100025253", "type": "MANUAL"},
        ],
        "pickup_stop": {"id": uuid4_str(), "type": "stop"},
        "status": "CONFIRMED",
        "trip": {"id": trip_id or uuid4_str(), "type": "trip"},
        "updated_at": "2021-01-21T12:01:09.536110+00:00",
    }


def booking_opening_time_api_response(line_id: str) -> dict:
    return {
        "days_before_booking": 2,
        "line_id": line_id or uuid4_str(),
        "time_of_day": {"time": 2130, "timezone": "Asia/Calcutta"},
    }


def user_journey_response() -> dict:
    return {
        "trip_id": uuid4_str(),
        "route": {"id": uuid4_str()},
        "start_time_window": {
            "start": "2020-10-04T14:38:11.020866+05:30",
            "end": "2020-10-04T14:38:11.020866+05:30",
        },
        "vehicle": {"id": uuid4_str(), "type": "vehicle"},
        "total_seats": 20,
        "available_seats": 15,
        "from_way_point": {
            "id": uuid4_str(),
            "stop": {
                "id": uuid4_str(),
                "location": {"lat": 89.23423, "lng": 78.23423},
            },
            "departure_time_window": {
                "start": "2020-10-04T14:38:11.020866+05:30",
                "end": "2020-10-04T14:38:11.020866+05:30",
            },
            "type": "PICKUP",
        },
        "to_way_point": {
            "id": uuid4_str(),
            "stop": {
                "id": uuid4_str(),
                "location": {"lat": 89.23423412342, "lng": 78.23423482343},
            },
            "departure_time_window": {
                "start": "2020-10-04T14:38:11.020866+05:30",
                "end": "2020-10-04T14:38:11.020866+05:30",
            },
            "type": "DROP",
        },
    }


def rebook_card_response() -> dict:
    return {
        "user_id": uuid4_str(),
        "from_stop_id": uuid4_str(),
        "to_stop_id": uuid4_str(),
        "session": "MORNING",
    }
