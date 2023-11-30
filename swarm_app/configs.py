from invoke import Collection, task
from . import docker, stack, rc_file
from slugify import slugify


# ns.add_task(toto)
# ns.add_collection(toto)
import hashlib
import sys
import os
import pprint
from io import StringIO
from invoke.exceptions import UnexpectedExit

import re


def local_files():
    config_files_path = "configs"
    result = []
    for dir_path, dir_names, file_names in os.walk(config_files_path):
        for file_name in file_names:
            this_config = {}
            this_config["path"] = "/".join([dir_path, file_name])
            this_config["key"] = slugify(this_config["path"], separator="_").upper()
            this_config["value"] = open(this_config["path"], "r").read()
            this_config["hash"] = hashlib.md5(
                this_config["value"].encode()
            ).hexdigest()[:8]
            result.append(this_config)
    return result


@task
def list(c, env):
    """List docker configs"""
    client = docker.Docker(c, env)
    stack_name = stack.name(env)
    client.configs_list(stack_name)


@task
def create(c, env):
    """
    Create Docker configs

    Create docker configs (docker config list)

    """
    # find all the files

    envvars = {}

    for local_file in local_files():
        print(stack.name(env))

        local_file[
            "name"
        ] = f"{stack.name(env)}_{local_file['key']}-{local_file['hash']}"

        print(local_file["name"])
        client = docker.Docker(c, env)

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
                pass
            else:
                raise

        # ca va dans le ficheir de env
        envvars[local_file["key"]] = local_file["name"]

    # write in env file
    envfile = f"envs/{env}/configs"
    rc_file.RC_File(envfile).write(envvars, append=False)
    c.run(f"cat {envfile}")
