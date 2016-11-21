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
import unittest

import boatd


class MockBoat(object):
    class NestedClass(object):
        def __init__(self):
            self.thing = lambda: 'well hello there'

    def __init__(self):
        self.active = False
        self.nest = self.NestedClass()
        self.heading = lambda: 45
        self.wind_apparent = lambda: 23.12
        self.wind_absolute = lambda: 180.3
        self.position = lambda: (2.2312, -23.2323)
        self.pony = lambda: 'magic'
        self.rudder_angle = 20

    def rudder(self, r):
        self.rudder_angle = r


class TestAPI(unittest.TestCase):
    TEST_PORTS = 50

    @classmethod
    def setUpClass(cls):
        cls.port = 2222

    def setUp(self):
        self.boat = MockBoat()
        for _ in range(self.TEST_PORTS):
            try:
                self.httpd = boatd.BoatdHTTPServer(self.boat, object,
                                                   object,
                                                   ('', self.port),
                                                   boatd.BoatdRequestHandler)
                break
            except socket.error as e:
                print('socket {} didn\'t work, trying a higher one '
                      '({})'.format(self.port, e))
                self.port += 1

        self.http_thread = threading.Thread(target=self.httpd.handle_request)
        self.http_thread.daemon = True
        self.http_thread.start()

    def _base_url(self):
        return 'http://localhost:{}'.format(self.port)

    def _url(self, endpoint):
        return self._base_url() + endpoint

    def _post_string(self, string, endpoint=None):
        if endpoint is not None:
            url = self._base_url() + endpoint
        else:
            url = self._base_url()

        post_data = string.encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        request = Request(url, post_data, headers)
        return urlopen(request)

    def test_thread(self):
        assert self.http_thread.is_alive()

    def test_GET(self):
        assert urlopen(self._base_url()).read()

    def test_valid_json(self):
        content = urlopen(self._base_url()).read()
        d = json.loads(content.decode("utf-8"))
        assert 'boatd' in d

    def test_version(self):
        content = urlopen(self._url('/')).read()
        d = json.loads(content.decode("utf-8"))
        assert d['boatd']['version'] == 1.3

    def test_request_pony(self):
        content = urlopen(self._url('/pony')).read()
        d = json.loads(content.decode("utf-8"))
        assert d.get('result') == 'magic'

    def test_request_active(self):
        content = urlopen(self._url('/active')).read()
        d = json.loads(content.decode("utf-8"))
        assert type(d.get('value')) is bool

    def test_request_boat(self):
        content = urlopen(self._url('/boat')).read()
        d = json.loads(content.decode("utf-8"))
        assert all([attr in d for attr in ['heading', 'wind', 'position']])

    def test_request_wind(self):
        content = urlopen(self._url('/wind')).read()
        d = json.loads(content.decode("utf-8"))
        assert all([attr in d for attr in ['direction', 'speed']])

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
        assert d.get('result') == 45

    def test_content_type(self):
        m = urlopen(self._url('/heading')).info()
        assert m['content-type'] == 'application/JSON'

    def test_response_code(self):
        code = urlopen(self._url('/heading')).getcode()
        assert code == 200

    def test_quit(self):
        status_json = self._post_string(json.dumps({'quit': True})).read()
        status = json.loads(status_json.decode("utf-8"))
        assert status['quit'] == True
        assert self.httpd.running == False

    def test_set_rudder(self):
        assert self.boat.rudder_angle == 20
        content = json.dumps({'value': 32})
        request = self._post_string(content, endpoint='/rudder')
        status = json.loads(request.read().decode("utf-8"))
        assert self.boat.rudder_angle == 32

    def test_reject_bad_json(self):
        content = '''{"value: something bad}'''
        try:
            code = self._post_string(content, endpoint='/rudder').getcode()
            assert '400 code returned' == True
        except HTTPError as e:
            assert e.code == 400
