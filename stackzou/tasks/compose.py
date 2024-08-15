"""
Subcommands related to the docker-compose.yml file
"""

from invoke import task  # type: ignore[attr-defined]
from invoke.context import Context
from stackzou import docker


@task
def show(c: Context, skip_interpolation=False) -> None:
    """Render and print the docker-compose.yml file"""
    client = docker.Docker(c)
    if skip_interpolation:
        client.stack_args += " --skip-interpolation"
    client.show()
