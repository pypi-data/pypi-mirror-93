__version__ = "0.0.1"
__all__ = []

from .pyfileindex import PyFileIndex

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
