import boatd

class MockBoat(object):
    def __init__(self):
        self.pos = 0

    def position(self):
        self.pos += 1
        return (self.pos, self.pos)

class TestLogging(object):
    def setup(self):
        self.boat = MockBoat()

    def test_mock(self):
        assert self.boat.position() == (1, 1)
