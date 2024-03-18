class UserExceptions(Exception):
    """Base class for user-defined exceptions"""
    pass


class InvalidDataException(UserExceptions):
    """Exception raised for errors in the input data.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class PromptActionException(UserExceptions):
    """Exception raised for errors related to prompt action processing.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class SeleniumBrokenLinkException(UserExceptions):
    """Exception raised for errors related to prompt action processing.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UserExceptions(object):
    pass
