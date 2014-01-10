from functools import wraps

from . import logging

def build_decorator(called_func):
    def dec(func):
        @wraps(func)
        def inner(*args, **kwargs):
            return_value = func(*args, **kwargs)
            called_func(return_value)
            return return_value
        return inner
    return dec

do_something = build_decorator(lambda x: logging.log('did something and got {}'.format(x)))
heading = build_decorator(lambda x: logging.log('heading: {}'.format(x)))
