# Base exception for all security-related errors
class BaseSecurityError(Exception):
    pass


# Password-related exceptions
class PasswordTooShortError(BaseSecurityError):
    def __init__(self, message="Password must be at least 8 characters long."):
        self.message = message
        super().__init__(self.message)


class PasswordMissingUppercaseError(BaseSecurityError):
    def __init__(self, message="Password must contain at least one uppercase letter."):
        self.message = message
        super().__init__(self.message)


class PasswordMissingLowercaseError(BaseSecurityError):
    def __init__(self, message="Password must contain at least one lowercase letter."):
        self.message = message
        super().__init__(self.message)


class PasswordMissingDigitError(BaseSecurityError):
    def __init__(self, message="Password must contain at least one digit."):
        self.message = message
        super().__init__(self.message)


class PasswordMissingSpecialCharError(BaseSecurityError):
    def __init__(self, message="Password must contain at least one special character."):
        self.message = message
        super().__init__(self.message)


# Token-related exceptions
class InvalidTokenError(BaseSecurityError):
    def __init__(self, message="Invalid or malformed token."):
        self.message = message
        super().__init__(self.message)


class TokenExpiredError(BaseSecurityError):
    def __init__(self, message="Token has expired."):
        self.message = message
        super().__init__(self.message)
