from http import Http

HOST, PORT = "0.0.0.0", 8082

def getRoot():
    body = "<h1>Hello</h1>"
    return body

def getHello():
    body = "<h1>Hello World</h1>"
    return body

http = Http(HOST, PORT)

http.routes = {
    "/": getRoot,
    "/hello": getHello,
}

http.run()
