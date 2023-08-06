from datetime import datetime
from typing import Optional, List, Dict

from requests import adapters
from shuttl_geo import Location
from shuttl_time import TimeWindow

from b2c_tms_wrapper.models import (
    Trip,
    BoardingMode,
    BookingState,
    BookingRequest,
    TripState,
    TripType,
    TripEvent,
    TripEventType,
    BookingOpeningTime,
    UserJourneyRequest,
    UserJourney,
    TripTrackingDetails,
    TripAllocationAssociation,
    Reservation,
    Booking,
)
from b2c_tms_wrapper.services.booking_history import BookingHistoryService
from b2c_tms_wrapper.services.booking_opening_times import BookingOpeningTimesService
from b2c_tms_wrapper.services.booking_requests import BookingRequestsService
from b2c_tms_wrapper.services.reservations import ReservationsService
from b2c_tms_wrapper.services.tracking_details import TripTrackingDetailsService
from b2c_tms_wrapper.services.trip_events import TripEventsService
from b2c_tms_wrapper.services.user_journeys import UserJourneysService

from b2c_tms_wrapper.timeout import SessionWithTimeOut
from b2c_tms_wrapper.services.trips import TripsService


class B2CTMS:
    def __init__(self, b2c_tms_url: str, session_timeout: int = 30):
        self._b2c_tms_url = b2c_tms_url
        self._session = SessionWithTimeOut(session_timeout)
        adapter = adapters.HTTPAdapter(pool_connections=40, max_retries=3)
        self._session.mount(adapter=adapter, prefix="http://")

        self._trips_service = TripsService(url=self._b2c_tms_url, session=self._session)
        self._trip_events_service = TripEventsService(
            url=self._b2c_tms_url, session=self._session
        )
        self._tracking_details_service = TripTrackingDetailsService(
            url=self._b2c_tms_url, session=self._session
        )
        self._booking_requests_service = BookingRequestsService(
            url=self._b2c_tms_url, session=self._session
        )
        self._booking_history_service = BookingHistoryService(
            url=self._b2c_tms_url, session=self._session
        )
        self._reservations_service = ReservationsService(
            url=self._b2c_tms_url, session=self._session
        )
        self._booking_opening_times_service = BookingOpeningTimesService(
            url=self._b2c_tms_url, session=self._session
        )
        self._user_journeys_service = UserJourneysService(
            url=self._b2c_tms_url, session=self._session
        )

    # Trip Interfaces #

    def create_trip(self, trip_json: Dict) -> Trip:
        return self._trips_service.create_trip(trip_json)

    def get_trip_by_id(self, trip_id: str) -> Optional[Trip]:
        return self._trips_service.get_trip_by_id(trip_id)

    def get_next_trip_for_vehicle(self, vehicle_id: str) -> Optional[Trip]:
        return self._trips_service.get_next_trip_for_vehicle(vehicle_id)

    def get_trips_by_ids(self, trip_ids: List[str]) -> List[Trip]:
        return self._trips_service.get_trips_by_ids(trip_ids)

    def get_trips_by_vehicle_ids(
        self,
        vehicle_ids: List[str],
        time_window: TimeWindow,
        states: List[TripState] = None,
    ) -> List[Trip]:
        return self._trips_service.get_trips_by_vehicle_ids(
            vehicle_ids=vehicle_ids, time_window=time_window, states=states
        )

    def get_trips_by_driver_ids(
        self, driver_ids: List[str], time_window: TimeWindow, states: [str] = None
    ) -> List[Trip]:
        return self._trips_service.get_trips_by_driver_ids(
            driver_ids=driver_ids, time_window=time_window, states=states
        )

    def get_completed_trips(
        self, from_time: datetime, to_time: datetime = None
    ) -> List[Trip]:
        return self._trips_service.get_completed_trips(from_time, to_time)

    def get_trips(
        self,
        route_ids: List[str] = None,
        from_time: datetime = None,
        to_time: datetime = None,
        states: List[TripState] = None,
        types: List[TripType] = None,
    ) -> List[Trip]:
        return self._trips_service.get_trips(
            route_ids=route_ids,
            from_time=from_time,
            to_time=to_time,
            states=states,
            types=types,
        )

    def get_trips_with_tracked_way_points(
        self,
        route_ids: List[str] = None,
        from_time: datetime = None,
        to_time: datetime = None,
        states: List[TripState] = None,
    ) -> List[Trip]:
        return self._trips_service.get_trips_with_tracked_way_points(
            route_ids=route_ids, from_time=from_time, to_time=to_time, states=states
        )

    def get_trips_by_updated_time(
        self, from_time: datetime, states: List[TripState] = None
    ) -> List[Trip]:
        return self._trips_service.get_trips_by_updated_time(
            from_time=from_time, states=states
        )

    def update_vehicle_on_trip(
        self, trip_id: str, current_vehicle_id: str, new_vehicle_id: str
    ) -> Trip:
        return self._trips_service.update_vehicle_on_trip(
            trip_id=trip_id,
            current_vehicle_id=current_vehicle_id,
            new_vehicle_id=new_vehicle_id,
        )

    def detach_vehicle_from_trip(self, trip_id: str) -> Trip:
        return self._trips_service.detach_vehicle_from_trip(trip_id)

    def attach_vehicle_to_trip(self, trip_id: str, vehicle_id: str) -> Trip:
        return self._trips_service.attach_vehicle_to_trip(
            trip_id=trip_id, vehicle_id=vehicle_id
        )

    def cancel_trip(
        self, trip_id: str, trip_state: TripState, generated_by: str, meta_info: Dict
    ) -> Trip:
        return self._trips_service.cancel_trip(
            trip_id=trip_id,
            trip_state=trip_state,
            generated_by=generated_by,
            meta_info=meta_info,
        )

    def get_trip_path(self, trip_id: str) -> List[Location]:
        return self._trips_service.get_trip_path(trip_id)

    def get_trip_paths_in_bulk(self, trip_ids: List[str]) -> Dict[str, List[Location]]:
        return self._trips_service.get_trip_paths_in_bulk(trip_ids)

    def get_trip_reschedule_window(self, trip_id: str) -> TimeWindow:
        return self._trips_service.get_trip_reschedule_window(trip_id)

    def start_trip(
        self,
        trip_id: str,
        reason: str,
        location: Location = None,
        generated_by: str = None,
    ) -> Trip:
        return self._trips_service.start_trip(
            trip_id=trip_id, reason=reason, location=location, generated_by=generated_by
        )

    def end_trip(
        self,
        trip_id: str,
        reason: str,
        location: Location = None,
        generated_by: str = None,
    ) -> Trip:
        return self._trips_service.end_trip(
            trip_id=trip_id, reason=reason, location=location, generated_by=generated_by
        )

    def mark_vehicle_breakdown_for_trip(
        self,
        trip_id: str,
        vehicle_id_on_trip: str,
        updated_by: str,
        reason_info: dict,
        vehicle_id_to_attach: str = None,
    ) -> Trip:
        return self._trips_service.mark_vehicle_breakdown_for_trip(
            trip_id=trip_id,
            vehicle_id_on_trip=vehicle_id_on_trip,
            updated_by=updated_by,
            reason_info=reason_info,
            vehicle_id_to_attach=vehicle_id_to_attach,
        )

    def get_trip_allocation_associations(
        self, after: str = None
    ) -> List[TripAllocationAssociation]:
        return self._trips_service.get_trip_allocation_associations(after)

    def get_trips_with_overlapping_allocations(
        self,
        vehicle_ids: List[str],
        time_window: TimeWindow,
        states: List[TripState] = None,
    ) -> List[Trip]:
        return self._trips_service.get_trips_with_overlapping_allocations(
            vehicle_ids=vehicle_ids, time_window=time_window, states=states
        )

    # Trip Events Interfaces #

    def get_trip_events(self, trip_id: str) -> List[TripEvent]:
        return self._trip_events_service.get_trip_events(trip_id)

    def get_trip_events_by_trip_ids(
        self, trip_ids: List[str], types: List[TripEventType] = None
    ) -> Dict[str, List[TripEvent]]:
        return self._trip_events_service.get_trip_events_by_trip_ids(
            trip_ids=trip_ids, types=types
        )

    def capture_trip_event(
        self,
        trip_id: str,
        type: TripEventType,
        details: Dict,
        generated_at: datetime,
        generated_by: str,
    ) -> List[TripEvent]:
        return self._trip_events_service.capture_trip_event(
            trip_id=trip_id,
            type=type,
            details=details,
            generated_at=generated_at,
            generated_by=generated_by,
        )

    # TripTrackingDetails Interfaces #

    def get_tracking_details_for_trip(self, trip_id: str) -> TripTrackingDetails:
        return self._tracking_details_service.get_tracking_details_for_trip(trip_id)

    def get_tracking_details_for_trips(
        self, trip_ids: List[str]
    ) -> List[TripTrackingDetails]:
        return self._tracking_details_service.get_tracking_details_for_trips(trip_ids)

    # BookingRequest Interfaces #

    def create_booking(
        self,
        user_id: str,
        trip_id: str,
        pickup_stop_id: str,
        drop_stop_id: str,
        booking_request_id: str,
    ) -> BookingRequest:
        return self._booking_requests_service.create_booking(
            user_id=user_id,
            trip_id=trip_id,
            pickup_stop_id=pickup_stop_id,
            drop_stop_id=drop_stop_id,
            booking_request_id=booking_request_id,
        )

    def create_booking_through_reservation(
        self, reservation_id: str, user_id: str
    ) -> BookingRequest:
        return self._booking_requests_service.create_booking_through_reservation(
            reservation_id, user_id
        )

    def get_booking_request_by_mode(
        self, mode: BoardingMode
    ) -> Optional[BookingRequest]:
        return self._booking_requests_service.get_booking_request_by_mode(mode)

    def get_booking_requests_by_ids(self, ids: List[str]) -> List[BookingRequest]:
        return self._booking_requests_service.get_booking_requests_by_ids(ids)

    def get_booking_requests_for_trip(self, trip_id: str) -> List[BookingRequest]:
        return self._booking_requests_service.get_booking_requests_for_trip(trip_id)

    def get_booking_requests_for_trips(
        self, trips_ids: List[str], states: List[BookingState] = None
    ) -> Dict[str, List[BookingRequest]]:
        return self._booking_requests_service.get_booking_requests_for_trips(
            trips_ids=trips_ids, states=states
        )

    def get_booking_requests_for_user(
        self,
        user_id: str,
        from_time: datetime = None,
        to_time: datetime = None,
        states: List[BookingState] = None,
    ) -> List[BookingRequest]:
        return self._booking_requests_service.get_booking_requests_for_user(
            user_id=user_id, from_time=from_time, to_time=to_time, states=states
        )

    def get_cancelled_booking_requests(self, after: str = None) -> List[BookingRequest]:
        return self._booking_requests_service.get_cancelled_booking_requests(after)

    def get_cancelled_booking_requests_by_reasons(
        self,
        cancellation_reasons: List[str],
        after: str = None,
        from_time: str = None,
    ) -> List[BookingRequest]:
        return self._booking_requests_service.get_cancelled_booking_requests_by_reasons(
            cancellation_reasons=cancellation_reasons, after=after, from_time=from_time
        )

    def reschedule_booking(self, booking_id: str, trip_id: str) -> BookingRequest:
        return self._booking_requests_service.reschedule_booking(
            booking_id=booking_id, trip_id=trip_id
        )

    def cancel_booking_by_mode(self, mode: BoardingMode) -> BookingRequest:
        return self._booking_requests_service.cancel_booking_by_mode(mode)

    def board(
        self, trip_id: str, time: datetime, location: Location, mode: BoardingMode
    ) -> BookingRequest:
        return self._booking_requests_service.board(
            trip_id=trip_id, time=time, location=location, mode=mode
        )

    def deboard(
        self, trip_id: str, time: datetime, location: Location, mode: BoardingMode
    ) -> BookingRequest:
        return self._booking_requests_service.deboard(
            trip_id=trip_id, time=time, location=location, mode=mode
        )

    # Booking History Interfaces #

    def get_booking_history_by_booking_request_ids(
        self, booking_request_ids: List[str]
    ) -> List[Booking]:
        return self._booking_history_service.get_booking_history_by_booking_request_ids(
            booking_request_ids
        )

    # Reservation Interfaces #

    def create_reservation(
        self,
        reservation_id: str,
        trip_id: str,
        pickup_stop_id: str,
        drop_stop_id: str,
        expires_at: datetime,
    ) -> Reservation:
        return self._reservations_service.create_reservation(
            reservation_id=reservation_id,
            trip_id=trip_id,
            pickup_stop_id=pickup_stop_id,
            drop_stop_id=drop_stop_id,
            expires_at=expires_at,
        )

    # BookingOpeningTime Interfaces #

    def get_booking_opening_time(self, line_id: str) -> Optional[BookingOpeningTime]:
        return self._booking_opening_times_service.get_booking_opening_time(
            line_id=line_id
        )

    def get_user_journeys(
        self, user_journey_requests: List[UserJourneyRequest], time_window: TimeWindow
    ) -> List[UserJourney]:
        return self._user_journeys_service.get_user_journeys(
            user_journey_requests=user_journey_requests, time_window=time_window
        )
