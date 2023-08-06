class BaseExceptions(Exception):
    pass


class AuthException(BaseException):
    """Raised when an api method requires authentication"""

    pass


class DeleteException(BaseException):
    """Raised when the delete of an object fails"""

    pass


class UpsertException(BaseException):
    """Raised when the combined insert or update fails"""

    pass


class NotFoundException(BaseException):
    """Raised when objects cannot be found by the API"""

    pass
