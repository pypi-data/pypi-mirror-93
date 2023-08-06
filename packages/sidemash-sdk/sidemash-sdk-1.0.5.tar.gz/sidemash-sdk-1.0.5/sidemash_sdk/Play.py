from typing import Dict
import json


class Play:
    def __init__(self, todo: int):
        self._type = "Play" 
        self.todo = todo

    @staticmethod
    def _type(): 
        return "Play"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Play.from_dict(value)

    def __to_remote_dict(self):
        tuples = [('todo', self.todo)]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([('todo', self.todo)])

    @staticmethod
    def __from_remote_dict(d: Dict[str, any]):
        return Play(d["todo"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Play(d["todo"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Play(todo=" + str(self.todo) + ")"