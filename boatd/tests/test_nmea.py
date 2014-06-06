import boatd

def test_hdm():
    assert boatd.nmea.hdm(49.6) == '$HDM,49.6,M*19'

def test_degrees_to_nmea():
    assert boatd.nmea.degrees_to_nmea(45.555) == '4533.3'
