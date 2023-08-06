from sidemash_sdk.SecureAndNonSecure import SecureAndNonSecure
from typing import Dict
import json


class PublishRtmp:
    def __init__(self,
                 stream_key_prefix: str,
                 ip: SecureAndNonSecure,
                 domain: SecureAndNonSecure):
        self._type = "PublishRtmp" 
        self.stream_key_prefix = stream_key_prefix
        self.ip = ip
        self.domain = domain

    @staticmethod
    def _type(): 
        return "PublishRtmp"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return PublishRtmp.from_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('streamKeyPrefix', self.stream_key_prefix),
            ('ip', self.ip.__to_remote_dict()),
            ('domain', self.domain.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('stream_key_prefix', self.stream_key_prefix),
            ('ip', self.ip.to_dict()),
            ('domain', self.domain.to_dict())
        ])

    @staticmethod
    def __from_remote_dict(d: Dict[str, any]):
        return PublishRtmp(d["streamKeyPrefix"],
                           SecureAndNonSecure.__from_remote_dict(d["ip"]),
                           SecureAndNonSecure.__from_remote_dict(d["domain"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return PublishRtmp(d["stream_key_prefix"],
                           SecureAndNonSecure.from_dict(d["ip"]),
                           SecureAndNonSecure.from_dict(d["domain"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("PublishRtmp(stream_key_prefix=" + self.stream_key_prefix + 
                            ", ip=" + repr(self.ip) + 
                            ", domain=" + repr(self.domain) + ")")