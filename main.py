from http import MiniApp, Request
from html import escape

app = MiniApp()

@app.route("/")
def index(request):
    return "<h1>Welcome to MiniApp</h1><p>Try /hello?name=World</p>"

@app.route("/hello")
def hello(request: Request):
    # 从 request.args 获取 GET 参数
    name = request.args.get("name", "Flask")
    return f"<h1>Hello, {escape(name)}!</h1>"

app.run("0.0.0.0", 8000)
