"""Custom exceptions raised by WayPy."""


class WayPyError(Exception):
    """Base exception for package-specific errors."""


class InvalidGraphError(WayPyError, ValueError):
    """Raised when graph input cannot be converted to a valid adjacency list."""


class UnknownSearchMethodError(WayPyError, ValueError):
    """Raised when a search method name is not supported."""
