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
        return {'heading': self.boat.heading}

    def boatd_info(self):
        return {'boatd': {'version': 0.1}}


class BoatdRequestHandler(BaseHTTPRequestHandler):
    server_version = 'boatd/0.1'

    def do_GET(self, *args, **kwargs):
        if self.path in self.server.handles:
            self.send_response(200)
            self.send_header('Content-Type', 'application/JSON')
            self.end_headers()
            json_content = self.server.handles.get(self.path)()
            self.request.sendall(json.dumps(json_content).encode())
        else:
            print('fail')

    def log_request(self, code='-', size='-'):
        logging.log('REST request {}'.format(self.path), level=logging.VERBOSE)

if __name__ == '__main__':
    class BoatMock(object):
        def __init__(self):
            self.heading = 24.23

    httpd = BoatdHTTPServer(BoatMock(), ('', 2222),
        BoatdRequestHandler)
    httpd.serve_forever()
