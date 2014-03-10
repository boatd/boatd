import boatd
import os

class TestConfig(object):
    def test_yaml(self):
        print(__file__)
        self.config = boatd.Config.from_yaml('config.yaml')
        assert self.config.boatd.port == 2222
        
