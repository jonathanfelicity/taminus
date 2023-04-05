from taminus import Taminus



app = Taminus()

def index(req, res):
    res.send(200, [("Content-Type", "text/plain")], "Hello, world!")

app.route("/", view=index)


app.serve()
