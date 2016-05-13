from boatd import BasePlugin

import datetime
import time


class LoggerPlugin(BasePlugin):
    def main(self):
        period = self.config.period
        filename = self.config.filename

        while self.running:
            lat, lon = self.boatd.boat.position()

            ts = time.time()

            log_line = '{} lat:{} long:{}\n'.format(
                    datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'),
                    lat,
                    lon
            )

            with open(filename, 'a') as f:
                f.write(log_line)

            time.sleep(period)

plugin = LoggerPlugin
