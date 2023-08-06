from sidemash_sdk.Timestamp import Timestamp
from typing import Dict
import json


class UTCDateTime:
    def __init__(self, iso8601: str, timestamp: Timestamp):
        self._type = "UTCDateTime" 
        self.iso8601 = iso8601
        self.timestamp = timestamp

    @staticmethod
    def _type(): 
        return "UTCDateTime"

    @staticmethod
    def from_json(js: str):
        value = json.loads(js)
        return UTCDateTime.from_dict(value)

    def __to_remote_dict(self):
        tuples = [
            ('iso8601', self.iso8601),
            ('timestamp', self.timestamp.__to_remote_dict())
        ]
        return dict(t for t in tuples if t[1] is not None)

    def to_dict(self):
        return dict([
            ('iso8601', self.iso8601),
            ('timestamp', self.timestamp.to_dict())
        ])

    @staticmethod
    def __from_remote_dict(d: Dict[str, any]):
        return UTCDateTime(d["iso8601"],
                           Timestamp.__from_remote_dict(d["timestamp"]))

    @staticmethod
    def from_dict(d: Dict[str, any]):
        return UTCDateTime(d["iso8601"],
                           Timestamp.from_dict(d["timestamp"]))

    def to_json(self):
        return json.dumps(self.to_dict())

    def __to_remote_json(self):
        return json.dumps(self.__to_remote_dict())

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return ("UTCDateTime(iso8601=" + self.iso8601 + 
                            ", timestamp=" + repr(self.timestamp) + ")")