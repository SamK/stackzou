"""
Define env vars for

- docker command settings
- compose variable interpolation

"""
from invoke import task
from stackzou import env_files


@task(name="list")
def list_(c):  # avec 2 underscore LOLILOL
    """List env files of a specific env"""
    print(env_files.find_envfiles(c))
