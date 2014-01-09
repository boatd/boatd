from __future__ import print_function

import imp
import sys
import os
import time
from functools import wraps

class Boat(object):
    def __init__(self, driver):
        self.driver = driver

    def __getattr__(self, name):
        func = vars(self.driver).get(name)
        if func is None:
            raise AttributeError
        else:
            return func

def inject_import(name, filename, inject):
    module = imp.new_module(name)
    vars(module).update(inject)
    with open(filename) as f:
        exec(f.read(), vars(module))
    sys.modules[name] = module
    return module

def log(message):
    print(time.strftime('[%H:%M:%S]'), message)

def do_something(func):
    @wraps(func)
    def inner(*args, **kwargs):
        r = func(*args, **kwargs)
        log('did something and got {}'.format(r))
        return r
    return inner

def main():
    assert len(sys.argv) > 2
    boatd = imp.new_module('boatd')
    vars(boatd).update(globals())
    drive_path = sys.argv[1]
    driver = inject_import('driver', drive_path, {'boatd': boatd})

    behaviour_path = sys.argv[2]
    behaviour = inject_import('behaviour',
                              behaviour_path,
                              {'boat': Boat(driver)})
