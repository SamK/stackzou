"""Test suite"""

from invoke import MockContext
from stackzou.tasks import stack
from tests.lib import chdir


def test_tasks_stack_name_(capfd):
    c = MockContext()
    c.env = "toto"
    with chdir("examples"):
        stack.name_(c)
    out, _ = capfd.readouterr()
    assert out == "examples-toto\n"
