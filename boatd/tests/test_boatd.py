import sys
import os
import unittest

import boatd

class TestBoatd(unittest.TestCase):
    def setUp(self):
        sys.argv = sys.argv[0:1]
        self.directory, _ = os.path.split(__file__)

    def test_load_yaml_config(self):
        conf_file = os.path.join(self.directory, 'config.yaml')
        conf = boatd.load_conf(conf_file)
        assert conf.scripts.driver == 'driver.py'

    def test_load_default(self):
        current_dir = os.getcwd()
        os.chdir(self.directory)
        conf = boatd.load_conf('config.yaml')
        assert conf.scripts.driver == 'driver.py'

    def test_load_driver(self):
        configuration = {
            'driver': {
                'file': 'driver.py'
            }
        }
        mock_config = boatd.Config(configuration)
        mock_config.filename = os.path.join(self.directory, 'c.yaml')
        driver = boatd.load_driver(mock_config)
        assert driver.heading() == 2.43
