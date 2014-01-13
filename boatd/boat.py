class Boat(object):
    '''The boat itself. Most of the work is done by the active driver'''
    def __init__(self, driver):
        self.driver = driver

    def __getattr__(self, name):
        '''Return the requested attribute from the currently loaded driver'''
        func = vars(self.driver.module).get(name)
        if func is None:
            raise AttributeError(
                "'{}' driver has no attribute '{}'".format(
                    self.driver.path,
                    name)
            )
        else:
            return func
