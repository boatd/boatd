import os
import unittest
import time

import boatd.behaviour


class TestBehaviour(unittest.TestCase):
    def setUp(self):
        self.directory, _ = os.path.split(__file__)
        self.behaviour_file = os.path.join(self.directory, 'mock_behaviour')

    def test_start(self):
        behaviour = boatd.behaviour.Behaviour('mock_behaviour',
                                              self.behaviour_file)
        behaviour.start()

        # give it a little time to start up
        time.sleep(1)

        # not terminated yet
        assert behaviour.process.poll() == None

        # end the behaviour
        behaviour.end()

        # SIGTERM
        assert behaviour.process.poll() == -15

        # check behaviour was actually executed
        assert os.path.isfile('/tmp/mock_file')
        os.remove('/tmp/mock_file')
