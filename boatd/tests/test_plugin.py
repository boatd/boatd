import os
import time
import unittest

import boatd

d, _ = os.path.split(__file__)
PLUGIN_DIR = os.path.join(d, 'plugin')
PLUGIN_FILENAME = os.path.join(PLUGIN_DIR, 'small_plugin.py')

class TestPlugin(unittest.TestCase):
    def test_find_plugins(self):
        plugins = boatd.plugin.find_plugins([PLUGIN_DIR], ['small_plugin'])
        print(plugins)
        path_in = ['boatd/boatd/tests/plugin/small_plugin.py' in p for _, p in plugins]
        assert True in path_in

    def test_get_module_name(self):
        assert boatd.plugin.get_module_name(PLUGIN_FILENAME) == 'small_plugin'

    def test_load_plugins(self):
        conf = {
            'plugin_directory': PLUGIN_DIR,
            'plugins': [
                {
                    'small_plugin': {
                        'enabled': True,
                        'thing': True
                    }
                }
            ]
        }

        print(conf)

        modules = boatd.plugin.load_plugins(boatd.config.Config(conf),
                object(), object())
        assert True in [hasattr(module, 'accessed') for module in modules]

    def test_disabled_plugins(self):
        conf = {
            'plugin_directory': PLUGIN_DIR,
            'plugins': [
                {
                    'small_plugin': {
                        'enabled': False,
                        'thing': True
                    }
                }
            ]
        }

        print(conf)

        modules = boatd.plugin.load_plugins(boatd.config.Config(conf),
                object(), object())
        assert modules == []
