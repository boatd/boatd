from math import pi
from functools import wraps

from . import logging


def maybe_run(func, *args, **kwargs):
    if func is not None:
        return func(*args, **kwargs)
    else:
        return None


def build_decorator(before_func=None,
                    after_func=None,
                    constrain=None):
    def dec(func):
        @wraps(func)
        def inner(*args, **kwargs):
            maybe_run(before_func)
            return_value = func(*args, **kwargs)
            maybe_run(after_func, return_value)

            if constrain is not None:
                if hasattr(constrain, '__call__'):
                    if constrain(return_value):
                        logging.log('{} is out of bounds "{}"'.format(
                            inner.__name__,
                            return_value), level=logging.WARN)

                else:
                    lower, upper = constrain
                    if not lower <= return_value <= upper:
                        logging.log('{} is out of bounds ({} < {} < {})'.format(
                            inner.__name__,
                            lower,
                            return_value,
                            upper), level=logging.WARN)
            return return_value
        return inner
    return dec

do_something = build_decorator(
    after_func=lambda x: logging.log(
        'did something and got {}'.format(x))
)

heading = build_decorator(
    lambda: logging.log('requested heading', logging.VERBOSE),
    lambda x: logging.log('heading: {}'.format(x)),
    constrain=(0, 2*pi)
)

wind = build_decorator(
    lambda: logging.log('requested wind', logging.VERBOSE),
    lambda x: logging.log('wind: {}'.format(x)),
    constrain=(0, 2*pi)
)
