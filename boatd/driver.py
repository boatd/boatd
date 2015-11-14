import logging
import threading
from functools import wraps

from .color import color

log = logging.getLogger(__name__)


class Driver(object):
    def __init__(self):
        self.heading = self.handler('heading')
        self.wind_direction = self.handler('wind_direction')
        self.wind_speed = self.handler('wind_speed')
        self.position = self.handler('position')

        self.rudder = self.handler(
            'rudder',
            function=lambda name, args:
            log.debug('calling {}({})'.format(name, *args)))

        self.sail = self.handler('sail')

        self.handlers = {}

    def handler(self, name, function=None):
        '''
        Handler function for a particular item in the driver. This implements
        logging and locking for thread safet.
        '''
        def wrapper(f):
            lock = threading.Lock()

            @wraps(f)
            def dec(*args, **kwargs):
                if callable(function):
                    function(f.__name__, args)
                with lock:
                    return f(*args, **kwargs)

            self.handlers[name] = dec
            log.info('Loaded function {} as {}'.format(
                     color(f.__name__, 32),
                     color('"{}"'.format(name), 35)))
            return dec
        return wrapper
