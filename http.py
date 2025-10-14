import socket

class Http:
    def __init__(self, host="0.0.0.0", port=8082):
        self.host = host
        self.port = port
        self.routes = {}  # 路由字典
        print(f"🌐 HTTP server ready on http://{self.host}:{self.port}")

    def run(self):
        s = socket.socket()
        s.bind((self.host, self.port))
        s.listen(5)
        print("🚀 Server running...")

        while True:
            conn, addr = s.accept()
            print("🔗 Connected:", addr)
            with conn:
                request = conn.recv(4096).decode("utf-8", errors="ignore")
                if not request:
                    continue

                # 解析请求行
                first_line = request.split("\r\n", 1)[0]
                try:
                    method, path, _ = first_line.split(" ", 2)
                except ValueError:
                    continue

                # 处理请求
                resp = self.handle_request(path)
                conn.sendall(resp)

    def handle_request(self, path):
        if path in self.routes:
            body = self.routes[path]()  # 调用注册的函数
            return self.response(body)
        else:
            # 找不到路由 → 404
            return self.get404(path)

    def response(self, body, status="200 OK"):
        return (
            f"HTTP/1.1 {status}\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body.encode())}\r\n"
            "Connection: close\r\n\r\n"
            f"{body}"
        ).encode("utf-8")

    def get404(self, path):
        """默认 404"""
        body = f"<h1>404 Not Found</h1><p>Path={path}</p>"
        return self.response(body, "404 Not Found")
