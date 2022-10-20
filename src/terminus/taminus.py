from webob import Request, Response

class Taminus:
    def __init__(self):
        self.routes = {}

    def default_response(self, res):
        res.status_code = 404
        res.text = "Page Not Found"

    def router(self, path, view):
        self.routes[path] = view
        return view

    def __call__(self, environ, start_response):
        req = Request(environ)
        
        res = self.request_handler(req)

        return res(environ, start_response)


    def request_handler(self, req):
        res = Response()
        for path, view in self.routes.items():
            if path == req.path:
                view(req, res)
                return res
        self.default_response(res)
        return res