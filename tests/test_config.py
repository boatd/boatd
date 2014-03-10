import boatd
import os

class TestConfig(object):
    def setup(self):
        self.directory, _ = os.path.split(__file__)
        self.yaml_file = os.path.join(self.directory, 'config.yaml')

    def test_load_yaml(self):
        config = boatd.Config.from_yaml(self.yaml_file)
        assert config.boatd
