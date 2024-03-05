"""
Subcommands related to the Docker Stack
"""

from invoke import task
from stackzou import docker, stack


@task(name="name")
def name_(c):
    """
    Print the name of the stack

    Requires a defined environment.
    """
    print(stack.name(c.env))


@task(help={"command_args": 'exemple: -c "--no-trunc"'})
def ps(c, command_args=None):
    """
    Show the current tasks: execute "docker stack ps"
    """
    client = docker.Docker(c)
    client.ps(stack.name(c.env), command_args)


@task
def rm(c):
    """Remove a stack: execute "docker stack rm" """
    client = docker.Docker(c)
    client.rm(stack.name(c.env))


@task
def deploy(c):
    """
    Deploy the Docker Stack
    """
    client = docker.Docker(c)
    client.deploy(stack.name(c.env))
