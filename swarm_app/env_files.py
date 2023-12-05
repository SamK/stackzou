"""
Define env vars for

- docker command settings
- compose variable interpolation

"""
import os
import sys
from pathlib import Path
from invoke import task
from swarm_app import stack


def path(c):
    """
    Return the path to the current environment
    """
    return f"envs/{c.env}"


def dir_(path, basename):
    """
    Return une liste de fichiers env existants dans un dossier

    * env: le nom de l'env
    * basename à True pour uniquement le fichier
    * basename à False pour le chemin complet
    """
    return_value = []

    # Cherche dans le env

    try:
        files = os.listdir(path)
    except FileNotFoundError as e:
        print(f"Folder not found: '{path}': {e}", file=sys.stderr)
        raise
        sys.exit(127)

    for file_ in files:
        if file_.endswith(".env"):
            if basename:
                return_value.append(file_)
            else:
                return_value.append("/".join([path, file_]))

    return return_value


def find_envfiles(c):
    secret_file = f"{Path.home()}/.secrets/containers/{stack.name(c.env)}.env"
    env_dir = f"envs/{c.env}"
    found_envfiles = []
    found_envfiles.extend(dir_(env_dir, basename=False))
    found_envfiles.extend(dir_(".", basename=True))
    if os.path.exists(secret_file):
        found_envfiles.append(secret_file)
    return found_envfiles


@task(name="list")
def list_(c):  # avec 2 underscore LOLILOL
    """List env files of a specific env"""
    print(find_envfiles(c))


def cmd_prefix(c):
    """
    Fais les trucs de variable d'environnement
    """
    files = find_envfiles(c)
    return_value = ""
    prefix = "export $(cat"
    suffix = ") && "

    if not files:
        return ""

    for env_file in files:
        return_value += f" {env_file}"

    return_value = prefix + return_value + suffix

    return return_value
