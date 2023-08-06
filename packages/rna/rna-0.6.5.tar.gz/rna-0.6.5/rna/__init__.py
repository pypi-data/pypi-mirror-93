"""Top-level package of rna."""

__author__ = """Daniel Böckenhoff"""
__email__ = "dboe@ipp.mpg.de"
__version__ = "0.6.5"

from . import plotting
from . import log  # NOQA
from . import path  # NOQA
from . import process  # NOQA
from . import pattern  # NOQA
from . import polymorphism  # NOQA

plotting.use("matplotlib")
