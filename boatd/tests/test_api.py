try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

import threading

import boatd

class MockBoat(object):
    def __init__(self):
        self.heading = 45

class TestAPI(object):
    TEST_PORTS = 10
    def __init__(self):
        self.port = 2222

    def setup(self):
        for _ in range(self.TEST_PORTS):
            try:
                httpd = boatd.BoatdHTTPServer(MockBoat(), ('', self.port),
                            boatd.BoatdRequestHandler)
                break
            except Exception, e:
                self.port += 1

        self.http_thread = threading.Thread(target=httpd.handle_request)
        self.http_thread.daemon = True
        self.http_thread.start()

    def test_thread(self):
        assert self.http_thread.is_alive()

    def test_GET(self):
        assert urlopen('http://localhost:2222').read()
