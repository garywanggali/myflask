from http import Http

HOST = "0.0.0.0"
PORT = 8082

class MyHttp(Http):
    def getRoot(self, path):
        body = f"<h1>Hello</h1><p>Path={path}</p>"
        print("➡️ getRoot called")
        return self.response(body)

    def get404(self, path):
        body = f"<h1>404 Not Found</h1><p>Path={path}</p>"
        print("➡️ get404 called")
        return self.response(body, "404 Not Found")

MyHttp(HOST, PORT)
