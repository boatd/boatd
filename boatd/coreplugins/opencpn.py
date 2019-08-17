import datetime
import math
import socket
import sys
import time
#import argparse
import serial

import socket

from boatd import BasePlugin

class OpencpnPlugin(BasePlugin):

    def calculate_checksum(self, line):
        '''Return the NMEA checksum for a given line'''
        x = 0
        for c in line:
            x ^= ord(c)
        s = str(hex(x))[2:]
        return ('0' if len(s) < 2 else '') + s.upper()

    def get_distance(self, lat1, lon1, lat2, lon2):
        '''
        Calculate the distance between lat1/lon1 and lat2/lon2 in metres
        Expects coordinates in degrees
        Returns distance in metres
        '''
        radius = 6371  #earth radius in km

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) * math.sin(dlon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c

        return d * 1000.0

    def get_heading(self, lat1, lon1, lat2, lon2):
        '''
        Calculate the distance between lat1/lon1 and lat2/lon2 in degrees
        Expects coordinates in degrees
        '''    
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)    

        heading = math.degrees(math.atan2(math.sin(lon2-lon1)*math.cos(lat2), 
                                      math.cos(lat1)*math.sin(lat2)-
                                      math.sin(lat1)*math.cos(lat2)*
                                      math.cos(lon2-lon1)))

        #make headings between 0 and 360 not -180 and +180
        if(heading<0):
            heading = heading + 360

        return heading


    def nmea_line(self, line):
        '''
        Return a completed nmea line (starting with $ and ending with checksum).
        '''
        checksum = self.calculate_checksum(line)
        return '$' + line + '*' + checksum


    def degrees_to_nmea(self, input_degrees,places=3):
        '''Return a nmea formatted bearing from decimal degrees'''
        degrees = math.trunc(input_degrees)
        minutes = (input_degrees - degrees) * 60
        if places == 2:
            return '{:02}{:07.4f}'.format(degrees, abs(minutes))
        elif places == 3:
            return '{:03}{:07.4f}'.format(degrees, abs(minutes))
        else:
            return '{}{:07.4f}'.format(degrees, abs(minutes))


    def hdm(self, heading):
        '''Return a HDM nmea sentance from a given heading'''
        line = 'HCHDT,{0:.3},T'.format(heading)
        return self.nmea_line(line)

    def gga(self, latitude, longitude, utc_datetime):
        '''
        return a GGA message using lat, long and utc time, as wel as dummy datat
        '''
        centisecond = str(utc_datetime.microsecond)[:2]
        t = utc_datetime.strftime('%H%M%S.') + centisecond
        lat_direction = 'N' if latitude > 0 else 'S'  # noqa
        lon_direction = 'E' if longitude > 0 else 'W'  # noqa
        line = 'GPGGA,{time},{lat},{lat_dir},{lon},{lon_dir},1,12,.5,0,M,0,M,,'.format(
            lat=self.degrees_to_nmea(abs(latitude),2),
            lon=self.degrees_to_nmea(abs(longitude),3),
            lat_dir=lat_direction,
            lon_dir=lon_direction,
            time=t)
        return self.nmea_line(line)


    def gll(self, latitude, longitude, utc_datetime):
        '''
        Return a GLL nmea sentance from a lat, long and date (datetime object).
        '''
        centisecond = str(utc_datetime.microsecond)[:2]
        t = utc_datetime.strftime('%H%M%S.') + centisecond
        lat_direction = 'N' if latitude > 0 else 'S'  # noqa
        lon_direction = 'E' if longitude > 0 else 'W'  # noqa
        line = 'GPGLL,{lat},{lat_dir},{lon},{lon_dir},{time},A'.format(
            lat=self.degrees_to_nmea(abs(latitude),2),
            lon=self.degrees_to_nmea(abs(longitude),3),
            lat_dir=lat_direction,
            lon_dir=lon_direction,
            time=t)
        return self.nmea_line(line)


    def vtg(self, old_latitude, old_longitude, latitude, longitude, old_utc_datetime, utc_datetime):
        '''
        return a VTG message with speed and track made good
        '''
        tmg = self.get_heading(old_latitude,old_longitude,latitude,longitude)
        #distance in metres
        distance = self.get_distance(old_latitude,old_longitude,latitude,longitude)

        #time in seconds
        time_diff = float(utc_datetime) - float(old_utc_datetime)

        #speed in metres/sec
        speed_ms = distance / time_diff
        #print("speed in m/s",speed_ms)
        speed_kts = speed_ms * 1.94384
        speed_kph = speed_ms * 3.6

        lat_direction = 'N' if latitude > 0 else 'S'  # noqa
        lon_direction = 'E' if longitude > 0 else 'W'  # noqa
        line = 'GPVTG,{:05.1f},T,{:05.1f},M,{:05.1f},N,{:05.1f},K'.format(
            tmg, tmg, speed_kts, speed_kph)

        return self.nmea_line(line)

    def mwv(self, wind_angle, wind_speed, wind_speed_units='M', reference='T'):
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
        return self.nmea_line(line)


    def rsa(self,rudder_angle):
        line = 'RSA,{0:.3g},A,0.0,X'.format(rudder_angle)
        return self.nmea_line(line)

    def wpt(self,latitude, longitude, title):
        '''
        Return a GPWPL string with waypoint information
        '''
        lat_direction = 'N' if latitude > 0 else 'S'  # noqa
        lon_direction = 'E' if longitude > 0 else 'W'  # noqa
        line = 'GPWPL,{lat},{lat_dir},{lon},{lon_dir},{name}'.format(
            lat=self.degrees_to_nmea(abs(latitude),2),
            lon=self.degrees_to_nmea(abs(longitude),3),
            lat_dir=lat_direction,
            lon_dir=lon_direction,
            name=title)
        return self.nmea_line(line)

    def send_nmea_message(sock, message, dest):
        message = message + u"\r\n"
        sock.sendto(message.encode("utf-8"), dest)

    def send_udp_packet(self, message, sock):
        print("sending UDP packet",message)
        sock.sendto(message, ('255.255.255.255',10000))

    def main(self):
        time.sleep(5)
        device = self.config.get('device', '/dev/ttyUSB0')
        baud = self.config.get('baud', 115200)
        delay = self.config.get('delay', 1)

        self.ser = serial.Serial(device, baud, timeout=0.1)

        self.waypoint_count = 0
        self.waypoints = []
        self.last_sent_waypoint = 0

        old_lat, old_lon = self.boatd.boat.position()
        old_time = time.time() 

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        while self.running:
            lat, lon = self.boatd.boat.position()
            heading = self.boatd.boat.heading()
            rudder = self.boatd.boat.target_rudder_angle
            wind_abs = self.boatd.boat.wind_absolute()
            wind = self.boatd.boat.wind_apparent()

            messages = [
                self.gga(lat,
                    lon,
                    datetime.datetime.now()),
                self.hdm(float(heading)),
                self.vtg(old_lat,old_lon,lat,lon,old_time,time.time()),
                self.mwv(float(wind_abs), reference='T', wind_speed=1),
                self.mwv(float(wind), reference='R', wind_speed=1),
                self.rsa(float(rudder)),
            ]

            #save current positions for the next calculation of vmg/cmg
            old_lat = lat
            old_lon = lon
            old_time = time.time()

            for m in messages:
                message = m + "\r\n"
                self.ser.write(str.encode(message))
                self.send_udp_packet(str.encode(message),sock)

            time.sleep(delay)


plugin = OpencpnPlugin