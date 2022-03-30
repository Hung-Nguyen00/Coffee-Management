from apps.core.exceptions import GenericException


class MissedUsernameOrEmailException(GenericException):
    code = 2000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Username or email is required."
        super().__init__(message=message)


class EmailToResetNotExistException(GenericException):
    code = 2001
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "This e-mail address does not exist."
        super().__init__(message=message)


class EmailRegisteredNotVerifiedException(GenericException):
    code = 2002
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "This e-mail address is not verified. Please check your mailbox."
        super().__init__(message=message)


class PasswordsNotMatchException(GenericException):
    code = 2003
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "The two password fields didn't match."
        super().__init__(message=message)


class UsernameRegisteredWithThisEmailException(GenericException):
    code = 2004
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "A user is already registered with this e-mail address."
        super().__init__(message=message)


class UsernameAlreadyExistException(GenericException):
    code = 2005
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Username is already existed."
        super().__init__(message=message)


class PasswordValidateError(GenericException):
    code = 2006
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Password is not valid. Please try again."
        super().__init__(message=message)


class EmailValidateError(GenericException):
    code = 2007
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Email is not valid. Please try again."
        super().__init__(message=message)


class UserAccountDisabledException(GenericException):
    code = 2008
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "User account is disabled."
        super().__init__(message=message)


class LogInException(GenericException):
    code = 2009
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Unable to log in with provided credentials."
        super().__init__(message=message)


class PasswordException(GenericException):
    code = 2010
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Please enter the current password correctly"
        super().__init__(message=message)


class PasswordResetOTPException(GenericException):
    code = 2011
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Unable to reset password."
        super().__init__(message=message)


class PasswordResetOTPInvalidException(GenericException):
    code = 2012
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "This OTP code is invalid or verified."
        super().__init__(message=message)


class PasswordResetOTPExpiredException(GenericException):
    code = 2013
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "This OTP code is expired. Please request new code."
        super().__init__(message=message)


class PhoneAlreadyExistException(GenericException):
    code = 2014
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "This phone is already registered with another user."
        super().__init__(message=message)


class PhoneInvalidException(GenericException):
    code = 2015
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "This phone is invalid."
        super().__init__(message=message)


class UserNotExistsException(GenericException):
    code = 2016
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "User does not exist"
        super().__init__(message=message)


class RoleDoesNotExist(GenericException):
    code = 2017
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Role does not exist"
        super().__init__(message=message)
