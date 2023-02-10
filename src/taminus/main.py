from wsgiref.util import shift_path_info
from wsgiref.headers import Headers
from wsgiref.simple_server import make_server
import logging
import atexit


from utils import Response

class Taminus:
    def __init__(self):
        self.routes = {}

    def default_response(self, res):
        res.send(404, [], "Page Not Found")

    def router(self, path, view):
        self.routes[path] = view
        return view

    def __call__(self, environ, start_response):
        req = {}
        req["path"] = environ["PATH_INFO"]
        req["method"] = environ["REQUEST_METHOD"]
        req["headers"] = environ.items()

        res = Response()
        for path, view in self.routes.items():
            if path == req["path"]:
                view(req, res)
                break
        else:
            self.default_response(res)

        start_response(f"{res.status_code} {res.text}", [(str(k), str(v)) for k, v in res.headers])
        return [res.text.encode()]

    def serve(app, host='localhost', port=8000):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(message)s',
                            handlers=[logging.StreamHandler()])
        
        server = make_server(host, port, app)
        logging.info(f"Serving on http://{host}:{port}")

        def stop_server():
            server.shutdown()
            server.server_close()

        atexit.register(stop_server)
        server.serve_forever()

    

   



app = Taminus()


def index(req, res):
    res.send(200, [], "<h1>Hello Home</h1>")

def about(req, res):
    res.send(200, [], "<h1>Hello About</h1>")

def king(req, res):
    res.send(200, [], "<h1>Hello King</h1>")

app.router("/", index)
app.router("/about", about)
app.router("/king", king)

if __name__ == '__main__':
    app.serve("", 8000)
