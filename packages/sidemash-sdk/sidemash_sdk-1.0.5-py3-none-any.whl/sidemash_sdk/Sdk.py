
class Sdk:
    @staticmethod
    def version():
        return "v1.0"

    @staticmethod
    def host():
        return "dev-api.sidemash.io"

    @staticmethod
    def base_url(): 
        return "https://" + Sdk.host()

