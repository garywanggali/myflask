import socket
from functools import wraps

class MiniApp:
    def __init__(self):
        self.routes = {}  # 保存 path -> function

    def route(self, path):
        def decorator(func):
            self.routes[path] = func
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def run(self, host="0.0.0.0", port=8000):
        s = socket.socket()
        s.bind((host, port))
        s.listen(5)
        print(f"🌐 MiniApp running on http://{host}:{port}")

        while True:
            conn, addr = s.accept()
            with conn:
                request = conn.recv(4096).decode("utf-8", errors="ignore")
                if not request:
                    continue

                first_line = request.split("\r\n", 1)[0]
                try:
                    method, path, _ = first_line.split(" ", 2)
                except ValueError:
                    continue

                if path in self.routes:
                    body = self.routes[path]()
                    resp = self._response(body)
                else:
                    resp = self._response(f"<h1>404 Not Found</h1><p>Path={path}</p>", "404 Not Found")

                conn.sendall(resp)

    def _response(self, body, status="200 OK"):
        return (
            f"HTTP/1.1 {status}\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body.encode())}\r\n"
            "Connection: close\r\n\r\n"
            f"{body}"
        ).encode("utf-8")
