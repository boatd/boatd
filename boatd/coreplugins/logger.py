from boatd import BasePlugin

import datetime
import time


log_format = 'time={time} '
             'bhead={head} '
             'wind={wind} '
             'lat={lat} '
             'lon={long} '
             'nwlat={wpn} '
             'nwlon={wpe} '
             'nwn={num} '
             'spos={sail} '
             'rpos={rudder} '
             'whead={waypoint_heading} '
             'distance={waypoint_distance} '
             'speed={speed} '
             'thead={target_heading} '
             'tdist={target_distance}\n\r'


class LoggerPlugin(BasePlugin):
    def main(self):
        period = self.config.period
        filename = self.config.filename

        while self.running:
            lat, lon = self.boatd.boat.position()

            ts = time.time()

            # FIXME: use the log_format string defined above
            log_line = log_format.format(
                    time=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'),
                    lat=lat,
                    long=lon,
            )

            with open(filename, 'a') as f:
                f.write(log_line)

            time.sleep(period)

plugin = LoggerPlugin
