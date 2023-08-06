import json


class CircleResponse:
    def __init__(self, body, code, headers):
        self.body = body
        self.code = code
        self.headers = headers

        self.data = json.loads(body)["data"]

    @property
    def idempotency_key(self):
        try:
            return self.headers["idempotency-key"]
        except KeyError:
            return None
