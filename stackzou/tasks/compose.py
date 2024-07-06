"""
Subcommands related to the docker-compose.yml file
"""

from invoke import task
from stackzou import docker


@task
def show(c, skip_interpolation=False):
    """Render and print the docker-compose.yml file"""
    client = docker.Docker(c)
    if skip_interpolation:
        client.stack_args += " --skip-interpolation"
    client.show()
