import boatd
import unittest

class TestUtils(unittest.TestCase):
    def test_reldir(self):
        assert boatd.utils.reldir('test/thing.py', 'dir') == 'test/dir'
