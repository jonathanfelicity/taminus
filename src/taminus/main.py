from wsgiref.util import shift_path_info
from wsgiref.headers import Headers
from wsgiref.simple_server import make_server

from utils import Response

class Taminus:
    def __init__(self):
        self.routes = {}

    def default_response(self, res):
        res.send(404, [("Content-Type", "text/plain")], "Page Not Found")

    def route(self, path, methods=["GET"]):
        def decorator(view):
            self.routes[path] = {m: view for m in methods}
            return view
        return decorator

    def __call__(self, environ, start_response):
        req = {}
        req["path"] = environ["PATH_INFO"]
        req["method"] = environ["REQUEST_METHOD"]
        req["headers"] = environ.items()

        res = Response()
        view = self.routes.get(req["path"], {}).get(req["method"])
        if view:
            view(req, res)
        else:
            self.default_response(res)

        start_response(f"{res.status_code} {res.status_text}", [(str(k), str(v)) for k, v in res.headers.items()])
        return [res.body.encode()]

    def serve(self, port=8000):
        try:
            with make_server('', port, self) as httpd:
                print(f"Serving on port {port}...")
                httpd.serve_forever()
        except OSError as e:
            if e.errno == 98:
                print(f"Port {port} is already in use")
            else:
                print(f"Failed to start server: {e}")
        except KeyboardInterrupt:
            print("Shutting down server...")
        finally:
            print("Server stopped")


app = Taminus()

@app.route("/")
def home(req, res):
    res.send(200, [("Content-Type", "text/html")], "<h1>Hello, World!</h1>")

@app.route("/about")
def about(req, res):
    res.send(200, [("Content-Type", "text/html")], "<h1>About Us</h1><p>We are a small web development company.</p>")

if __name__ == '__main__':
    app.serve()

