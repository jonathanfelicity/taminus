# Taminus
Taminus is a lightweight web framework for Python that provides a simple way to build web applications. It's designed to be easy to use and flexible enough to accommodate a wide variety of use cases.

## Installation
You can install Taminus using pip:

```bash
pip install taminus
```

## Quickstart
To get started with Taminus, create a new Python file and import the Taminus class:

```python
from taminus import Taminus

app = Taminus()
```
You can then define a view function that will be called when a request is received:

```python
def index(req, res):
    res.send(200, [("Content-Type", "text/plain")], "Hello, world!")
```
To route requests to this view function, use the route() method:

```python
app.route("/", view=index)
```
Finally, start the server:

```python
app.serve()
```
That's it! You now have a basic Taminus web application up and running.

## Routing
Taminus uses a simple routing system to map URLs to view functions. The route() method takes a path and a view function, and associates the path with the view function. You can also specify the HTTP methods that the view function should handle (by default, it handles only GET requests):


```python
@app.route("/", methods=["GET", "POST"])
def index(req, res):
    # ...
```
Inside the view function, you can access the request data through the req argument and use the res argument to send a response:

```python
@app.route("/")
def index(req, res):
    res.send(200, [("Content-Type", "text/html")], "<h1>Hello, world!</h1>")
```
## Request and Response Objects
The req object passed to view functions contains information about the incoming request, including the request method, headers, and query parameters. The res object is used to send a response back to the client.

Here's an example view function that uses both the req and res objects:

```python
@app.route("/")
def index(req, res):
    name = req.get_param("name") or "world"
    res.send(200, [("Content-Type", "text/html")], f"<h1>Hello, {name}!</h1>")
```
In this example, the view function retrieves a query parameter named name from the req object (or uses the default value "world" if the parameter is not present). It then uses the res object to send an HTML response back to the client.

## Static Files
Taminus can also serve static files, such as CSS and JavaScript files. To do this, use the serve_static() method and specify the directory where your static files are stored:

```python
app.serve_static("/static", "path/to/static/files")
```
In this example, Taminus will serve any files in the path/to/static/files directory when the URL starts with /static. For example, if you have a file named style.css in the path/to/static/files directory, you can include it in an HTML file like this:

```html
<link rel="stylesheet" href="/static/style.css">
```
### Contributing
If you'd like to contribute to Taminus, please feel free to submit a pull request. You can also open an issue if you encounter a bug or have a feature request.