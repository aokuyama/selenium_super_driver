import server_base

class HTTPRequestHandler(server_base.HTTPRequestHandler):
    def get_response(self, path, query):
        return b"OK"

    def post_response(self, path, query):
        print(query)
        return query

server_base.ready(HTTPRequestHandler)
