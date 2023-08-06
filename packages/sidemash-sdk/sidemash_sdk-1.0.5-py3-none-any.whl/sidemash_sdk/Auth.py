from typing import Dict
import json


class Auth:
    def __init__(self, token: str, private_key: str):
        self._type = "Auth" 
        self.token = token
        self.private_key = private_key

    @staticmethod
    def _type(): 
        return "Auth"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Auth.from_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('token', self.token),
            ('privateKey', self.private_key)
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('token', self.token),
            ('private_key', self.private_key)
        ])

    @staticmethod
    def __from_remote_dict(d: Dict[str, any]):
        return Auth(d["token"],
                    d["privateKey"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Auth(d["token"],
                    d["private_key"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("Auth(token=" + self.token + 
                     ", private_key=******" + ")")