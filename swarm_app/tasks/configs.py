"""
Manipule les "docker configs" et génère les fichiers vars qui vont bien.
"""
import sys
import pathlib
from io import StringIO
from invoke import task
from invoke.exceptions import UnexpectedExit
from swarm_app import docker, stack, rc_file
from swarm_app import configs


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
    envfile = f"envs/{c.env}/.configs.env"
    envvars = {}

    # find all the files

    for local_file in configs.local_files():
        if "env" not in c:
            print("ya pas de env lol. il faut spécifier un env", file=sys.stderr)
            sys.exit(127)

        local_file[
            "name"
        ] = f"{stack.name(c.env)}_{local_file['key']}-{local_file['hash']}"

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

    if envvars:
        # write in env file and show the result on screen
        rc_file.RCFile(envfile).write(envvars, append=False)
        c.run(f"cat {envfile}")
    else:
        # no env vars, make sure the file does not exist
        pathlib.Path(envfile).unlink(missing_ok=True)
