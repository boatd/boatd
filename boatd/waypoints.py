from . import exceptions


class WaypointManager(object):
    def __init__(self, initial_waypoints=None):
        if initial_waypoints is None:
            self.waypoints = []
        self.current = None

    def add_waypoint(self, waypoint):
        if len(waypoint) == 2:
            lat, lon = waypoint
        else:
            raise exceptions.WaypointMalformedError('waypoint is not a tuple '
                                                    'of length two')

        if isinstance(lat, float) and isinstance(lon, float):
            self.waypoints.append(waypoint)
        else:
            raise exceptions.WaypointMalformedError('waypoint is not a tuple '
                                                    'of two floats')

    def add_waypoints(self, waypoints):
        for point in waypoints:
            self.add_waypoint(point)

    def next(self):
        if self.current is not None:
            self.current += 1
            return self.waypoints[self.current]
        else:
            raise exceptions.WaypointsNotLoadedError()

    def current(self):
        if self.current is not None:
            return self.waypoints[self.current]
        else:
            raise exceptions.WaypointsNotLoadedError()

    def previous(self):
        if self.current is not None:
            if self.current > 0:
                return self.waypoints[self.current - 1]
            else:
                return self.waypoints[0]
        else:
            raise exceptions.WaypointsNotLoadedError()
