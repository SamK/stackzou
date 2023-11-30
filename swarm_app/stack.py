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


@task(help={"env": "ENV", "command_args": 'exemple: -c "--no-trunc"'})
def ps(c, env, command_args=None):
    """
    Fait un "docker stack ps"
    """
    client = docker.Docker(c, env)
    client.ps(name(env), command_args)


@task
def deploy(c, env):
    """
    déploie la stack mais ne fait pas la config ou la validation
    """
    client = docker.Docker(c, env)
    client.deploy(name(env))
