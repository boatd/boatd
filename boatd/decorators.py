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
                    constrain=None,
                    setter=False):
    def dec(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if setter:
                maybe_run(before_func, *args, **kwargs)
            else:
                maybe_run(before_func)

            return_value = func(*args, **kwargs)
            maybe_run(after_func, return_value)

            if constrain is not None:
                if hasattr(constrain, '__call__'):
                    if not constrain(return_value):
                        logging.log('{} is invalid with the value "{}"'.format(
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

position = build_decorator(
    lambda: logging.log('requested position', logging.VERBOSE),
    lambda x: logging.log('position: {}, {}'.format(x[0], x[1])),
    constrain=lambda x:
        all(isinstance(v, (int, long, float)) for v in [x[0], x[1]])
)
