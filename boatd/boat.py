# This file is part of boatd, the Robotic Sailing Boat Daemon.
#
# Copyright (C) 2013-2016 Louis Taylor <louis@kragniz.eu>
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

log = logging.getLogger(__name__)


class Boat(object):
    '''The boat itself. Most of the work is done by the active driver'''
    def __init__(self, driver):
        self.driver = driver
        self.active = False

    def __getattr__(self, name):
        '''Return the requested attribute from the currently loaded driver'''
        return self.driver.handlers.get(name)

    def heading(self):
        return self.driver.heading()

    def wind_speed(self):
        return self.driver.wind_speed()

    def wind_direction(self):
        return self.driver.wind_direction()

    def position(self):
        return self.driver.position()

    def rudder(self, angle):
        log.debug('setting rudder angle to {}'.format(angle))
        return self.driver.rudder(angle)

    def sail(self, angle):
        log.debug('setting sail angle to {}'.format(angle))
        return self.driver.sail(angle)
