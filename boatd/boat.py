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
import math
import threading
import time

log = logging.getLogger(__name__)


class Boat(object):
    '''The boat itself. Most of the work is done by the active driver'''
    def __init__(self, driver, config=None):
        self.driver = driver
        self.active = False

        self.config = config if config else {}

        self._cached_heading = 0
        self._cached_wind_speed = 0
        self._cached_wind_direction = 0
        self._cached_position = (0, 0)
        self._cached_rudder_angle = 0
        self._cached_sail_angle = 0

        self.target_rudder_angle = 0
        self.target_sail_angle = 0

        # wind sensor averaging values (see the paper 'Technologies for
        # Autonomous Sailing: Wings and Wind Sensors')
        self.s = 0  # average sine value
        self.c = 0  # average cosine value
        # rate of change
        self.r = self.config.get(
            'wind_filtering', {'rate_of_change': 75}).\
            get('rate_of_change', 75)
        self.wind_filtering_enabled = self.config.get(
            'wind_filtering',
            {'enabled': True}).\
            get('enabled', True)

        self._update_thread_running = True
        self.update_thread = threading.Thread(
            target=self.update_cached_values_loop
        )
        self.update_thread.daemon = True
        self.update_thread.start()

        self.rudder_thread = threading.Thread(
            target=self.rudder_setting_loop)
        self.rudder_thread.daemon = True
        self.rudder_thread.start()

        self.sail_thread = threading.Thread(
            target=self.sail_setting_loop)
        self.sail_thread.daemon = True
        self.sail_thread.start()

    def update_cached_values(self):
        '''Update cached sensor values.'''
        try:
            self._cached_heading = self.driver.heading()
        except Exception as e:
            log.error('Got error when trying to update heading: '
                      '{}'.format(e))
            self.driver.reconnect()

        try:
            self._cached_wind_speed = self.driver.wind_speed()
        except Exception as e:
            log.error('Got error when trying to update wind speed: '
                      '{}'.format(e))
            self.driver.reconnect()

        try:
            if self.wind_filtering_enabled:
                wind_dir = self.driver.absolute_wind_direction()
                self._cached_wind_direction = self._get_wind_average(wind_dir)
            else:
                self._cached_wind_direction = \
                    self.driver.absolute_wind_direction()
        except Exception as e:
            log.error('Got error when trying to update wind direction: '
                      '{}'.format(e))
            self.driver.reconnect()

        try:
            self._cached_position = self.driver.position()
        except Exception as e:
            log.error('Got error when trying to update position: '
                      '{}'.format(e))
            self.driver.reconnect()

    def update_cached_values_loop(self):
        '''Run in background and periodically update sensor values.'''

        # run until _update_thread_running is false
        while True:
            self.update_cached_values()
            time.sleep(0.05)

    def rudder_setting_loop(self):
        while True:
            if abs(self.target_rudder_angle - self._cached_rudder_angle) > 0.2:
                self._cached_rudder_angle = self.target_rudder_angle
                self.driver.rudder(self.target_rudder_angle)
            time.sleep(0.01)

    def sail_setting_loop(self):
        while True:
            if abs(self.target_sail_angle - self._cached_sail_angle) > 1:
                self._cached_sail_angle = self.target_sail_angle
                self.driver.sail(self.target_sail_angle)
            time.sleep(0.2)

    def rudder(self, angle):
        log.debug('setting rudder angle to {}'.format(angle))
        self.target_rudder_angle = angle

    def sail(self, angle):
        log.debug('setting sail angle to {}'.format(angle))
        self.target_sail_angle = angle

    def __getattr__(self, name):
        '''Return the requested attribute from the currently loaded driver'''
        return self.driver.handlers.get(name)

    def heading(self):
        return self._cached_heading

    def wind_speed(self):
        return self._cached_wind_speed

    def wind_apparent(self):
        return self._cached_wind_direction

    def wind_absolute(self):
        return self._cached_wind_direction - self._cached_heading

    def position(self):
        return self._cached_position

    def _get_wind_average(self, wind_direction):
        self.s += (math.sin(math.radians(wind_direction)) - self.s) / self.r
        self.c += (math.cos(math.radians(wind_direction)) - self.c) / self.r
        a = int(math.degrees(math.atan2(self.s, self.c)))
        if a < 0:
            return a + 360
        else:
            return a
