from functools import wraps
import time

def log(message):
    print(time.strftime('[%H:%M:%S]'), message)

def do_something(func):
    @wraps(func)
    def inner(*args, **kwargs):
        r = func(*args, **kwargs)
        log('did something and got {}'.format(r))
        return r
    return inner
