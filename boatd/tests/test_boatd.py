import sys
import os

import boatd

class TestBoatd(object):
    def __init__(self):
        sys.argv = sys.argv[0:1]
        self.directory, _ = os.path.split(__file__)

    def test_version(self):
        assert boatd.VERSION == 1.1

    def test_load_json_config(self):
        conf_file = os.path.join(self.directory, 'config.json')
        conf = boatd.load_conf(sys.argv + [conf_file])
        assert conf.scripts.driver == 'driver.py'

    def test_load_yaml_config(self):
        conf_file = os.path.join(self.directory, 'config.yaml')
        conf = boatd.load_conf(sys.argv + [conf_file])
        assert conf.scripts.driver == 'driver.py'

    def test_load_default(self):
        current_dir = os.getcwd()
        os.chdir(self.directory)
        conf = boatd.load_conf(sys.argv)
        assert conf.scripts.driver == 'driver.py'

    def test_load_driver(self):
        configuration = {
            'scripts': {
                'driver': 'driver.py'
            }
        }
        mock_config = boatd.Config(configuration)
        mock_config.filename = os.path.join(self.directory, 'c.yaml')
        driver = boatd.load_driver(mock_config)
        assert driver.handlers.get('pony')() == 'magic'
