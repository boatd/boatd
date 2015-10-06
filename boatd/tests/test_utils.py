import boatd

class TestUtils(object):
    def test_reldir(self):
        assert boatd.utils.reldir('test/thing.py', 'dir') == 'test/dir'
