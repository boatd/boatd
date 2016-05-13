import boatd

class MyFancyBoatDriver(boatd.BaseBoatdDriver):
    def __init__(self):
        # initialize some things here
        pass

    def heading(self):
        return 30.0

    def wind_direction(self):
        return 45.0

    def wind_speed(self):
        return 4.0

    def position(self):
        return (0, 0)

    def rudder(self, angle):
        print('moving rudder to', angle)

    def sail(self, angle):
        print('moving sail to', angle)

# create an instance of the driver class
driver = MyFancyBoatDriver()
