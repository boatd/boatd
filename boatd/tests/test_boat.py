import unittest

import boatd

from .driver import TestDriver


class TestBoat(unittest.TestCase):
    def setUp(self):
        self.boat = boatd.Boat(TestDriver())
        self.boat.update_cached_values()

    def test_get_heading(self):
        assert self.boat.heading() == 2.43

    def test_active(self):
        assert not self.boat.active
