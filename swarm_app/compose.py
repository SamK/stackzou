from invoke import task
from swarm_app import env_files, docker, stack


@task
def show(c, env):
    client = docker.Docker(c, env)
    client.show()


@task
def validate(c, env):
    cmd_prefix = env_files.cmd_prefix(env)
    command = f"{cmd_prefix} docker-compose config --quiet"
    ignore = ["Compose does not support 'configs' configuration", ""]

    result = c.run(command, hide="stderr")
    for line in result.stderr.split("\n"):
        if any(word in line for word in ignore):
            pass
        else:
            print(line, file=sys.stderr)
