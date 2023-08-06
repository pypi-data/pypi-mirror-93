from abc import ABC, abstractmethod
from sidemash_sdk.HttpMethod import HttpMethod
from typing import Dict
import json


class Hook(ABC):
    def is_http_call(self):
        return self._type == HttpCall._type()

    def is_not_http_call(self):
        return self._type != HttpCall._type()

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Hook.from_dict(value)

    def __to_remote_dict(self):
        pass

    def to_dict(self):
        pass

    @staticmethod
    def __from_remote_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == HttpCall._type(): return HttpCall.from_dict(d)
        else: raise ValueError("Invalid dict submitted for creating 'Hook'" + " Unexpected '_type' = " + ty)

    @staticmethod
    def from_dict(d: Dict[str, any]):
        ty = d['_type']
        if ty == HttpCall._type(): return HttpCall.from_dict(d)
        else: raise ValueError("Invalid dict submitted for creating 'Hook'" + " Unexpected '_type' = " + ty)

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())



class HttpCall:
    def __init__(self, method: HttpMethod, url: str):
        self._type = "Hook.HttpCall" 
        self.method = method
        self.url = url

    @staticmethod
    def _type(): 
        return "Hook.HttpCall"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return HttpCall.from_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('method', str(self.method)),
            ('url', self.url)
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('method', str(self.method)),
            ('url', self.url)
        ])

    @staticmethod
    def __from_remote_dict(d: Dict[str, any]):
        return HttpCall(HttpMethod.from_string(d["method"]),
                        d["url"])

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return HttpCall(HttpMethod.from_string(d["method"]),
                        d["url"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("HttpCall(method=" + repr(self.method) + 
                         ", url=" + self.url + ")")