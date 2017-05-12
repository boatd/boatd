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

import imp
import logging
import os
import threading

from .color import color
from . import utils
from .config import Config

log = logging.getLogger(__name__)


class Boatd(object):
    def __init__(self, boat, waypoint_manager):
        self.boat = boat
        self.waypoint_manager = waypoint_manager


boatd_module = None


def get_boatd_module(boat, waypoint_manager):
    global boatd_module
    if boatd_module is None:
        boatd_module = Boatd(boat, waypoint_manager)

    return boatd_module


def get_module_name(filepath):
    _, name = os.path.split(filepath)
    module_name, _ = os.path.splitext(name)
    return module_name


def find_plugins(search_directories, enabled_plugins):
    found_plugins = []

    for plugin_name in enabled_plugins:
        found = False
        for directory in search_directories:
            path = os.path.join(directory, plugin_name) + '.py'
            if os.path.isfile(path):
                found = True
                found_plugins.append((plugin_name, path))

        if found is not True:
            log.warning('Could not find an appropriate module for plugin '
                        '\'{}\''.format(color(plugin_name, 31)))

    return found_plugins


def start_plugin(module, conf, boat, waypoint_manager):
    log.info('Starting plugin {} with config \'{}\''.format(
             color(module.plugin.__name__, 34),
             color(str(conf), 36)))

    boatd = get_boatd_module(boat, waypoint_manager)
    plugin = module.plugin(conf, boatd)

    t = threading.Thread(target=plugin.start)
    t.start()

    return plugin


def load_plugins(conf, boat, waypoint_manager):
    plugin_dirs = [utils.reldir(__file__, 'coreplugins')]

    if conf.get('plugin_directory') is not None:
        plugin_dirs += [conf.plugin_directory]

    plugin_names = get_plugin_names_from_config(conf)

    found_plugins = find_plugins(plugin_dirs, plugin_names)

    plugins = []
    for (name, module_filename) in found_plugins:
        with open(module_filename) as f:
            plugin_conf = get_config_for_plugin(conf, name)
            if plugin_conf.get('enabled', False):
                module = imp.load_module(
                    get_module_name(module_filename),
                    f,
                    module_filename,
                    ('.py', 'U', 1)
                )
                log.info('Loaded plugin from {}'.format(
                        color(module_filename, 37)))

                plugins.append(start_plugin(module,
                                            plugin_conf,
                                            boat,
                                            waypoint_manager))
            else:
                log.info('Ignored plugin {}, since `enabled: true` is not '
                         'set in plugin config'.format(color(name, 36)))

    return plugins


def get_plugin_names_from_config(config):
    return [list(plugin.keys())[0] for plugin in config.plugins]


def get_config_for_plugin(config, plugin_name):
    for plugin in config.plugins:
        conf = plugin.get(plugin_name, None)
        if conf is not None:
            return Config(conf)
    return Config({})
