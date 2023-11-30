import os
from invoke import task
from swarm_app import configs, docker, env_files


def name(env):
    remove = "-deploy$"
    value = os.path.basename(os.getcwd())
    value = value.removesuffix("-deploy")
    value = f"{value}-{env}"
    return value


@task(name="name")
def name_(c, env):
    print(name(env))


@task
def ps(c, env):
    client = docker.Docker(c, env)
    client.ps(name(env))


@task
def deploy(c, env):
    """
    déploie la stack mais ne fait pas la config ou la validation
    """
    client = docker.Docker(c, env)
    client.deploy(name(env))
