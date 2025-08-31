
class MappingBusinessException(Exception):
    message: str
    statusCode: int

    def __init__(self, message: str):
        self.message = message
        self.statusCode = 400

    def __str__(self):
        return self.message


class AiClientAuthenticationException(Exception):
    message: str
    statusCode: int

    def __init__(self, message: str):
        self.message = message
        self.statusCode = 400

    def __str__(self):
        return self.message
