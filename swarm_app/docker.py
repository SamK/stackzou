from invoke import task
from swarm_app import configs, env_files


class Docker(object):
    def __init__(self, c, env):
        self.c = c
        self.env = env
        self.c.config.runners.local.input_sleep = 0
        self.cmd_prefix = env_files.cmd_prefix(env)

    def run(self, command, **kwargs):
        result = self.c.run(command, **kwargs)

    def configs_create(self, name, in_stream):
        command = f"{self.cmd_prefix} time docker config create {name} -"
        result = self.run(command, in_stream=in_stream, hide="both")
        return result.stdout.strip()

    def configs_list(self, stack_name):
        command = f"{self.cmd_prefix} docker config list --format json --filter name={stack_name}"
        return self.run(command)

    def show(self):
        command = f"{self.cmd_prefix} docker-compose config"
        result = self.c.run(command)

    def ps(self, stack_name, cmd_args=None):
        command = f"{self.cmd_prefix} docker stack ps {stack_name}"
        if cmd_args:
            command = " ".join([command, cmd_args])
        return self.c.run(command)

    def deploy(self, stack_name):
        command = f"{self.cmd_prefix} docker stack deploy --prune {stack_name} --compose-file docker-compose.yml"
        return self.c.run(command)
