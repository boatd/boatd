import threading

import boatd

class MockBoat(object):
    def __init__(self):
        self.heading = 45

class TestAPI(object):
    def setup(self):
        httpd = boatd.BoatdHTTPServer(MockBoat(), ('', 2222),
                    boatd.BoatdRequestHandler)
        self.http_thread = threading.Thread(target=httpd.handle_request)
        self.http_thread.daemon = True
        self.http_thread.start()

    def test_thread(self):
        assert self.http_thread.is_alive()
