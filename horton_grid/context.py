import os
import pkg_resources
from glob import glob

__all__ = ["context", "Context"]


class Context(object):
    """Finds out where the data directory is located etc.

    The data directory contains data files with standard basis sets and
    pseudo potentials.
    """

    def __init__(self):
        # Determine data directory (also for in-place build)
        self.data_dir = pkg_resources.resource_filename(__name__, "data")
        self.include_dir = pkg_resources.resource_filename(__name__, "include")

        # Check if directories exist
        if not pkg_resources.resource_isdir(__name__, "data"):
            raise IOError(
                "Can not find the data files. The directory %s does not exist." % self.data_dir
            )

    def get_fn(self, filename):
        """Return the full path to the given filename in the data directory."""
        return os.path.join(self.data_dir, filename)

    def glob(self, pattern):
        """Return all files in the data directory that match the given pattern."""
        return glob(self.get_fn(pattern))

    def get_include(self):
        """Return the list with directories containing header files (.h and .pxd)"""
        return self.include_dir


context = Context()
