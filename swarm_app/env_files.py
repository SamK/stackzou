"""
Define env vars for

- docker command settings
- compose variable interpolation

"""
import os
from invoke import task


def list(env):
    """
    Return the env files for a specifc env
    """
    env_dir = f"envs/{env}"
    return_value = ["env"]
    files = os.listdir(env_dir)

    for file_ in files:
        return_value.append("/".join([env_dir, file_]))
    return return_value


@task(name="list")
def list_(c, env):
    print(list(env))


def cmd_prefix(env):
    """
    Fais les trucs de variable d'environnement
    """
    return_value = ""
    prefix = "eval $( cat"
    suffix = ")"

    files = list(env)
    if not files:
        return ""

    for env_file in list(env):
        return_value += f" {env_file}"

    return_value = prefix + return_value + suffix

    return return_value
