# /psqtraviscontainer/directory.py
#
# Utilities for safe directory navigation.
#
# See /LICENCE.md for Copyright information
"""Utilities for safe directory navigation."""

import errno

import os


def safe_makedirs(path):
    """Make directories without throwing if a directory exists."""
    try:
        os.makedirs(path)
    except OSError as err:
        if err.errno != errno.EEXIST:  # suppress(PYC90)
            raise err


def safe_touch(path):
    """Create a file without throwing if it exists."""
    safe_makedirs(os.path.dirname(path))
    if not os.path.exists(path):
        with open(path, "w") as fileobj:
            fileobj.write("")


class Navigation(object):  # pylint:disable=R0903
    """Context manager to enter and exit directories."""

    def __init__(self, path):
        """Initialize the path we want to change to."""
        super(Navigation, self).__init__()
        self._path = path
        self._current_dir = None

    def __enter__(self):
        """Upon entry, attempt to create the directory and then enter it."""
        safe_makedirs(self._path)
        self._current_dir = os.getcwd()
        os.chdir(self._path)

        return self._path

    def __exit__(self, exc_type, value, traceback):
        """Pop directory on exiting with statement."""
        del exc_type
        del traceback
        del value

        os.chdir(self._current_dir)
