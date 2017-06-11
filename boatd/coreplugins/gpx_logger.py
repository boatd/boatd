from boatd import BasePlugin

import datetime
import time

gpx_trkpt_format = (
             '\t\t\t<trkpt '
             'lat="{lat}" '
             'lon="{long}">'
             
             '<time>{datetime}</time>'
             
             '<cmt>Rudder:{rudder} Sail:{sail} Wind:{wind_direction} Heading:{heading}</cmt>'
             
             '</trkpt>'
             '\n'
             )
             
gpx_wpt_format = (
             '\t\t<wpt '
             'lat="{lat}" '
             'lon="{long}">'
             '</wpt>'
             '\n'
             )

class GPXLoggerPlugin(BasePlugin):
    def main(self):
        self.period = self.config.period
        self.filename = self.config.filename + time.strftime("_%d-%m-%yT%H,%M,%SZ.gpx")
        
        self.startfile()
        
        self.trackpoints()
        
        self.waypoints()
            
        self.endfile()
            
    def startfile(self):
        
        with open(self.filename, 'a') as f:
                f.write('<?xml version="1.0"?> \n'
    '<gpx creator="boatd" xmlns="http://www.topografix.com/GPX/1/1"'
    ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation='
    '"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n')
                f.write("\t<name>Boatd Output Track</name>\n")
                
    def trackpoints(self):
        with open(self.filename, 'a') as f:
            f.write("\t<trk>\n\t\t<trkseg> \n")
        
            while self.running:
                boat_heading = self.boatd.boat.heading()
                boat_wind_direction = self.boatd.boat.wind_absolute()
                boat_lat, boat_lon = self.boatd.boat.position()
                boat_sail = self.boatd.boat.get_sail()
                boat_rudder = self.boatd.boat.get_rudder()
                boat_datetime = datetime.datetime.now().isoformat()

                log_line = gpx_trkpt_format.format(
                        lat=boat_lat,
                        long=boat_lon,
                        datetime=boat_datetime,
                        rudder=boat_rudder,
                        sail=boat_sail,
                        wind_direction=boat_wind_direction,
                        heading=boat_heading,
                )

                f.write(log_line)

                time.sleep(self.period)
            
            f.write("\t\t</trkseg>\n\t</trk>\n")
            
    def waypoints(self):
        with open(self.filename, 'a') as f:
            for mark in self.boatd.waypoint_manager.waypoints:
                mark_lat, mark_long = mark
            
                point_line = gpx_wpt_format.format(
                    lat=mark_lat,
                    long=mark_long,
                )
            
                f.write(point_line)
    
    def endfile(self):
        with open(self.filename, 'a') as f:
                f.write("</gpx>")

plugin = GPXLoggerPlugin
