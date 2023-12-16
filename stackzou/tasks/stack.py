"""
On gère la stack docker par ici
"""
from invoke import task
from stackzou import docker, stack


@task(name="name")
def name_(c):
    """Print the name of the stack"""
    print(stack.name(c.env))


@task(help={"command_args": 'exemple: -c "--no-trunc"'})
def ps(c, command_args=None):
    """
    Fait un "docker stack ps"
    """
    client = docker.Docker(c)
    client.ps(stack.name(c.env), command_args)


@task
def rm(c):
    """Fait un "docker stack rm" """
    client = docker.Docker(c)
    client.rm(stack.name(c.env))


@task
def deploy(c):
    """
    déploie la stack mais ne fait pas la config ou la validation
    """
    client = docker.Docker(c)
    client.deploy(stack.name(c.env))
