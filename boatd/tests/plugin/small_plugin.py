import boatd

class TestPlugin(boatd.BasePlugin):
    def __init__(self, conf, boatd):
        self.accessed = False
        self.boat = boatd

    def main(self):
        self.boat.accessed = True

plugin = TestPlugin
