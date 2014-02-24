from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

class BoatdRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self, *args, **kwargs):
        print('Requested', self.path)

if __name__ == '__main__':
    httpd = HTTPServer(('', 8000),
            BoatdRequestHandler)
    httpd.serve_forever()
