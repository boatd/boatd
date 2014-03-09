from functools import wraps

from . import logging
from .color import color


class Driver(object):
    def __init__(self):
        logging.log('Initialising driver')

        self.handlers = {}

    def handler(self, name):
        def wrapper(f):
            @wraps(f)
            def dec(*args, **kwargs):
                return f(*args, **kwargs)
            self.handlers[name] = dec
            logging.log('loaded function {} as "{}"'.format(
                        color(f.__name__, 32), color(name, 35)))
            return dec
        return wrapper

    def heading(self, func):
        @self.handler('heading')
        @wraps(func)
        def decorator():
            logging.log('requested heading', logging.VERBOSE)
            head = func()
            logging.log('heading: {}'.format(head))
            return head
        return decorator
