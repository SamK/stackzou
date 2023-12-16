"""
Manipule le fichier docker-compose.yml
"""
from invoke import task
from stackzou import docker


@task
def show(c):
    """Affiche le fichier docker-compose.yml rendered"""
    client = docker.Docker(c)
    client.show()
