from functools import wraps

from . import logging

def maybe_run(func, *args, **kwargs):
    if func is not None:
        return func(*args, **kwargs)
    else:
        return None

def build_decorator(before_func=None,
                    after_func=None):
    def dec(func):
        @wraps(func)
        def inner(*args, **kwargs):
            maybe_run(before_func)
            return_value = func(*args, **kwargs)
            maybe_run(after_func, return_value)
            return return_value
        return inner
    return dec

do_something = build_decorator(
                   after_func=lambda x: logging.log('did something and got {}'.format(x))
               )

heading = build_decorator(
            lambda: logging.log('requested heading'),
            lambda x: logging.log('got heading: {}'.format(x))
          )
