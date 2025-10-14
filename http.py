import socket

class Http:
    def __init__(self, host="0.0.0.0", port=8082):
        self.host = host
        self.port = port
        self.start_server()

    def start_server(self):
        s = socket.socket()
        s.bind((self.host, self.port))
        s.listen(5)
        print(f"🌐 服务器启动：http://{self.host}:{self.port}")

        while True:
            conn, addr = s.accept()
            print("🔗 新连接：", addr)
            with conn:
                request = conn.recv(4096).decode("utf-8", errors="ignore")
                if not request:
                    continue

                # 解析请求
                first_line = request.split("\r\n", 1)[0]
                try:
                    method, path, _ = first_line.split(" ", 2)
                except ValueError:
                    continue

                # 调用子类定义的处理逻辑，获取响应内容
                resp = self.handle_request(method, path)
                if resp:  # 确保不是 None
                    conn.sendall(resp)

    def response(self, body, status="200 OK"):
        return (
            f"HTTP/1.1 {status}\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body.encode())}\r\n"
            "Connection: close\r\n\r\n"
            f"{body}"
        ).encode("utf-8")

    def handle_request(self, method, path):
        if path == "/":
            return self.getRoot(path)
        else:
            return self.get404(path)

    def getRoot(self, path):
        body = "<h1>Default Root</h1>"
        return self.response(body)

    def get404(self, path):
        body = "<h1>404 Not Found</h1>"
        return self.response(body, "404 Not Found")
