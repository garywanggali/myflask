from http.server import BaseHTTPRequestHandler, HTTPServer

class myflask:
    def __init__(self, host, port):
        self.routes = {}
        self.host = host
        self.port = port

    def route(self, path, methods=["GET"]):
        def decorator(func):
            for method in methods:
                self.routes[(method.upper(), path)] = func
            return func
        return decorator

    def run(self):
        app = self

        class RequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.handle_request("GET")

            def do_POST(self):
                self.handle_request("POST")

            def handle_request(self, method):
                func = app.routes.get((method, self.path))
                if func:
                    try:
                        body = func()
                        if not isinstance(body, str):
                            body = str(body)

                        self.send_response(200)
                        self.send_header("Content-Type", "text/html; charset=utf-8")
                        self.end_headers()
                        self.wfile.write(body.encode("utf-8"))
                    except Exception as e:
                        self.send_error(500, f"Internal Server Error: {e}")
                else:
                    self.send_error(404, "Not Found")


        server = HTTPServer((self.host, self.port), RequestHandler)
        print(f"🚀 Server running at http://{self.host}:{self.port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped.")
            server.server_close()
