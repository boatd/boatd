import boatd

class TestDriver(boatd.BaseBoatdDriver):
    def __init__(self):
        self.some_hardware = {}

    def reconnect(self):
        pass

    def heading(self):
        return 2.43

    def wind_speed(self):
        return 25

    def rudder(self, angle):
        self.some_hardware['rudder'] = angle

    def position(self):
        pass

    def sail(self):
        pass

    def absolute_wind_direction(self):
        return 1

driver = TestDriver()
