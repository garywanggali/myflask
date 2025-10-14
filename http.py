import socket
from functools import wraps
from urllib.parse import urlparse, parse_qs
from html import escape

class Request:
    """封装 HTTP 请求信息"""
    def __init__(self, raw_path, method, headers, body):
        self.method = method
        self.headers = headers  # 原始头部字符串
        self.body = body
        url = urlparse(raw_path)
        self.path = url.path
        # 将 query 参数解析成字典，取第一个值
        self.args = {k: v[0] for k, v in parse_qs(url.query).items()}

class MiniApp:
    def __init__(self):
        self.routes = {}  # path -> function

    def route(self, path):
        """装饰器注册路由"""
        def decorator(func):
            self.routes[path] = func
            @wraps(func)
            def wrapper(request):
                return func(request)
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
                data = conn.recv(4096).decode("utf-8", errors="ignore")
                if not data:
                    continue

                # 解析请求行和头
                request_line, headers_rest = data.split("\r\n", 1)
                try:
                    method, raw_path, _ = request_line.split(" ", 2)
                except ValueError:
                    continue

                headers_str, _, body = headers_rest.partition("\r\n\r\n")

                # 构建 Request 对象
                req = Request(raw_path, method, headers_str, body)

                # 调用路由函数
                if req.path in self.routes:
                    body = self.routes[req.path](req)
                    resp = self._response(body)
                else:
                    resp = self._response(f"<h1>404 Not Found</h1><p>Path={req.path}</p>", "404 Not Found")

                conn.sendall(resp)

    def _response(self, body, status="200 OK"):
        return (
            f"HTTP/1.1 {status}\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body.encode())}\r\n"
            "Connection: close\r\n\r\n"
            f"{body}"
        ).encode("utf-8")
