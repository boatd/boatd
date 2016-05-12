from abc import ABCMeta, abstractmethod


class BasePlugin(object):
    __metaclass__ = ABCMeta

    def __init__(self, config, boatd):
        self.config = config
        self.boatd = boatd
        self.running = False

    def start(self):
        self.running = True
        self.main()

    @abstractmethod
    def main(self):
        pass
