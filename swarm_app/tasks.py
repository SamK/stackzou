"""
Here lie Invoke commands with no subcommands.
"""
from invoke import task


@task(name="env")
def set_env(c, env):
    """
    Define the environment to manipulate.

    For a list of environments, execute `ls envs`.
    """
    c.env = env
