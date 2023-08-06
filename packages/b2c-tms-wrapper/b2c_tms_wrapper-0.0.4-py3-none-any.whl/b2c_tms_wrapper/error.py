class TripNotFound(Exception):
    pass


class BookingNotFound(Exception):
    pass


class BookingNotFoundOnTrip(Exception):
    pass


class InvalidOperation(Exception):
    pass


class TripInfoAlreadyExists(Exception):
    pass


class VehicleNonOperational(Exception):
    pass


class AllocationConflict(Exception):
    pass


class VehicleNotAttached(Exception):
    pass


class TripVehicleMismatch(Exception):
    pass


class NotAtLocation(Exception):
    pass


class EarlyForEventAction(Exception):
    pass


class BookingAlreadyExists(Exception):
    pass


class NoSeatsAvailable(Exception):
    pass


class CancellationNotAllowedForMissedBooking(Exception):
    pass


class CancellationNotAllowedForBoardedBooking(Exception):
    pass


class ResourceNotFound(Exception):
    pass


class ReservationAlreadyConsumed(Exception):
    pass
