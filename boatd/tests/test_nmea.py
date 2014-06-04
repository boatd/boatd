import boatd

def test_hdm():
    assert boatd.nmea.hdm(49.6) == '$HDM,49.6,M*19'
