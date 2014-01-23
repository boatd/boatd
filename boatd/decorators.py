from math import pi
from functools import wraps

from . import logging


def maybe_run(func, *args, **kwargs):
    if func is not None:
        return func(*args, **kwargs)
    else:
        return None


def constrain_value(constrain, value, funcname):
    if hasattr(constrain, '__call__'):
        if not constrain(value):
            logging.log('{} is invalid with the value "{}"'.format(
                funcname,
                value), level=logging.WARN)
            return False
        else:
            return True

    elif value is not None:
        if hasattr(value, '__len__'):
            if len(value) == 1:
                value = value[0]

        lower, upper = constrain
        if not lower <= value <= upper:
            logging.log('{} is out of bounds ({} < {} < {})'.format(
                funcname,
                lower,
                value,
                upper), level=logging.WARN)
            return False
        else:
            return True

def build_decorator(before_func=None,
                    after_func=None,
                    constrain=None,
                    input_constrain=None):
    def dec(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if input_constrain is not None:
                if constrain_value(input_constrain,
                                   args,
                                   '{} input'.format(inner.__name__)):
                    maybe_run(before_func, *args, **kwargs)
            else:
                maybe_run(before_func)

            return_value = func(*args, **kwargs)
            maybe_run(after_func, return_value)

            if constrain is not None:
                constrain_value(constrain, return_value, inner.__name__)
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

rudder = build_decorator(
    lambda x: logging.log('setting rudder to {}'.format(x)),
    lambda x: logging.log('rudder position set', logging.VERBOSE),
    input_constrain=(-pi, pi)
)
