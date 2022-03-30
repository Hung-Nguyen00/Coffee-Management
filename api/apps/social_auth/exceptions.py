from apps.core.exceptions import GenericException


class MissedAccessTokenOrProviderException(GenericException):
    code = 3001
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "access_token and provider is required"
        super().__init__(message=message)


class ProviderNotDefinedException(GenericException):
    code = 3002
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "provider is not found"
        super().__init__(message=message)


class IncorrectDataException(GenericException):
    code = 3003
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Incorrect data"
        super().__init__(message=message)


class MissedEmailException(GenericException):
    code = 3004
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Email is required"
        super().__init__(message=message)


class LogInException(GenericException):
    code = 3005
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Unable to log in with provided credentials."
        super().__init__(message=message)


class SocialDomainInvalidException(GenericException):
    code = 3006
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Unable to log in with invalid domain."
        super().__init__(message=message)
