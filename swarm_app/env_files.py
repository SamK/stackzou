"""
Define env vars for

- docker command settings
- compose variable interpolation

"""
import os
import sys
from invoke import task


def path(c):
    """
    Return the path to the current environment
    """
    return f"envs/{c.env}"


def list_(env, basename):
    """
    Return une liste de fichiers env existants

    * env: le nom de l'env
    * basename à True pour uniquement le fichier
    * basename à False pour le chemin complet
    """
    return_value = []

    # Cherche dans le env

    env_dir = f"envs/{env}"

    try:
        files = os.listdir(env_dir)
    except FileNotFoundError as e:
        print(f"Environment '{env}' is not defined locally: {e}", file=sys.stderr)
        envs = os.listdir("envs")
        print(f"Available envs: {envs}", file=sys.stderr)
        sys.exit(127)

    for file_ in files:
        if file_.endswith(".env"):
            if basename:
                return_value.append(file_)
            else:
                return_value.append("/".join([env_dir, file_]))

    # charnge dans "."
    files = os.listdir(".")
    for file_ in files:
        if file_.endswith(".env"):
            if basename:
                return_value.append(file_)
            else:
                return_value.append("/".join([env_dir, file_]))

    return return_value


@task(name="list")
def list__(c):  # avec 2 underscore LOLILOL
    """List env files of a specific env"""
    print(list_(c.env, basename=True))


def cmd_prefix(env):
    """
    Fais les trucs de variable d'environnement
    """
    return_value = ""
    prefix = "export $(cat"
    suffix = ");"

    files = list_(env, basename=True)
    if not files:
        return ""

    for env_file in files:
        return_value += f" {env_file}"

    return_value = prefix + return_value + suffix

    return return_value
