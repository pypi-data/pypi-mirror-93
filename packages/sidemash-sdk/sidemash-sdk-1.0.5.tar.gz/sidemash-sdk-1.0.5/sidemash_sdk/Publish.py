from sidemash_sdk.PublishRtmp import PublishRtmp
from typing import Dict
import json


class Publish:
    def __init__(self, rtmp: PublishRtmp):
        self._type = "Publish" 
        self.rtmp = rtmp

    @staticmethod
    def _type(): 
        return "Publish"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return Publish.from_dict(value)

    def __to_remote_dict(self):
        tuples = [('rtmp', self.rtmp.__to_remote_dict())]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([('rtmp', self.rtmp.to_dict())])

    @staticmethod
    def __from_remote_dict(d: Dict[str, any]):
        return Publish(PublishRtmp.__from_remote_dict(d["rtmp"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return Publish(PublishRtmp.from_dict(d["rtmp"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Publish(rtmp=" + repr(self.rtmp) + ")"