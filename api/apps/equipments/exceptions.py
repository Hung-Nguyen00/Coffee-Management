from apps.core.exceptions import GenericException


class MaterialNotEmptyException(GenericException):
    code = 2000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "The materials is not empty."
        super().__init__(message=message)
        
        
class MaterialDoesNotExistsException(GenericException):
    code = 2001
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "The materials does not exist."
        super().__init__(message=message)
        

class BillDetailDoesNotExistsException(GenericException):
    code = 2002
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "This item does not exist in the bill."
        super().__init__(message=message)
