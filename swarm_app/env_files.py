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


def list_(path, basename):
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


@task(name="list")
def list__(c):  # avec 2 underscore LOLILOL
    """List env files of a specific env"""
    env_dir = f"envs/{c.env}"
    env_files = list_(env_dir, basename=False)
    default_files = list_(".", basename=True)
    print(env_files + default_files)


def cmd_prefix(env):
    """
    Fais les trucs de variable d'environnement
    """
    return_value = ""
    prefix = "export $(cat"
    suffix = ") && "

    env_dir = f"envs/{env}"
    env_files = list_(env_dir, basename=False)
    default_files = list_(".", basename=True)

    files = env_files + default_files

    if not files:
        return ""

    for env_file in files:
        return_value += f" {env_file}"

    return_value = prefix + return_value + suffix

    return return_value
