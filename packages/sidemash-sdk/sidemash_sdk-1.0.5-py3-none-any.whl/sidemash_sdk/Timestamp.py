from typing import Dict
import json


class Timestamp:
    def __init__(self, seconds: int):
        self._type = "Timestamp" 
        self.seconds = seconds

    @staticmethod
    def _type(): 
        return "Timestamp"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Timestamp.from_dict(value)

    def __to_remote_dict(self):
        tuples = [('seconds', self.seconds)]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([('seconds', self.seconds)])

    @staticmethod
    def __from_remote_dict(d: Dict[str, any]):
        return Timestamp(d["seconds"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Timestamp(d["seconds"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Timestamp(seconds=" + str(self.seconds) + ")"