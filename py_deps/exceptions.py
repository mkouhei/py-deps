# -*- coding: utf-8 -*-
"""py_deps.exceptions module."""


class Error(Exception):
    """Base error class."""

    pass


class NotFound(Error):
    """Not Found."""

    pass


class BrokenPackage(Error):
    """BrokenPackage."""

    pass


class InvalidMetadata(Error):
    """Invalid package metadata."""

    pass


class BackendFailure(Error):
    """PyPI service down."""

    pass
