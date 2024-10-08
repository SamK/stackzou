"""
Subcommands related to the Docker Configs.
"""

import sys
import pathlib
from io import StringIO
from invoke import task
from invoke.context import Context
from stackzou import docker, stack, rc_file
from stackzou import configs


@task(name="list")
def list_(c: Context) -> None:
    """List the docker configs"""
    client = docker.Docker(c)
    stack_name = stack.name(c.env)
    print(client.configs_list(stack_name))


@task
def show(c: Context, filename: str) -> None:
    """Print the properties of a file"""
    stack_name = stack.name(c.env)
    config = configs.Config(c, filename, stack_name)
    print(config)


@task
def create(c: Context) -> None:
    """Create the Docker Configs"""

    if "env" not in c:
        print("ya pas de env lol. il faut spécifier un env", file=sys.stderr)
        sys.exit(127)

    envfile = f"envs/{c.env}/.stackzou.env"
    envvars = {}
    stack_name = stack.name(c.env)
    client = docker.Docker(c)

    # find all the existin docker configs
    if "docker_configs" not in c:
        c.docker_configs = client.configs_list(stack_name)

    try:
        for local_file in configs.local_files(c):
            found = False
            for config in c.docker_configs:
                if config["Name"] == local_file.id:
                    found = True
                    break

            if not found:
                # Create docker configs
                result = client.configs_create(
                    name=local_file.id, in_stream=StringIO(local_file.value)
                )
                docker_config_id = result
                print(f"Config {local_file.id} updated with id {docker_config_id}.")

            # ca va dans le ficheir de env
            envvars[local_file.key] = local_file.id
    except UnicodeDecodeError:
        # there was an error message before
        sys.exit(4)

    if envvars:
        # write in env file and show the result on screen
        rc_file.RCFile(envfile).write(envvars, append=False)
        c.run(f"cat {envfile}")
    else:
        # no env vars, make sure the file does not exist
        pathlib.Path(envfile).unlink(missing_ok=True)
