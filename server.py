from http.server import HTTPServer
from importlib import import_module
import os

address = ('', 3000)
module = import_module(os.environ['REQUEST_HANDLER'])
with HTTPServer(address, module.HTTPRequestHandler) as server:
    server.serve_forever()
