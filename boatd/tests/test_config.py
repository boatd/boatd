import os
import unittest

import boatd


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.directory, _ = os.path.split(__file__)
        self.yaml_file = os.path.join(self.directory, 'config.yaml')
        self.json_file = os.path.join(self.directory, 'config.json')

    def test_load_yaml(self):
        config = boatd.Config.from_yaml(self.yaml_file)
        assert config.boatd

    def test_load_json(self):
        config = boatd.Config.from_yaml(self.json_file)
        assert config.boatd

    def test_port(self):
        config = boatd.Config.from_yaml(self.yaml_file)
        assert config.boatd.port == 2222

    def test_driver(self):
        config = boatd.Config.from_yaml(self.yaml_file)
        assert config.scripts.driver == 'driver.py'

    def test_set_attr(self):
        config = boatd.Config.from_yaml(self.yaml_file)
        config.scripts.driver = 'new_driver.py'
        assert config.scripts.driver == 'new_driver.py'

    def test_get(self):
        config = boatd.Config.from_yaml(self.yaml_file)
        assert config.get('boatd') is not None

    def test_get_invalid(self):
        config = boatd.Config.from_yaml(self.yaml_file)
        assert config.get('not_a_valid_config_option') is None
