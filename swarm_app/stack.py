import os
from invoke import task
from swarm_app import docker


def name(env):
    value = os.path.basename(os.getcwd())
    value = value.removesuffix("-deploy")
    value = f"{value}-{env}"
    return value


@task(name="name")
def name_(c):
    print(name(c.env))


@task(help={"command_args": 'exemple: -c "--no-trunc"'})
def ps(c, command_args=None):
    """
    Fait un "docker stack ps"
    """
    client = docker.Docker(c)
    client.ps(name(c.env), command_args)


@task
def deploy(c):
    """
    déploie la stack mais ne fait pas la config ou la validation
    """
    client = docker.Docker(c)
    client.deploy(name(c.env))
