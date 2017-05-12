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

from abc import ABCMeta, abstractmethod
import logging

log = logging.getLogger(__name__)


class BaseBoatdDriver(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def heading(self):
        '''
        Must return the heading of the boat in degrees, relative to the world.

        :rtype: float between 0 and 360
        '''
        pass

    @abstractmethod
    def wind_speed(self):
        '''
        Must return the speed the wind is blowing in knots.

        :rtype: float
        '''
        pass

    @abstractmethod
    def absolute_wind_direction(self):
        '''
        Must return the direction the wind is blowing in degrees, relative to
        the world.

        :rtype: float between 0 and 360
        '''
        pass

    @abstractmethod
    def position(self):
        '''
        Must return a tuple containing the current latitude and longitude of
        the boat, in that order.

        :rtype: tuple of two floats - ``(float, float)``
        '''
        pass

    @abstractmethod
    def rudder(self, angle):
        '''
        Set the boat's rudder to ``angle`` degrees relative to the boat.

        :param angle: target number of degrees
        :type angle: float between -90 and 90
        '''
        pass

    @abstractmethod
    def sail(self, angle):
        '''
        Set the sail to ``angle`` degrees relative to the boat.

        :param angle: target number of degrees
        :type angle: float between -90 and 90
        '''
        pass

    @abstractmethod
    def reconnect(self):
        '''
        Reconnect the driver to boat devices. It is recommended that initial
        connections are made using this function by calling it in the
        ``__init__`` method. If the driver does not require any persistent
        connections, this method may be empty.
        '''
        pass
