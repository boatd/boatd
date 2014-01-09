from __future__ import print_function

import imp
import sys
import os
from functools import wraps

from .decorators import *
from .boat import Boat
from .config import Config

def inject_import(name, filename, inject):
    module = imp.new_module(name)
    vars(module).update(inject)
    with open(filename) as f:
        exec(f.read(), vars(module))
    return module

class Driver(object):
    def __init__(self, driver_path, boatd):
        self.module = inject_import('driver',
                                    driver_path,
                                    {'boatd': boatd})
        self.path = driver_path

def main():
    if len(sys.argv) > 1:
        conf = Config.from_file(sys.argv[1])
    else:
        conf = Config.from_file('boatd-config.json')

    boatd = imp.new_module('boatd')
    vars(boatd).update(globals())
    driver = Driver(conf.driver, boatd)

    behaviour = inject_import('behaviour',
                              conf.behaviour,
                              {'boat': Boat(driver)})
