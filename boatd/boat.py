class Boat(object):
    '''The boat itself. Most of the work is done by the active driver'''
    def __init__(self, driver):
        self.driver = driver
        self.active = False

    def __getattr__(self, name):
        '''Return the requested attribute from the currently loaded driver'''
        return self.driver.handlers.get(name)
