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
    if len(sys.argv) > 1:
        conf_file = sys.argv[1]
    else:
        conf_file = 'boatd-config.yaml'

    _, ext = os.path.splitext(conf_file)
    if ext == '.yaml':
        conf = Config.from_yaml(conf_file)
    elif ext == '.json':
        conf = Config.from_json(conf_file)

    conf.filename = conf_file

    return conf

def load_driver(conf):
    directory, name = os.path.split(conf.scripts.driver)
    conf_directory, _ = os.path.split(conf.filename)
    module_name = os.path.splitext(name)[0]
    try:
        found_module = imp.find_module(module_name, [directory, conf_directory])
        driver_module = imp.load_module('driver_module', *found_module)
    except:
        logging.log('exception raised in driver module:', logging.WARN)
        print(traceback.format_exc())
    finally:
        found_module[0].close()

    return driver_module.driver

def run():
    conf = load_conf()
    driver = load_driver(conf)
    boat = Boat(driver)

    httpd = BoatdHTTPServer(boat, ('', conf.boatd.port), BoatdRequestHandler)
    while httpd.running:
        httpd.handle_request()
