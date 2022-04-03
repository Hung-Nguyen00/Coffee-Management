from apps.core.exceptions import GenericException


class ScheduleStaffExistException(GenericException):
    code = 3000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "The staff exists in the schedule"
        super().__init__(message=message)


class SessionDoesNotExistException(GenericException):
    code = 3000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "These sessions does not exist."
        super().__init__(message=message)