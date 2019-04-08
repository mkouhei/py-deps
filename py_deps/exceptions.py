# -*- coding: utf-8 -*-
"""py_deps.exceptions module."""


class Error(Exception):
    """Base error class."""


class NotFound(Error):
    """Not Found."""


class BrokenPackage(Error):
    """BrokenPackage."""


class InvalidMetadata(Error):
    """Invalid package metadata."""


class BackendFailure(Error):
    """PyPI service down."""
