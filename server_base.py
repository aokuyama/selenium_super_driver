from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json

def ready(handler):
    address = ('', 3000)
    with HTTPServer(address, handler) as server:
        server.serve_forever()

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('path = {}'.format(self.path))

        parsed_path = urlparse(self.path)
        print('parsed: path = {}, query = {}'.format(parsed_path.path, parse_qs(parsed_path.query)))

        print('headers\r\n-----\r\n{}-----'.format(self.headers))
       
        response = self.get_response(parsed_path.path, parsed_path.query)

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(response)

    def do_POST(self):
        print('path = {}'.format(self.path))

        parsed_path = urlparse(self.path)
        print('parsed: path = {}, query = {}'.format(parsed_path.path, parse_qs(parsed_path.query)))

        print('headers\r\n-----\r\n{}-----'.format(self.headers))

        content_length = int(self.headers['content-length'])
        
        print('body = {}'.format(self.rfile.read(content_length).decode('utf-8')))
        
        response = self.post_response(parsed_path.path, parse_qs(parsed_path.query))

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        res = json.dumps(response)
        self.wfile.write(res.encode('utf-8'))

    def get_response(self, path, query):
        return b"NG"

    def post_response(self, path, query):
        return []
