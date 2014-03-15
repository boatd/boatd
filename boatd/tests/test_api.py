try:
    from urllib.request import urlopen
    from urllib.request import HTTPError
    from urllib.request import Request
except ImportError:
    from urllib2 import urlopen
    from urllib2 import HTTPError
    from urllib2 import Request

import threading
import socket
import json

import boatd


class MockBoat(object):
    class NestedClass(object):
        def __init__(self):
            self.thing = lambda: 'well hello there'

    def __init__(self):
        self.nest = self.NestedClass()
        self.heading = lambda: 45
        self.pony = lambda: 'magic'
        self.rudder_angle = 20

    def rudder(r):
        self.rudder_angle = r


class TestAPI(object):
    TEST_PORTS = 10

    def __init__(self):
        self.port = 2222

    def setup(self):
        for _ in range(self.TEST_PORTS):
            try:
                self.httpd = boatd.BoatdHTTPServer(MockBoat(), ('', self.port),
                                                   boatd.BoatdRequestHandler)
                break
            except socket.error:
                self.port += 1

        self.http_thread = threading.Thread(target=self.httpd.handle_request)
        self.http_thread.daemon = True
        self.http_thread.start()

    def _base_url(self):
        return 'http://localhost:{}'.format(self.port)

    def _url(self, endpoint):
        return self._base_url() + endpoint

    def _post_string(self, string):
        post_data = string.encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        request = Request(self._base_url(), post_data, headers)
        return urlopen(request)

    def test_thread(self):
        assert self.http_thread.is_alive()

    def test_GET(self):
        assert urlopen(self._base_url()).read()

    def test_valid_json(self):
        content = urlopen(self._base_url()).read()
        d = json.loads(content.decode("utf-8"))
        assert 'boatd' in d

    def test_request_pony(self):
        content = urlopen(self._url('/pony')).read()
        d = json.loads(content.decode("utf-8"))
        assert d.get('result') == 'magic'

    def test_request_nested(self):
        content = urlopen(self._url('/nest/thing')).read()
        d = json.loads(content.decode("utf-8"))
        assert d.get('result') == 'well hello there'

    def test_request_nonexistant(self):
        try:
            urlopen(self._url('/does_not_exist'))
            assert '404 code returned' == True
        except HTTPError as e:
            assert e.code == 404

    def test_request_heading(self):
        content = urlopen(self._url('/heading')).read()
        d = json.loads(content.decode("utf-8"))
        assert d.get('heading') == 45

    def test_content_type(self):
        m = urlopen(self._url('/heading')).info()
        assert m['content-type'] == 'application/JSON'

    def test_response_code(self):
        code = urlopen(self._url('/heading')).getcode()
        assert code == 200

    def test_quit(self):
        status_json = self._post_string(json.dumps({'quit': True})).read()
        status = json.loads(status_json)
        assert status['quit'] == True
        assert self.httpd.running == False
