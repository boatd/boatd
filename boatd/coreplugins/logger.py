from boatd import BasePlugin

import time


class LoggerPlugin(BasePlugin):
    def main(self):
        while self.running:
            print('logging some crap')
            time.sleep(1)

plugin = LoggerPlugin
