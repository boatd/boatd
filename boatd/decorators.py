from functools import wraps

from . import logging

def do_something(func):
     @wraps(func)
     def inner(*args, **kwargs):
         return_value = func(*args, **kwargs)
         logging.log('did something and got {}'.format(return_value))
         return return_value
     return inner
