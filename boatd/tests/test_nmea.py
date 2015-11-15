import datetime
import unittest

import boatd


class TestNMEA(unittest.TestCase):
    def test_hdm(self):
        assert boatd.nmea.hdm(49.6) == '$HDM,49.6,M*19'

    def test_degrees_to_nmea(self):
        assert boatd.nmea.degrees_to_nmea(45.555) == '4533.3'

    def test_negative_degrees_to_nmea(self):
        assert boatd.nmea.degrees_to_nmea(-45.555) == '-4533.3'

    def test_gll(self):
        date = datetime.datetime(2014, 6, 7, 22, 22, 1, 152642)
        assert boatd.nmea.gll(38.063413, -122.240910, date) == \
            '$GLL,383.8,N,12214.5,W,222201.15,A*35'
