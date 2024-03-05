"""Test suite for the env_files"""

import os
from contextlib import AbstractContextManager


# https://stackoverflow.com/a/72163496/238913
class chdir(AbstractContextManager):  # pylint: disable=invalid-name
    """Non thread-safe context manager to change the current working directory."""

    def __init__(self, path):
        self.path = path
        self._old_cwd = []

    def __enter__(self):
        self._old_cwd.append(os.getcwd())
        os.chdir(self.path)

    def __exit__(self, *excinfo):
        os.chdir(self._old_cwd.pop())
