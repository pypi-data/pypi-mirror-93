"""
quantnn.common
==============

Implements common features used by the other submodules of the ``quantnn``
package.
"""
class QuantnnException(Exception):
    """ Base exception for exception from the quantnn package."""


class UnknownArrayTypeException(QuantnnException):
    """Thrown when a function is called with an unsupported array type."""


class UnknownModuleException(QuantnnException):
    """
    Thrown when an unsupported backend is passed to a generic array
    operation.
    """

class UnsupportedBackendException(QuantnnException):
    """
    Thrown when quantnn is requested to load a backend that is not supported.

    """

class InvalidDimensionException(QuantnnException):
    """Thrown when an input array doesn't match expected shape."""

class ModelNotSupported(QuantnnException):
    """Thrown when a provided model isn't supported by the chosen backend."""

class MissingAuthenticationInfo(QuantnnException):
    """Thrown when required authentication information is not available."""

class DatasetError(QuantnnException):
    """
    Thrown when a given dataset object does not provide the expected interface.
    """

class InvalidURL(QuantnnException):
    """
    Thrown when a provided file URL is invalid.
    """
