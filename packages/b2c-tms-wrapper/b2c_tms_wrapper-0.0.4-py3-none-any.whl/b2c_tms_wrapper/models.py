from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List

import pytz
from shuttl_geo import Location
from shuttl_time import TimeWindow
from shuttl_time.time import from_iso_format, maybe_datetime_from_iso_format
from shuttlis.time import MilitaryTime
from shuttlis.utils import one_or_none, next_or_none


class BookingState(Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class TripState(Enum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class TripType(Enum):
    MANUAL = "MANUAL"
    AUTOMATIC = "AUTOMATIC"
    DRY_RUN = "DRY_RUN"


@dataclass
class Vehicle:
    id: str
    registration_number: str

    @classmethod
    def from_dict(cls, dikt: dict) -> "Vehicle":
        return cls(id=dikt["id"], registration_number=dikt.get("registration_number"))


@dataclass
class Stop:
    id: str
    location: Optional[Location] = None

    @classmethod
    def from_dict(self, dikt: dict) -> "Stop":
        return Stop(
            id=dikt["id"],
            location=Location(**dikt["location"]) if dikt.get("location") else None,
        )


@dataclass
class TripTrackedWayPoint:
    stop: Stop
    estimated_departure_time: datetime
    departed_at: Optional[datetime]

    @classmethod
    def from_dict(self, dikt: dict) -> "TripTrackedWayPoint":
        estimated_departure_time = maybe_datetime_from_iso_format(
            dikt.get("estimated_departure_time")
        )
        static_departure_time = maybe_datetime_from_iso_format(
            dikt.get("departure_time")
        )
        return TripTrackedWayPoint(
            stop=Stop.from_dict(dikt["stop"]),
            estimated_departure_time=estimated_departure_time or static_departure_time,
            departed_at=maybe_datetime_from_iso_format(dikt.get("departed_at")),
        )

    @property
    def stop_id(self) -> str:
        return self.stop.id

    @property
    def location(self) -> Location:
        return self.stop.location

    @property
    def is_departed(self) -> bool:
        return self.departed_at is not None

    @property
    def departure_time(self) -> datetime:
        return self.departed_at or self.estimated_departure_time


@dataclass
class Trip:
    id: str
    route_id: str
    start_time: datetime
    state: TripState
    max_bookings: int
    vehicle: Optional[Vehicle]
    way_points: List[TripTrackedWayPoint]

    @classmethod
    def from_dict(cls, dikt: dict) -> "Trip":
        return cls(
            id=dikt["id"],
            route_id=dikt["route"]["id"],
            state=TripState(dikt["state"]),
            start_time=from_iso_format(dikt["start_time"]),
            max_bookings=int(dikt["max_bookings"]),
            vehicle=Vehicle.from_dict(dikt["vehicle"]) if dikt["vehicle"] else None,
            way_points=[
                TripTrackedWayPoint.from_dict(way_point)
                for way_point in dikt["way_points"]
            ],
        )

    @property
    def departure_time_for_first_stop(self) -> datetime:
        return self.way_points[0].estimated_departure_time

    @property
    def vehicle_id(self) -> str:
        return self.vehicle.id if self.vehicle else None


@dataclass
class UpcomingStopDistance:
    stop_id: str
    distance: float

    @classmethod
    def from_dict(cls, dikt: dict) -> "UpcomingStopDistance":
        return cls(stop_id=dikt["stop_id"], distance=dikt["distance"])


@dataclass
class TripTrackingDetails:
    trip_id: str
    way_points: List[TripTrackedWayPoint]
    state: TripState
    vehicle: Optional[Vehicle]
    upcoming_stop_distance: Optional[List[UpcomingStopDistance]]

    @classmethod
    def from_dict(cls, dikt: dict) -> "TripTrackingDetails":
        return cls(
            trip_id=dikt["trip_id"],
            vehicle=Vehicle.from_dict(dikt["vehicle"]) if dikt["vehicle"] else None,
            way_points=[
                TripTrackedWayPoint.from_dict(wp_dikt) for wp_dikt in dikt["way_points"]
            ],
            state=TripState[dikt["state"]],
            upcoming_stop_distance=[
                UpcomingStopDistance.from_dict(usd)
                for usd in dikt.get("upcoming_stop_distance", [])
            ],
        )

    @property
    def trip_start_time(self) -> datetime:
        return self.way_points[0].departure_time

    @property
    def stop_ids(self) -> List[str]:
        return [wp.stop_id for wp in self.way_points]

    def _waypoint_details_by_stop_id(self, stop_id: str) -> TripTrackedWayPoint:
        return one_or_none(self.way_points, lambda w: w.stop_id == stop_id)

    def has_departed_from(self, stop_id: str) -> bool:
        return self._waypoint_details_by_stop_id(stop_id).is_departed

    def departure_time_for_stop(self, stop_id: str) -> datetime:
        return self._waypoint_details_by_stop_id(stop_id).departure_time

    def location_for_stop(self, stop_id: str) -> Location:
        return self._waypoint_details_by_stop_id(stop_id).location

    def distance_to_pickup(self, pickup_stop_id: str) -> Optional[int]:
        pickup_stop_distance = next_or_none(
            self.upcoming_stop_distance, lambda usd: usd.stop_id == pickup_stop_id
        )
        return int(pickup_stop_distance.distance) if pickup_stop_distance else None


@dataclass
class TripAllocationAssociation:
    trip_id: str
    allocation_id: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dict(cls, dikt: dict) -> "TripAllocationAssociation":
        return cls(
            trip_id=dikt["trip_id"],
            allocation_id=dikt["allocation_id"],
            created_at=from_iso_format(dikt["created_at"]),
            updated_at=from_iso_format(dikt["updated_at"]),
        )


@dataclass
class BoardingMode:
    type: str
    id: str

    @classmethod
    def from_dict(cls, dikt: dict) -> "BoardingMode":
        return cls(id=dikt["id"], type=dikt["type"])


@dataclass
class Booking:
    booking_request_id: str
    trip_id: str
    pickup_stop_id: str
    drop_stop_id: str
    status: BookingState
    modes: List[BoardingMode]
    created_at: datetime
    updated_at: datetime
    boarding_time: Optional[datetime]
    boarding_info: Optional[dict]
    deboarding_info: Optional[dict]
    cancellation_reason: Optional[str]

    @classmethod
    def from_dict(cls, dikt: dict) -> "Booking":
        return cls(
            booking_request_id=dikt.get("booking_request_id"),
            trip_id=dikt["trip"]["id"],
            pickup_stop_id=dikt["pickup_stop"]["id"],
            drop_stop_id=dikt["drop_stop"]["id"],
            status=BookingState(dikt["status"]),
            modes=[BoardingMode.from_dict(mode) for mode in dikt.get("modes", [])],
            boarding_time=maybe_datetime_from_iso_format(dikt["boarding_time"]),
            created_at=from_iso_format(dikt["created_at"]),
            updated_at=from_iso_format(dikt["updated_at"]),
            boarding_info=dikt["boarding_info"],
            deboarding_info=dikt["deboarding_info"],
            cancellation_reason=dikt["cancellation_reason"],
        )


@dataclass
class BookingRequest:
    id: str
    user_id: str
    modes: List[BoardingMode]
    booking: Booking
    created_at: datetime
    updated_at: datetime
    missed_bookings_count: Optional[int]

    @classmethod
    def from_dict(cls, dikt: dict) -> "BookingRequest":
        return BookingRequest(
            id=dikt["id"],
            user_id=dikt["user"]["id"],
            modes=[BoardingMode.from_dict(mode) for mode in dikt["modes"]],
            booking=Booking.from_dict(dikt["booking"]),
            missed_bookings_count=dikt.get("missed_bookings_count"),
            created_at=from_iso_format(dikt["created_at"]),
            updated_at=from_iso_format(dikt["updated_at"]),
        )

    @property
    def is_boarded(self) -> bool:
        return bool(self.booking.boarding_info)

    @property
    def trip_id(self) -> str:
        return self.booking.trip_id


@dataclass()
class Reservation:
    id: str
    trip_id: str
    pickup_stop_id: str
    drop_stop_id: str
    expires_at: datetime
    created_at: datetime
    is_deleted: bool
    seat_id: str

    @classmethod
    def from_dict(cls, dikt: dict) -> "Reservation":
        return cls(
            id=dikt["id"],
            trip_id=dikt["trip_id"],
            pickup_stop_id=dikt["pickup_stop_id"],
            drop_stop_id=dikt["drop_stop_id"],
            expires_at=from_iso_format(dikt["expires_at"]),
            created_at=from_iso_format(dikt["created_at"]),
            is_deleted=bool(dikt["is_deleted"]),
            seat_id=dikt["seat_id"],
        )


class TripEventType(Enum):
    BOARDING_ALLOWED = "BOARDING_ALLOWED"
    REACHED = "REACHED"
    REPORTED = "REPORTED"
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    VEHICLE_SWAP = "VEHICLE_SWAP"
    CONSISTENCY_CHECK = "CONSISTENCY_CHECK"
    VEHICLE_UPDATE = "VEHICLE_UPDATE"


@dataclass
class TripEvent:
    id: str
    trip_id: str
    generated_by: str
    generated_at: datetime
    type: TripEventType
    details: dict
    created_at: datetime

    @classmethod
    def from_dict(cls, dikt: dict) -> "TripEvent":
        return cls(
            id=dikt["id"],
            trip_id=dikt["trip_id"],
            generated_by=dikt["generated_by"],
            generated_at=from_iso_format(dikt["generated_at"]),
            details=dikt["details"],
            type=TripEventType(dikt["type"]),
            created_at=from_iso_format(dikt["created_at"]),
        )


@dataclass
class BookingOpeningTime:
    line_id: str
    days_before_booking: int
    time_of_day: MilitaryTime

    @classmethod
    def from_dict(cls, dikt: dict) -> "BookingOpeningTime":
        return cls(
            line_id=dikt["line_id"],
            days_before_booking=dikt["days_before_booking"],
            time_of_day=MilitaryTime(
                time=dikt["time_of_day"]["time"],
                tzinfo=pytz.timezone(dikt["time_of_day"]["timezone"]),
            ),
        )

    @property
    def tz(self) -> pytz.tzinfo:
        return self.time_of_day.tz

    def for_(self, dt: datetime) -> datetime:
        tz_dt = dt.astimezone(self.tz)
        tz_dt -= timedelta(days=self.days_before_booking)
        return self.time_of_day.combine(tz_dt.date()).astimezone(pytz.utc)


@dataclass
class UserJourneyRequest:
    route_id: str
    from_stop_id: str
    to_stop_id: str


@dataclass
class WayPoint:
    id: str
    stop: Stop
    departure_time_window: TimeWindow

    @classmethod
    def from_dict(cls, dikt: dict) -> "WayPoint":
        return cls(
            id=dikt["id"],
            stop=Stop.from_dict(dikt["stop"]),
            departure_time_window=TimeWindow(
                from_date=from_iso_format(dikt["departure_time_window"]["start"]),
                to_date=from_iso_format(dikt["departure_time_window"]["end"]),
            ),
        )


@dataclass
class UserJourney:
    trip_id: str
    route_id: str
    start_time_window: TimeWindow
    vehicle_id: str
    total_seats: int
    available_seats: int
    from_way_point: WayPoint
    to_way_point: WayPoint

    @classmethod
    def from_dict(cls, dikt: dict) -> "UserJourney":
        return cls(
            trip_id=dikt["trip_id"],
            route_id=dikt["route"]["id"],
            start_time_window=TimeWindow(
                from_date=from_iso_format(dikt["start_time_window"]["start"]),
                to_date=from_iso_format(dikt["start_time_window"]["end"]),
            ),
            vehicle_id=dikt["vehicle"]["id"] if dikt.get("vehicle") else None,
            total_seats=dikt["total_seats"],
            available_seats=dikt["available_seats"],
            from_way_point=WayPoint.from_dict(dikt["from_way_point"]),
            to_way_point=WayPoint.from_dict(dikt["to_way_point"]),
        )


class Session(Enum):
    MORNING = "MORNING"
    EVENING = "EVENING"
