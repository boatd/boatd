from __future__ import print_function

import imp
import os
import sys
import traceback

from . import logging
from .boat import Boat
from .config import Config
from .driver import Driver
from .api import BoatdHTTPServer, BoatdRequestHandler


def load_conf():
    '''
    Return the configuration object. Reads from the first argument by default,
    otherwise falls back to 'boatd-config.yaml'.
    '''
    if len(sys.argv) > 1:
        conf_file = sys.argv[1]
    else:
        conf_file = ''

    _, ext = os.path.splitext(conf_file)
    if ext == '.yaml' or ext == '.yml':
        conf = Config.from_yaml(conf_file)
    elif ext == '.json':
        conf = Config.from_json(conf_file)
    else:
        conf = Config.from_yaml('boatd-config.yaml')

    conf.filename = conf_file

    return conf


def load_driver(conf):
    '''
    Return the driver module from the filename specified in the configuration
    file with key configuration.scripts.driver.
    '''
    directory, name = os.path.split(conf.scripts.driver)

    if hasattr(conf, 'filename'):
        conf_directory, _ = os.path.split(conf.filename)
        search_dirs = [directory, conf_directory]
    else:
        search_dirs = [directory]

    module_name = os.path.splitext(name)[0]
    try:
        found_module = imp.find_module(module_name, search_dirs)
        driver_module = imp.load_module('driver_module', *found_module)
    except:
        logging.log('exception raised in driver module:', logging.WARN)
        print(traceback.format_exc())
    finally:
        found_module[0].close()

    return driver_module.driver


def run():
    '''Run the main server.'''
    conf = load_conf()
    driver = load_driver(conf)
    boat = Boat(driver)

    httpd = BoatdHTTPServer(boat, ('', conf.boatd.port), BoatdRequestHandler)
    while httpd.running:
        httpd.handle_request()
