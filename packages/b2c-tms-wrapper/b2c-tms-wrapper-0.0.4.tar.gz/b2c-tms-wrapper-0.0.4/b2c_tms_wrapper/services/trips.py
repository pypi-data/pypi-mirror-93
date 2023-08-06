from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Optional, List, Dict

from shuttl_geo import Location
from shuttl_time import TimeWindow
from shuttl_time.time import time_now, from_iso_format
from shuttlis.pagination import After
from shuttlis.serialization import serialize
from shuttlis.utils import uuid4_str
from stream_processor.schedulers import ThreadPoolScheduler
from stream_processor.stream import Stream
from stream_processor.tasks import Task

from b2c_tms_wrapper.error import (
    InvalidOperation,
    TripInfoAlreadyExists,
    TripNotFound,
    AllocationConflict,
    VehicleNonOperational,
    VehicleNotAttached,
    TripVehicleMismatch,
)
from b2c_tms_wrapper.models import Trip, TripState, TripType, TripAllocationAssociation
from b2c_tms_wrapper.timeout import SessionWithTimeOut
from b2c_tms_wrapper.utils import auto_paginate, mk_exc


class TripsService:
    def __init__(self, url: str, session: SessionWithTimeOut):
        self._url = url
        self._session = session
        self._thread_pool_scheduler = ThreadPoolScheduler(max_workers=5)
        self._BATCH_SIZE = 25

    def create_trip(self, trip_json: Dict) -> Trip:
        response = self._session.post(f"{self._url}/api/v1/trips", json=trip_json)

        if response.status_code == HTTPStatus.CONFLICT:
            raise TripInfoAlreadyExists(response.json()["error"]["message"])

        if response.status_code == HTTPStatus.BAD_REQUEST:
            raise InvalidOperation(f"Invalid Operation: {response.json()}")

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return Trip.from_dict(response.json()["data"])

    def get_trip_by_id(self, trip_id: str) -> Optional[Trip]:
        response = self._session.get(url=f"{self._url}/api/v1/trips/{trip_id}")

        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return Trip.from_dict(response.json()["data"])

    def get_next_trip_for_vehicle(self, vehicle_id: str) -> Optional[Trip]:
        response = self._session.get(f"{self._url}/api/v1/trips/next/{vehicle_id}")

        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return Trip.from_dict(response.json()["data"])

    def get_trips_by_ids(self, trip_ids: List[str]) -> List[Trip]:
        if not trip_ids:
            return []

        response = self._session.get(
            url=f"{self._url}/api/v1/trips/by_ids", json={"ids": ",".join(trip_ids)}
        )

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return [Trip.from_dict(trip_json) for trip_json in response.json()["data"]]

    def get_trips_by_vehicle_ids(
        self,
        vehicle_ids: List[str],
        time_window: TimeWindow,
        states: List[TripState] = None,
    ) -> List[Trip]:
        if not vehicle_ids:
            return []

        def _get_trips_by_vehicle_ids_for_time_windows(
            vehicle_ids: List[str],
        ) -> List[Trip]:
            params = {
                "vehicle_ids": ",".join(vehicle_ids),
                "from_time": time_window.from_date,
                "to_time": time_window.to_date,
            }
            if states:
                params["states"] = ",".join([state.value for state in states])

            response = self._session.get(
                url=f"{self._url}/api/v1/trips/by_vehicle_ids",
                params=serialize(params),
            )

            if response.status_code != HTTPStatus.OK:
                raise mk_exc(response)

            return [Trip.from_dict(trip_json) for trip_json in response.json()["data"]]

        trips = (
            (
                Stream(vehicle_ids)
                .batch(self._BATCH_SIZE)
                .map(
                    Task(_get_trips_by_vehicle_ids_for_time_windows),
                    scheduler=self._thread_pool_scheduler,
                )
            )
            .concat()
            .list()
        )
        return trips

    def get_trips_by_driver_ids(
        self, driver_ids: List[str], time_window: TimeWindow, states: [str] = None
    ) -> List[Trip]:
        if not driver_ids:
            return []

        params = {
            "driver_ids": ",".join(driver_ids),
            "from_time": time_window.from_date,
            "to_time": time_window.to_date,
        }
        if states:
            params["states"] = ",".join([state.value for state in states])

        response = self._session.get(
            f"{self._url}/api/v1/trips/by_driver_ids", params=params
        )

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return [Trip.from_dict(trip_json) for trip_json in response.json()["data"]]

    def get_trips_by_updated_time(
        self, from_time: datetime, states: List[TripState] = None
    ) -> List[Trip]:
        params = {"from_time": from_time}
        if states:
            params["states"] = ",".join([state.value for state in states])

        trips = auto_paginate(
            session=self._session,
            url=f"{self._url}/api/v1/trips/by_updated_time",
            params=serialize(params),
        )

        return [Trip.from_dict(trip) for trip in trips]

    def get_completed_trips(
        self, from_time: datetime, to_time: datetime = None
    ) -> List[Trip]:
        params = {"from_time": from_time}
        if to_time:
            params["to_time"] = to_time

        trips = auto_paginate(
            session=self._session,
            url=f"{self._url}/api/v1/trips/completed",
            params=serialize(params),
        )

        return [Trip.from_dict(trip) for trip in trips]

    def get_trips(
        self,
        route_ids: List[str] = None,
        from_time: datetime = None,
        to_time: datetime = None,
        states: List[TripState] = None,
        types: List[TripType] = None,
    ) -> List[Trip]:

        params = {}
        if route_ids:
            params["route_ids"] = ",".join(route_ids)
        if from_time:
            params["from_time"] = from_time
        if to_time:
            params["to_time"] = to_time
        if states:
            params["states"] = ",".join([state.value for state in states])
        if types:
            params["types"] = ",".join([type.value for type in types])

        trips = auto_paginate(
            session=self._session,
            url=f"{self._url}/api/v1/trips",
            params=serialize(params),
        )

        return [Trip.from_dict(trip) for trip in trips]

    def get_trips_with_tracked_way_points(
        self,
        route_ids: List[str] = None,
        from_time: datetime = None,
        to_time: datetime = None,
        states: List[TripState] = None,
    ) -> List[Trip]:
        params = {}
        if route_ids:
            params["route_ids"] = ",".join(route_ids)
        if from_time:
            params["from_time"] = from_time
        if to_time:
            params["to_time"] = to_time
        if states:
            params["states"] = ",".join([state.value for state in states])

        trips = auto_paginate(
            session=self._session,
            url=f"{self._url}/api/v2/trips",
            params=serialize(params),
        )

        return [Trip.from_dict(trip) for trip in trips]

    def attach_vehicle_to_trip(self, trip_id: str, vehicle_id: str) -> Trip:
        response = self._session.post(
            f"{self._url}/api/v1/trips/{trip_id}/vehicle", json={"id": vehicle_id}
        )

        if response.status_code == HTTPStatus.BAD_REQUEST:
            if response.json()["error"].get("type") == "VEHICLE_NON_OPERATIONAL":
                raise VehicleNonOperational(response.json()["error"]["message"])
            if response.json()["error"].get("type") == "ALLOCATION_CONFLICT":
                raise AllocationConflict(response.json()["error"]["message"])
            raise InvalidOperation(f"Could not perform operation: {response.json()}")

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return Trip.from_dict(response.json()["data"])

    def update_vehicle_on_trip(
        self, trip_id: str, current_vehicle_id: str, new_vehicle_id: str
    ) -> Trip:
        params = {
            "trip_id": trip_id,
            "from_vehicle_id": current_vehicle_id,
            "to_vehicle_id": new_vehicle_id,
        }
        response = self._session.post(
            f"{self._url}/api/v1/trips/vehicle/update", json=serialize(params)
        )

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise TripNotFound("No trip found for the requested id")

        if response.status_code == HTTPStatus.BAD_REQUEST:
            if response.json()["error"].get("type") == "VEHICLE_NOT_ATTACHED":
                raise VehicleNotAttached(response.json()["error"]["message"])
            if response.json()["error"].get("type") == "TRIP_VEHICLE_MISMATCH":
                raise TripVehicleMismatch(response.json()["error"]["message"])
            raise InvalidOperation(f"Could not perform operation: {response.json()}")

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return Trip.from_dict(response.json()["data"])

    def detach_vehicle_from_trip(self, trip_id: str) -> Trip:
        response = self._session.post(
            f"{self._url}/api/v1/trips/{trip_id}/vehicle/detach"
        )

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return Trip.from_dict(response.json()["data"])

    def cancel_trip(
        self,
        trip_id: str,
        trip_state: TripState,
        generated_by: str,
        meta_info: Dict,
    ) -> Trip:

        json = {
            "from_state": trip_state,
            "meta_info": meta_info,
            "generated_by": generated_by,
            "generated_at": time_now(),
        }
        response = self._session.delete(
            f"{self._url}/api/v1/trips/{trip_id}", json=serialize(json)
        )

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise TripNotFound("No trip found for the requested id")

        if response.status_code == HTTPStatus.BAD_REQUEST:
            raise InvalidOperation(f"Could not perform operation: {response.json()}")

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return Trip.from_dict(response.json()["data"])

    def get_trip_path(self, trip_id: str) -> List[Location]:
        response = self._session.get(f"{self._url}/api/v1/trips/{trip_id}/path")

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise TripNotFound("No trip found for the requested id")

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return [
            Location(lat=location["lat"], lng=location["lng"])
            for location in response.json()["data"]
        ]

    def get_trip_paths_in_bulk(self, trip_ids: List[str]) -> Dict[str, List[Location]]:
        if not trip_ids:
            return {}

        response = self._session.get(
            url=f"{self._url}/api/v1/trips/path", params=",".join(trip_ids)
        )

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        trip_id_vs_path_map = response.json()["data"]
        return {
            trip_id: [
                Location(lat=location["lat"], lng=location["lng"]) for location in path
            ]
            for trip_id, path in trip_id_vs_path_map.items()
        }

    def get_trip_reschedule_window(self, trip_id: str) -> TimeWindow:
        response = self._session.get(
            f"{self._url}/api/v1/trips/{trip_id}/reschedule_window"
        )

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise TripNotFound("No trip found for the requested id")

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        reschedule_window_json = response.json()["data"]
        return TimeWindow(
            from_date=from_iso_format(reschedule_window_json["from_date"]),
            to_date=from_iso_format(reschedule_window_json["to_date"]),
        )

    def start_trip(
        self,
        trip_id: str,
        reason: str,
        location: Location = None,
        generated_by: str = None,
    ) -> Trip:
        json = {"meta_info": {"reason": reason}, "generated_by": generated_by}
        if location:
            json["meta_info"]["location"] = {"lat": location.lat, "lng": location.lng}

        response = self._session.patch(
            f"{self._url}/api/v1/trips/{trip_id}/start", json=serialize(json)
        )

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise TripNotFound("No trip found for the requested id")

        if response.status_code == HTTPStatus.BAD_REQUEST:
            raise InvalidOperation(f"Invalid operation: {response.json()}")

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return Trip.from_dict(response.json()["data"])

    def end_trip(
        self,
        trip_id: str,
        reason: str,
        generated_by: str,
        location: Location = None,
    ) -> Trip:
        json = {"meta_info": {"reason": reason}, "generated_by": generated_by}
        if location:
            json["meta_info"]["location"] = {"lat": location.lat, "lng": location.lng}

        response = self._session.patch(
            f"{self._url}/api/v1/trips/{trip_id}/end", json=serialize(json)
        )

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise TripNotFound("No trip found for the requested id")

        if response.status_code == HTTPStatus.BAD_REQUEST:
            raise InvalidOperation(f"Invalid operation: {response.json()}")

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return Trip.from_dict(response.json()["data"])

    def mark_vehicle_breakdown_for_trip(
        self,
        trip_id: str,
        vehicle_id_on_trip: str,
        updated_by: str,
        reason_info: dict,
        vehicle_id_to_attach: str = None,
    ) -> Trip:
        json = {
            "updated_by": updated_by,
            "reason_info": reason_info,
            "vehicle_id_on_trip": vehicle_id_on_trip,
        }
        if vehicle_id_to_attach:
            json["vehicle_id_to_attach"] = vehicle_id_to_attach

        response = self._session.post(
            f"{self._url}/api/v1/trips/{trip_id}/mark_vehicle_breakdown",
            json=serialize(json),
        )

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return Trip.from_dict(response.json()["data"])

    def get_trip_allocation_associations(
        self, after: str = None
    ) -> List[TripAllocationAssociation]:
        if not after:
            after = str(After(id=uuid4_str(), date=time_now() + timedelta(hours=1)))
        trip_allocation_associations = auto_paginate(
            session=self._session,
            url=f"{self._url}/api/v1/trips/allocation_associations",
            after=after,
        )

        return [
            TripAllocationAssociation.from_dict(association)
            for association in trip_allocation_associations
        ]

    def get_trips_with_overlapping_allocations(
        self,
        vehicle_ids: List[str],
        time_window: TimeWindow,
        states: List[TripState] = None,
    ) -> List[Trip]:
        if not vehicle_ids:
            return []

        json = {
            "vehicle_schedules": [
                {
                    "vehicle_id": vehicle_id,
                    "time_windows": [
                        {
                            "from_time": time_window.from_date,
                            "to_time": time_window.to_date,
                        }
                    ],
                }
                for vehicle_id in vehicle_ids
            ]
        }
        if states:
            json["states"] = states

        response = self._session.get(
            f"{self._url}/api/v1/trips/overlapping_allocations", json=serialize(json)
        )

        if response.status_code != HTTPStatus.OK:
            raise mk_exc(response)

        return [Trip.from_dict(trip) for trip in response.json()["data"]]
