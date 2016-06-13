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

import math


def calculate_checksum(line):
    '''Return the NMEA checksum for a given line'''
    x = 0
    for c in line:
        x ^= ord(c)
    s = str(hex(x))[2:]
    return ('0' if len(s) < 2 else '') + s.upper()


def nmea_line(line):
    checksum = calculate_checksum(line)
    return '$' + line + '*' + checksum


def degrees_to_nmea(input_degrees):
    degrees = math.trunc(input_degrees)
    minutes = (input_degrees - degrees) * 60
    return '{}{:.3g}'.format(degrees, abs(minutes))


def hdm(heading):
    '''Return a HDM nmea sentance from a given heading'''
    line = 'HDM,{0:.3g},M'.format(heading)
    return nmea_line(line)


def gll(latitude, longitude, utc_datetime):
    '''
    Return a GLL nmea sentance from a lat, long and date (datetime object).
    '''
    centisecond = str(utc_datetime.microsecond)[:2]
    t = utc_datetime.strftime('%H%M%S.') + centisecond
    lat_direction = 'N' if latitude > 0 else 'S'  # noqa
    lon_direction = 'E' if longitude > 0 else 'W'  # noqa
    line = 'GLL,{lat},N,{lon},W,{time},A'.format(
        lat=degrees_to_nmea(abs(latitude)),
        lon=degrees_to_nmea(abs(longitude)),
        time=t)
    return nmea_line(line)
