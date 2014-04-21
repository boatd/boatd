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

        log_dir = os.path.dirname(self.conf.boatd.log.gpx.filename)
        if os.path.isdir(log_dir):
            #make sure the log directory is clean
            shutil.rmtree(log_dir)

    def test_mock(self):
        assert self.boat.position() == (1, 1)

    def test_correct_config_file(self):
        assert self.conf.name == 'boatd-test-config'
