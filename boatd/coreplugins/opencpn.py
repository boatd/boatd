import datetime
import math
import socket
import sys
import time
import argparse


from boatd import BasePlugin

class OpencpnPlugin(BasePlugin):

    def calculate_checksum(line):
        '''Return the NMEA checksum for a given line'''
        x = 0
        for c in line:
            x ^= ord(c)
        s = str(hex(x))[2:]
        return ('0' if len(s) < 2 else '') + s.upper()


    def nmea_line(line):
        '''
        Return a completed nmea line (starting with $ and ending with checksum).
        '''
        checksum = calculate_checksum(line)
        return '$' + line + '*' + checksum


    def degrees_to_nmea(input_degrees,places=3):
        '''Return a nmea formatted bearing from decimal degrees'''
        degrees = math.trunc(input_degrees)
        minutes = (input_degrees - degrees) * 60
        if places == 2:
            return '{:02}{:07.4f}'.format(degrees, abs(minutes))
        elif places == 3:
            return '{:03}{:07.4f}'.format(degrees, abs(minutes))
        else:
            return '{}{:07.4f}'.format(degrees, abs(minutes))


    def hdm(heading):
        '''Return a HDM nmea sentance from a given heading'''
        line = 'HCHDT,{0:.3},T'.format(heading)
        return nmea_line(line)

    def gga(latitude, longitude, utc_datetime):
        '''
        return a GGA message using lat, long and utc time, as wel as dummy datat
        '''
        centisecond = str(utc_datetime.microsecond)[:2]
        t = utc_datetime.strftime('%H%M%S.') + centisecond
        lat_direction = 'N' if latitude > 0 else 'S'  # noqa
        lon_direction = 'E' if longitude > 0 else 'W'  # noqa
        line = 'GPGGA,{time},{lat},{lat_dir},{lon},{lon_dir},1,12,.5,0,M,0,M,,'.format(
            lat=degrees_to_nmea(abs(latitude),2),
            lon=degrees_to_nmea(abs(longitude),3),
            lat_dir=lat_direction,
            lon_dir=lon_direction,
            time=t)
        return nmea_line(line)


    def gll(latitude, longitude, utc_datetime):
        '''
        Return a GLL nmea sentance from a lat, long and date (datetime object).
        '''
        centisecond = str(utc_datetime.microsecond)[:2]
        t = utc_datetime.strftime('%H%M%S.') + centisecond
        lat_direction = 'N' if latitude > 0 else 'S'  # noqa
        lon_direction = 'E' if longitude > 0 else 'W'  # noqa
        line = 'GPGLL,{lat},{lat_dir},{lon},{lon_dir},{time},A'.format(
            lat=degrees_to_nmea(abs(latitude),2),
            lon=degrees_to_nmea(abs(longitude),3),
            lat_dir=lat_direction,
            lon_dir=lon_direction,
            time=t)
        return nmea_line(line)


    def mwv(wind_angle, wind_speed, wind_speed_units='M', reference='T'):
        '''
        Return an MWV nmea sentance (wind information).

        wind_speed_units can be one of K/M/N,
        reference can be 'R' = Relative, 'T' = True.
        '''
        line = 'MWV,{0:.3g},{reference},{speed},{speed_units},A'.format(
            wind_angle,
            reference=reference,
            speed=wind_speed,
            speed_units=wind_speed_units,
        )
        return nmea_line(line)


    def rsa(rudder_angle):
        line = 'RSA,{0:.3g},A,0.0,X'.format(rudder_angle)
        return nmea_line(line)

    def wpt(latitude, longitude, title):
        '''
        Return a GPWPL string with waypoint information
        '''
        lat_direction = 'N' if latitude > 0 else 'S'  # noqa
        lon_direction = 'E' if longitude > 0 else 'W'  # noqa
        line = 'GPWPL,{lat},{lat_dir},{lon},{lon_dir},{name}'.format(
            lat=degrees_to_nmea(abs(latitude),2),
            lon=degrees_to_nmea(abs(longitude),3),
            lat_dir=lat_direction,
            lon_dir=lon_direction,
            name=title)
        return nmea_line(line)

    def send_nmea_message(sock, message, dest):
        message = message + u"\r\n"
        sock.sendto(message.encode("utf-8"), dest)


    def main(self):
        time.sleep(5)
        device = self.config.get('device', '/dev/ttyUSB0')
        baud = self.config.get('baud', 115200)
        delay = self.config.get('delay', 1)

        self.ser = serial.Serial(device, baud, timeout=0.1)

        self.waypoint_count = 0
        self.waypoints = []
        self.last_sent_waypoint = 0

        while self.running:
            lat, lon = self.boatd.boat.position()
            heading = self.boatd.boat.heading()
            rudder = self.boatd.boat.target_rudder_angle()
            wind_abs = self.boatd.boat.wind.absolute()
            wind = self.boatd.boat.wind.apparent()

            messages = [
                gga(lat,
                    lon,
                    datetime.datetime.now()),
                hdm(float(heading)),
                mwv(float(wind_abs), reference='T', wind_speed=1),
                mwv(float(wind), reference='R', wind_speed=1),
                rsa(float(rudder)),
            ]

            for m in messages:
                message = m + u"\r\n"
                self.ser.write(message)

            time.sleep(delay)


plugin = OpencpnPlugin