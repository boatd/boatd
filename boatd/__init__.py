# This file is part of boatd, the Robotic Sailing Boat Daemon.
#
# Copyright (C) 2013-2017 Louis Taylor <louis@kragniz.eu>
#
# boatd is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# boatd is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import argparse
import logging
import imp
import os
import sys
import signal

from . import logger
from . import plugin
from .api import BoatdAPI
from .behaviour import Behaviour
from .behaviour import BehaviourManager
from .boat import Boat
from .color import color
from .config import Config
from .waypoints import WaypointManager
from .driver import BaseBoatdDriver  # noqa
from .base_plugin import BasePlugin  # noqa


__version__ = '2.0.0'

log = logging.getLogger()


def shutdown(behaviour_manager, plugins):
    log.info('Quitting and requesting plugins end...')
    behaviour_manager.stop()
    for p in plugins:
        p.running = False
    sys.exit()


def load_conf(conf_file):
    '''
    Return the configuration object. Reads from the first argument by default,
    otherwise falls back to 'boatd-config.yaml'.
    '''

    conf = Config.from_yaml(conf_file)
    conf.filename = conf_file

    return conf


def load_driver(conf):
    '''
    Return the driver module from the filename specified in the configuration
    file with key configuration.scripts.driver.
    '''

    driver_file = conf.driver.get('file', None)
    driver_module_name = conf.driver.get('module', None)

    if driver_file and driver_module_name:
        log.error('you should only specify one of file and module for driver '
                  'configuration')
        exit(1)

    if driver_module_name is not None:
        driver_module = __import__(driver_module_name)
        return driver_module.driver

    expanded_path = os.path.expanduser(conf.driver.file)
    directory, name = os.path.split(expanded_path)
    sys.path.append(os.path.dirname(directory))

    if hasattr(conf, 'filename'):
        conf_directory, _ = os.path.split(conf.filename)
        search_dirs = [directory, conf_directory]
    else:
        search_dirs = [directory]

    module_name = os.path.splitext(name)[0]
    try:
        found_module = imp.find_module(module_name, search_dirs)

        _, filename, _ = found_module
        log.info('Loading boat driver from {}'.format(color(filename, 37)))

        driver_module = imp.load_module('driver_module', *found_module)
        log.info('Using \'{}\' as boat driver'.format(
            color(type(driver_module.driver).__name__, 33)))

    except Exception:
        log.exception('Exception raised in boat driver module')
        raise
    finally:
        found_module[0].close()

    if not isinstance(driver_module.driver, BaseBoatdDriver):
        log.error('Driver module does not instantiate BaseBoatdDriver')
        sys.exit(1)

    return driver_module.driver


def load_behaviours(conf):
    behaviour_manager = BehaviourManager()

    for behaviour in conf.behaviours:
        name = list(behaviour.keys())[0]
        behaviour_conf = behaviour.get(name)
        filename = behaviour_conf.get('file')

        b = Behaviour(name, filename)
        behaviour_manager.add(b)

    return behaviour_manager


def load_waypoints(conf):
    waypoints_file = conf.get('waypoint_file', None)
    waypoints = []
    if waypoints_file is not None:
        with open(waypoints_file) as f:
            lines = f.readlines()
            for line in lines:
                # trim comments and skip empty lines
                point = line.split('#')[0].strip()
                if point:
                    lat, lon = point.split()
                    waypoints.append((float(lat), float(lon)))

    return waypoints


def parse_args():
    description = '''\
Experimental robotic sailing boat daemon.
'''

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('config', metavar='CONFIG FILE',
                        default='/etc/boatd-config.yaml',
                        nargs='?',
                        help='a path to a configuration file')
    parser.add_argument('--version',
                        action='version',
                        version='boatd {}'.format(__version__))
    return parser.parse_args()


def run():
    '''Run the main server.'''

    args = parse_args()

    conf = load_conf(args.config)

    logger.setup_logging()

    driver = load_driver(conf)
    boat = Boat(driver, config=conf)

    behaviour_manager = load_behaviours(conf)

    waypoints = load_waypoints(conf)
    home_position = conf.get('home_position', None)

    waypoint_manager = WaypointManager(home_position=home_position)
    waypoint_manager.add_waypoints(waypoints)

    plugins = plugin.load_plugins(conf, boat, waypoint_manager)

    def shutdown_handler(signum, frame):
        shutdown(behaviour_manager, plugins)

    signal.signal(signal.SIGTERM, shutdown_handler)

    api = BoatdAPI(boat, behaviour_manager, waypoint_manager,
                   (conf.boatd.interface, conf.boatd.port))

    try:
        api.run()
    except (KeyboardInterrupt):
        shutdown(behaviour_manager, plugins)
