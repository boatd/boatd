try:
    from urllib.request import urlopen
    from urllib.request import HTTPError
    from urllib.request import Request
except ImportError:
    from urllib2 import urlopen
    from urllib2 import HTTPError
    from urllib2 import Request

import json
import time
import threading
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
        self.target_rudder_angle = 0.0
        self.target_sail_angle = 20.0

    def rudder(self, r):
        self.rudder_angle = r


class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.port = 2222
        cls.boat = MockBoat()

        cls.api = boatd.BoatdAPI(cls.boat, object,
                                 object,
                                 ('', cls.port))

        cls.http_thread = threading.Thread(target=cls.api.run)
        cls.http_thread.daemon = True
        cls.http_thread.start()

        # Block main thread while server starts
        time.sleep(3)


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
        return urlopen(request, timeout=1)

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

    def test_request_boat(self):
        content = urlopen(self._url('/boat')).read()
        d = json.loads(content.decode("utf-8"))
        assert all([attr in d for attr in ['heading', 'wind', 'position']])

    def test_request_wind(self):
        content = urlopen(self._url('/wind')).read()
        d = json.loads(content.decode("utf-8"))
        assert all([attr in d for attr in ['absolute', 'apparent', 'speed']])

    def test_request_nonexistant(self):
        try:
            urlopen(self._url('/does_not_exist'))
            assert '404 code returned' == True
        except HTTPError as e:
            assert e.code == 404

    def test_content_type(self):
        m = urlopen(self._url('/sail')).info()
        assert m['content-type'] == 'application/json; charset=UTF-8'

    def test_response_code(self):
        code = urlopen(self._url('/sail')).getcode()
        assert code == 200

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
