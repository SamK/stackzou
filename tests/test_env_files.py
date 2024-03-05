"""Test suite"""

from invoke import MockContext
from stackzou import env_files
from tests.lib import chdir


def test_envpath():
    c = MockContext()
    c.env = "toto"
    assert env_files.envpath(c) == "envs/toto"


def test_dir_empty():
    path = "envs/simple"
    with chdir("examples"):
        res = env_files.dir_(path, True)
    assert isinstance(res, list)
    if ".configs.env" in res:
        assert len(res) == 1
    else:
        assert len(res) == 0


def test_dir_():
    path = "envs/vars"
    with chdir("examples"):
        res = env_files.dir_(path, True)
    assert res == ["vars.env"]
