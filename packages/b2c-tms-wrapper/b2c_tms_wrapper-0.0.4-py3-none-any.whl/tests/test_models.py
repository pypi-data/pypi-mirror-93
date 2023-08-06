from b2c_tms_wrapper.models import TripTrackingDetails
from tests.factories import trip_tracking_details_response


class TestTripTrackingDetails:
    def test_has_departed_from(self):
        tracking_details = TripTrackingDetails.from_dict(
            trip_tracking_details_response()
        )
        stop_ids = tracking_details.stop_ids
        assert tracking_details.has_departed_from(stop_ids[0]) is True
        assert tracking_details.has_departed_from(stop_ids[1]) is False

    def test_departure_time_for_stop(self):
        tracking_details = TripTrackingDetails.from_dict(
            trip_tracking_details_response()
        )
        stop_ids = tracking_details.stop_ids

        result = tracking_details.departure_time_for_stop(stop_ids[0])
        assert result == tracking_details.way_points[0].departure_time

    def test_location_for_stop(self):
        tracking_details = TripTrackingDetails.from_dict(
            trip_tracking_details_response()
        )
        stop_ids = tracking_details.stop_ids
        stop_1_location = tracking_details.way_points[0].location
        stop_2_location = tracking_details.way_points[1].location
        assert tracking_details.location_for_stop(stop_ids[0]) == stop_1_location
        assert tracking_details.location_for_stop(stop_ids[1]) == stop_2_location

    def test_distance_to_pickup(self):
        tracking_details = TripTrackingDetails.from_dict(
            trip_tracking_details_response()
        )
        stop_ids = tracking_details.stop_ids
        assert tracking_details.distance_to_pickup(stop_ids[0]) is None
        assert tracking_details.distance_to_pickup(stop_ids[1]) == int(
            tracking_details.upcoming_stop_distance[0].distance
        )
