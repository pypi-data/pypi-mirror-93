from typing import Dict
import json


class HttpMethod:
    def __init__(self, value: str):
        self._type = "HttpMethod" 
        self.value = value

    @staticmethod
    def GET():
        return HttpMethod("GET")

    @staticmethod
    def POST():
        return HttpMethod("POST")

    @staticmethod
    def PUT():
        return HttpMethod("PUT")

    @staticmethod
    def DELETE():
        return HttpMethod("DELETE")

    @staticmethod
    def PATCH():
        return HttpMethod("PATCH")

    @staticmethod
    def all_possibles_values():
        return {"GET",
                "POST",
                "PUT",
                "DELETE",
                "PATCH"}

    @staticmethod
    def from_string(value):
        if value == "GET": return HttpMethod.GET()
        elif value == "POST": return HttpMethod.POST()
        elif value == "PUT": return HttpMethod.PUT()
        elif value == "DELETE": return HttpMethod.DELETE()
        elif value == "PATCH": return HttpMethod.PATCH()
        else: return None

    @staticmethod
    def is_valid(value):
        return value in HttpMethod.all_possibles_values()

    def is_not_get(self):
        return self.value != "GET"

    def is_not_post(self):
        return self.value != "POST"

    def is_not_put(self):
        return self.value != "PUT"

    def is_not_delete(self):
        return self.value != "DELETE"

    def is_not_patch(self):
        return self.value != "PATCH"

    def is_get(self):
        return self.value == "GET"

    def is_post(self):
        return self.value == "POST"

    def is_put(self):
        return self.value == "PUT"

    def is_delete(self):
        return self.value == "DELETE"

    def is_patch(self):
        return self.value == "PATCH"

    def to_json(self):
        return json.dumps(self.value)

    def __to_remote_json(self):
        return json.dumps(self.value)

    def to_string(self):
        return self.__repr__()

    def __repr__(self):
        return "HttpMethod(value=" + self.value + ")"

    def __str__(self):
        return self.value