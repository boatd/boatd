from functools import wraps

from . import logging


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
