from sidemash_sdk.Auth import Auth
from sidemash_sdk.StreamSquareService import StreamSquareService


class Client:
    def __init__(self, auth: Auth):
        self._type = "Client" 
        self.auth = auth
        self._stream_square = StreamSquareService(auth)

    def stream_square(self):
        return self._stream_square

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "Client(auth=" + repr(self.auth) + ")"