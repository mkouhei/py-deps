# -*- coding: utf-8 -*-
"""py_deps.exceptions module."""


class Error(Exception):

    """Base error class."""

    def __init__(self, message=None):
        """Initialize."""
        super(Error, self).__init__(message)


class NotFound(Error):

    """Not Found."""

    pass


class BrokenPackage(Error):

    """BrokenPackage."""

    pass
