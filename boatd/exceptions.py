class BoatdError(Exception):
    pass


class WaypointsNotLoadedError(BoatdError):
    pass


class WaypointMalformedError(BoatdError):
    pass
