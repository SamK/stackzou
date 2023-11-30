"""
Define env vars for

- docker command settings
- compose variable interpolation

"""
import os
import sys
from invoke import task


def list_(env):
    """
    Return the env files for a specifc env
    """
    default_env_file = "env"
    env_dir = f"envs/{env}"
    return_value = []

    if os.path.exists(default_env_file):
        return_value.append(default_env_file)

    try:
        files = os.listdir(env_dir)
    except FileNotFoundError as e:
        print(f"Environment '{env}' is not defined locally: {e}", file=sys.stderr)
        envs = os.listdir("envs")
        print(f"Available envs: {envs}", file=sys.stderr)
        sys.exit(127)

    for file_ in files:
        if file_.endswith(".env"):
            return_value.append("/".join([env_dir, file_]))
    return return_value


@task(name="list")
def list__(c):  # avec 2 underscore LOLILOL
    """List env files of a specific env"""
    print(list_(c.env))


def cmd_prefix(env):
    """
    Fais les trucs de variable d'environnement
    """
    return_value = ""
    prefix = "eval $( cat"
    suffix = ")"

    files = list_(env)
    if not files:
        return ""

    for env_file in files:
        return_value += f" {env_file}"

    return_value = prefix + return_value + suffix

    return return_value
