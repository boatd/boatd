import os

import boatd


class TestDriver(object):
    def setup(self):
        self.directory, _ = os.path.split(__file__)
        self.driver_file = os.path.join(self.directory, 'driver.py')

        configuration = {
            'scripts': {
                'driver': 'driver.py'
            }
        }
        self.mock_config = boatd.Config(configuration)

    def test_config(self):
        assert self.mock_config.scripts
