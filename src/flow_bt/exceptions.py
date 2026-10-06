"""Custom exceptions for Flow BT."""


class Flow2ConnectionError(Exception):
    """Raised when connection to the device fails."""

    pass


class AuthenticationError(Exception):
    """Raised when authentication with the device fails."""

    pass


class NotConnectedError(Exception):
    """Raised when an operation is attempted while disconnected."""

    pass