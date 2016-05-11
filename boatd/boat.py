class Boat(object):
    '''The boat itself. Most of the work is done by the active driver'''
    def __init__(self, driver):
        self.driver = driver
        self.active = False

    def __getattr__(self, name):
        '''Return the requested attribute from the currently loaded driver'''
        return self.driver.handlers.get(name)

    def heading(self):
        return self.driver.heading()

    def wind_speed(self):
        return self.driver.wind_speed()

    def wind_direction(self):
        return self.driver.wind_direction()

    def position(self):
        return self.driver.position()

    def rudder(self, angle):
        return self.driver.rudder(angle)

    def sail(self, angle):
        return self.driver.sail(angle)
