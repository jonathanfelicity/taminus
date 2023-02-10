class Response:
    def __init__(self):
        self.status_code = 404
        self.headers = []
        self.text = "Page Not Found"

    def send(self, status_code, headers, text):
        self.status_code = status_code
        self.headers = headers
        self.text = text
