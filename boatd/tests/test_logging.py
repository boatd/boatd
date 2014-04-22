import os
import shutil

import boatd

class MockBoat(object):
    def __init__(self):
        self.pos = 0

    def position(self):
        self.pos += 1
        return (self.pos, self.pos)

class TestGpxLogging(object):
    def setup(self):
        self.boat = MockBoat()
        self.conf = boatd.Config.from_yaml('boatd-config.yaml')

        base_name = self.conf.boatd.log.gpx.filename
        self.log_dir, name = os.path.split(base_name)
        if os.path.exists(self.log_dir):
            #make sure the log directory is clean
            shutil.rmtree(self.log_dir)

        self.logger = boatd.logging.GpxLogger(self.boat, base_name)

    def test_mock(self):
        assert self.boat.position() == (1, 1)

    def test_correct_config_file(self):
        assert self.conf.name == 'boatd-test-config'

    def test_dir_created(self):
        assert os.path.exists(self.log_dir)
