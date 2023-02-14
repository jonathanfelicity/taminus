from status import STATUS_CODES
class Response:
    def __init__(self, body=""):
        self.status_code = 200
        self.status_text = "OK"
        self.headers = {}
        self.body = body

    def send(self, status_code, headers, body):
        self.status_code = status_code
        self.status_text = STATUS_CODES.get(status_code, "Unknown")
        self.headers.update(headers)
        self.body = body