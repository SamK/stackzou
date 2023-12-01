"""
Here lie Invoke commands with no subcommands.
"""
from invoke import task
from . import configs, stack

@task(pre=[configs.create], post=[stack.deploy])
def deploy(c):
    pass


@task(name="env")
def set_env(c, env):
    """
    Define the environment to manipulate.

    For a list of environments, execute `ls envs`.
    """
    c.env = env
