"""
Define env vars for

- docker command settings
- compose variable interpolation

"""
import os
import sys
from pathlib import Path
from stackzou import stack
from stackzou import log


def envpath(c):
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
        # sys.exit(127)

    for file_ in files:
        if file_.endswith(".env"):
            if basename:
                return_value.append(file_)
            else:
                return_value.append("/".join([path, file_]))

    return return_value


def find_envfiles(c):
    """Retourne une list de envfiles existants pour un environement défini"""
    secret_file = f"{Path.home()}/.secrets/containers/{stack.name(c.env)}.env"
    env_dir = f"envs/{c.env}"
    found_envfiles = []
    found_envfiles.extend(dir_(env_dir, basename=False))
    found_envfiles.extend(dir_(".", basename=True))
    if os.path.exists(secret_file):
        found_envfiles.append(secret_file)
    return found_envfiles


def cmd_prefix(c):
    """
    Fais les trucs de variable d'environnement
    """
    files = find_envfiles(c)
    return_value = ""
    prefix = "set -o allexport && source"
    suffix = " && "

    if not files:
        return ""

    for env_file in files:
        return_value += f" {env_file}"

    return_value = prefix + return_value + suffix

    return return_value
