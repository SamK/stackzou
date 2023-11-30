"""
Manipule les "docker configs" et génère les fichiers vars qui vont bien.
"""
import os
import hashlib
from io import StringIO
from invoke import task
from invoke.exceptions import UnexpectedExit
from slugify import slugify
from . import docker, stack, rc_file


def local_files():
    """
    Return a list of config files dicts.

    The dicts have these keys:
    - path: the path to the file
    - key: the key of the file (without hash)
    - value: the content
    - hash: a unique identifier based on the file properties
    """
    config_files_path = "configs"
    result = []
    for dir_path, _, file_names in os.walk(config_files_path):
        for file_name in file_names:
            this_config = {}
            this_config["path"] = "/".join([dir_path, file_name])
            this_config["key"] = slugify(this_config["path"], separator="_").upper()
            with open(this_config["path"], "r") as file:
                this_config["value"] = file.read()
            this_config["hash"] = hashlib.md5(
                this_config["path"].encode() + this_config["value"].encode()
            ).hexdigest()[:8]
            result.append(this_config)
    return result


@task(name="list")
def list_(c):
    """List docker configs"""
    client = docker.Docker(c)
    stack_name = stack.name(c.env)
    client.configs_list(stack_name)


@task
def create(c):
    """
    Create Docker configs

    Create docker configs (docker config list)

    """
    # find all the files

    envvars = {}

    for local_file in local_files():
        print(stack.name(c.env))

        local_file[
            "name"
        ] = f"{stack.name(c.env)}_{local_file['key']}-{local_file['hash']}"

        print(local_file["name"])
        client = docker.Docker(c)

        # Create docker configs
        try:
            result = client.configs_create(
                name=local_file["name"], in_stream=StringIO(local_file["value"])
            )
            docker_config_id = result
            print(f"Config {local_file['name']} updated with id {docker_config_id}.")
        # except invoke.exceptions.UnexpectedExit as e:
        except UnexpectedExit as e:
            if "AlreadyExists" in e.result.stderr:
                print(f"Config {local_file['name']} already exists.")
            else:
                raise

        # ca va dans le ficheir de env
        envvars[local_file["key"]] = local_file["name"]

    # write in env file
    envfile = f"envs/{c.env}/.configs.env"
    rc_file.RCFile(envfile).write(envvars, append=False)
    c.run(f"cat {envfile}")
