from http import MiniApp

HOST, PORT = "0.0.0.0", 8082

def getRoot():
    return "<h1>Hello</h1>"

def getHello():
    return "<h1>Hello World</h1>"

http = MiniApp()

http.routes = {
    "/": getRoot,
    "/hello": getHello,
}

http.run(HOST, PORT)
