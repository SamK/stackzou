"""Test suite"""

from invoke import MockContext
from tests.lib import chdir
from stackzou import configs


def test_configs_local_files():
    """
    Make sure configs.local_files() can read local config files
    """
    c = MockContext()
    c.env = "toto"
    with chdir("examples"):
        result = configs.local_files(c)
    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], configs.Config)
    assert result[0].path == "configs/file.txt"
