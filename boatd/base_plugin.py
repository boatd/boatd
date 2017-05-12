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


class BasePlugin(object):
    __metaclass__ = ABCMeta

    def __init__(self, config, boatd):
        self.config = config
        self.boatd = boatd
        self.running = False

    def start(self):
        self.running = True
        self.main()

    @abstractmethod
    def main(self):
        '''
        The main method for a plugin. This should contain a loop if the plugin
        is intended to be long-running.
        '''
        pass
