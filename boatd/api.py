try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

import logging
import json


class BoatdHTTPServer(HTTPServer):
    def __init__(self, boat,
            server_address, RequestHandlerClass, bind_and_activate=True):

        HTTPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.boat = boat

        self.handles = {
            '/': self.boatd_info,
            '/heading': self.boat_heading
        }

    def boat_heading(self):
        return {'heading': self.boat.heading()}

    def boatd_info(self):
        return {'boatd': {'version': 0.1}}

    def boat_function(self, function_string):
        '''Return the encoded json response from an endpoint string.'''
        json_content = self.handles.get(function_string)()
        return json.dumps(json_content).encode()


class BoatdRequestHandler(BaseHTTPRequestHandler):
    server_version = 'boatd/0.1'

    def send_json(self, content):
        self.send_response(200)
        self.send_header('Content-Type', 'application/JSON')
        self.end_headers()
        self.request.sendall(content)

    def do_GET(self, *args, **kwargs):
        '''Handle a GET request to the server'''
        if self.path in self.server.handles:
            self.send_json(self.server.boat_function(self.path))
        else:
            print('fail')

    def do_POST(self):
        '''Handle a POST request to the server'''
        length = int(self.headers.getheader('content-length'))
        data = json.loads(self.rfile.read(length))
        print(data)

    def log_request(self, code='-', size='-'):
        logging.log('REST request {}'.format(self.path), level=logging.VERBOSE)

if __name__ == '__main__':
    class BoatMock(object):
        def __init__(self):
            self.heading = 24.23

    httpd = BoatdHTTPServer(BoatMock(), ('', 2222),
        BoatdRequestHandler)
    httpd.serve_forever()
