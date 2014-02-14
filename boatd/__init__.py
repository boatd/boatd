from __future__ import print_function

import imp
import sys

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


class Behaviour(object):
    def __init__(self, behaviour_path, boat):
        self.boat = boat
        self.path = behaviour_path

    def run(self):
        return inject_import('behaviour',
                             self.path,
                             {'boat': self.boat})


def main():
    if len(sys.argv) > 1:
        conf = Config.from_yaml(sys.argv[1])
    else:
        conf = Config.from_yaml('boatd-config.yaml')

    boat = Boat()
    driver = Driver(conf.driver, boat)

    behaviour = Behaviour(conf.behaviour, boat)
    behaviour.run()
