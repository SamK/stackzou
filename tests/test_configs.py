"""Test suite"""
from invoke import MockContext
from tests.lib import chdir
from stackzou import configs


def test_configs_local_files():
    c = MockContext()
    c.env = "toto"
    with chdir("examples"):
        result = configs.local_files(c)
    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], configs.Config)
