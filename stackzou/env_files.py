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
    """Retourne une list de envfiles existants relatifs à l'environment actuel"""
    secret_file = f"{Path.home()}/.secrets/containers/{stack.name(c.env)}.env"
    env_dir = f"envs/{c.env}"
    found_envfiles = []
    found_envfiles.extend(dir_(".", basename=True))
    found_envfiles.extend(dir_(env_dir, basename=False))
    if os.path.exists(secret_file):
        found_envfiles.append(secret_file)
    log.log1(c, f"Found env files: {found_envfiles}")
    return found_envfiles


def cmd_prefix(c, suffix=" && "):
    """
    Fais les trucs de variable d'environnement
    """
    files = find_envfiles(c)
    commands = ["set -o allexport"]

    if not files:
        return ""

    for env_file in files:
        commands.append(f"source {env_file}")

    command_line = " && ".join(commands)
    command_line += suffix

    return command_line
