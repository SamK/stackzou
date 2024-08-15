"""
Here lie Invoke commands with no subcommands.
"""

from invoke import task, call  # type: ignore[attr-defined]
from invoke.context import Context
from stackzou import docker
from stackzou import stack as stackzou_stack
from . import configs, stack


@task(pre=[configs.create], post=[stack.deploy])
def deploy(c: Context) -> None:  # pylint: disable=unused-argument
    """
    A shortcut for "configs.create stack.deploy"
    """


@task(pre=[call(stack.ps_, format_="cclines")])
def ps(_):
    """
    raccourci pour "stack.ps -c cclines"
    """


@task(name="env")
def set_env(c: Context, env: str) -> None:
    """
    Define the environment to manipulate.

    For a list of environments, execute `ls envs`.
    """
    c.env = env


@task
def verbose(c: Context) -> None:
    """Enable verbose mode"""
    if "loglevel" in c:
        c.loglevel += 1
    else:
        c.loglevel = 1
