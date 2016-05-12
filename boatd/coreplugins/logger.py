from boatd import BasePlugin

import time


class LoggerPlugin(BasePlugin):
    def main(self):
        while self.running:
            position = self.boatd.boat.position()
            print('logging some crap -', position)
            time.sleep(1)

plugin = LoggerPlugin
