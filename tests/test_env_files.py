"""Test suite"""

from invoke import MockContext
from stackzou import env_files
from tests.lib import chdir


def test_envpath():
    c = MockContext()
    c.env = "toto"
    assert env_files.envpath(c) == "envs/toto"


def test_dir_empty():
    """
    Make sure env_files.list returns nothing when there is not env file
    """
    path = "envs/simple"
    with chdir("examples"):
        res = env_files.dir_(path, True)
    assert isinstance(res, list)
    assert len(res) == 0


def test_dir_():
    """
    Make sure env_files.list finds the appropriate env files
    """
    path = "envs/vars"
    with chdir("examples"):
        res = env_files.dir_(path, True)
    assert res == ["vars.env"]
