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
