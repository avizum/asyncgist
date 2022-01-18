class AsyncGistException(Exception):
    """
    Base Exception of the library.

    Can be theoretically used to catch all errors raised by this library.
    """
    pass


class HTTPExeption(AsyncGistException):
    """
    Base HTTP exception.

    Attributes
    ----------
    status: :class:`int`
        The HTTP error code.
    reason: :class:`str`
        The HTTP error reason.
    text: :class:`str`
        The text returned from the website.
    """
    def __init__(self, status: int, reason: str, text: str):
        self.status = status
        self.reason = reason
        self.text = text


class NotFound(HTTPExeption):
    pass


class Forbidden(HTTPExeption):
    pass
