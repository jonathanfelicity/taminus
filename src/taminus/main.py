from wsgiref.util import shift_path_info
from wsgiref.headers import Headers
from wsgiref.simple_server import make_server

from utils import Response

class Taminus:
    def __init__(self):
        self.routes = {}

    def default_response(self, res):
        res.send(404, [("Content-Type", "text/plain")], "Page Not Found")

    def route(self, path, methods=["GET"], view=None):
        if view is not None:
            self.routes[path] = {m: view for m in methods}

        def decorator(view_func):
            self.routes[path] = {m: view_func for m in methods}
            return view_func

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
