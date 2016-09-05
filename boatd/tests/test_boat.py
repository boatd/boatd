import unittest

import boatd

class MockDriver(object):
    def heading(self):
        return 2.43

class TestBoat(unittest.TestCase):
    def setUp(self):
        self.boat = boatd.Boat(MockDriver())
        self.boat.update_cached_values()

    def test_get_heading(self):
        assert self.boat.heading() == 2.43

    def test_active(self):
        assert not self.boat.active
