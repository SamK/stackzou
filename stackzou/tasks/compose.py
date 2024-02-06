"""
Subcommands related to the docker-compose.yml file
"""
from invoke import task
from stackzou import docker


@task
def show(c):
    """Render and print the docker-compose.yml file"""
    client = docker.Docker(c)
    client.show()
