# Base exception for all email-related errors
class BaseEmailError(Exception):
    pass


class InvalidEmailFormatError(BaseEmailError):
    def __init__(self, message="Invalid email format provided."):
        self.message = message
        super().__init__(self.message)
