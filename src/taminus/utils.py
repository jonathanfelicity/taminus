

def json(res, data):
    """
        Returns a json object
    """
    res.content_type = 'text/json'
    res.json = data
    res

def send(res, data):
    res.content_type = 'text/html'
    res.text = data
    return res

