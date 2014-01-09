from __future__ import print_function

import imp
import sys
import os
from functools import wraps

from .decorators import *
from .boat import Boat

def inject_import(name, filename, inject):
    module = imp.new_module(name)
    vars(module).update(inject)
    with open(filename) as f:
        exec(f.read(), vars(module))
    sys.modules[name] = module
    return module

def main():
    assert len(sys.argv) > 2
    boatd = imp.new_module('boatd')
    vars(boatd).update(globals())
    driver_path = sys.argv[1]
    driver = inject_import('driver', driver_path, {'boatd': boatd})

    behaviour_path = sys.argv[2]
    behaviour = inject_import('behaviour',
                              behaviour_path,
                              {'boat': Boat(driver)})
