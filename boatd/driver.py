from functools import wraps

class Driver(object):
    def __init__(self):
        print('Initialising driver')

        self.handlers = {}

    def function(self, f, name):
        @wraps(f)
        def dec(*args, **kwargs):
            print 'inner func'

            return f()
        self.handlers[name] = dec
        return dec

    def heading(self, f):
        return self.function(f, 'heading')
