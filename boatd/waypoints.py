# This file is part of boatd, the Robotic Sailing Boat Daemon.
#
# Copyright (C) 2013-2017 Louis Taylor <louis@kragniz.eu>
#
# boatd is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# boatd is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

from . import exceptions

log = logging.getLogger(__name__)


class WaypointManager(object):
    def __init__(self, initial_waypoints=None, home_position=None):
        if initial_waypoints is None:
            self.waypoints = []
        self.current = None
        self.home_position = home_position

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
        log.info('Loaded waypoints: {}'.format(waypoints))
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
