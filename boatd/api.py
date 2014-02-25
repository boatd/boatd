from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

class BoatdRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self, *args, **kwargs):
        print('Requested', self.path)
        self.send_response(200)
        self.send_header('Content-Type', 'application/JSON')
        self.end_headers()
        self.request.sendall('hi there')

if __name__ == '__main__':
    httpd = HTTPServer(('', 8000),
            BoatdRequestHandler)
    httpd.serve_forever()
