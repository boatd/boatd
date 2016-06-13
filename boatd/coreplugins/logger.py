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

from boatd import BasePlugin

import datetime
import time


log_format = (
             'time={time} '
             'bhead={head} '
             'wind={wind} '
             'lat={lat} '
             'lon={long} '
             #'nwlat={wpn} '
             #'nwlon={wpe} '
             #'nwn={num} '
             #'spos={sail} '
             #'rpos={rudder} '
             #'whead={waypoint_heading} '
             #'distance={waypoint_distance} '
             #'speed={speed} '
             '\n\r'
             )


class LoggerPlugin(BasePlugin):
    def main(self):
        period = self.config.period
        filename = self.config.filename

        while self.running:
            heading = self.boatd.boat.heading()
            wind_direction = self.boatd.boat.wind_direction()
            lat, lon = self.boatd.boat.position()

            ts = time.time()

            log_line = log_format.format(
                    time=time.time(),
                    head=heading,
                    wind=wind_direction,
                    lat=lat,
                    long=lon,
            )

            with open(filename, 'a') as f:
                f.write(log_line)

            time.sleep(period)

plugin = LoggerPlugin
