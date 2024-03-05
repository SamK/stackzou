"""Test suite"""

from tests.lib import chdir
from stackzou import stack


def test_stack_name():
    with chdir("examples"):
        res = stack.name("testenv")
    assert res == "examples-testenv"
