"""Top-level package of transcoding.

The transcoding library offers python file based descriptors for standardized file reading and
writing which can be shared an exchanged.
"""

__author__ = """Daniel Böckenhoff"""
__email__ = "dboe@ipp.mpg.de"
__version__ = "0.2.0"

from .trigger import *  # noqa
from .pattern import *  # noqa
from .core import *  # noqa
from . import transcodings  # noqa
