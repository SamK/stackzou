from invoke import task
from swarm_app import env_files, docker, stack


@task
def show(c):
    client = docker.Docker(c)
    client.show()


@task
def validate(c):
    cmd_prefix = env_files.cmd_prefix(c.env)
    command = f"{cmd_prefix} docker-compose config --quiet"
    ignore = ["Compose does not support 'configs' configuration", ""]

    result = c.run(command, hide="stderr")
    for line in result.stderr.split("\n"):
        if any(word in line for word in ignore):
            pass
        else:
            print(line, file=sys.stderr)
