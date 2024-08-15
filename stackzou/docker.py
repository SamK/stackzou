""" Handle the docker client
"""

import json
from invoke.context import Context
from stackzou import env_files


class Docker:
    """
    Abstraction layer of the `docker` command
    """

    def __init__(self, c: Context) -> None:
        self.c = c
        """The *Invoke context*"""
        self.c.config.runners.local.input_sleep = 0
        self.cmd_prefix = env_files.cmd_prefix(c)
        """The command prefix set by stackzou.env_files.cmd_prefix"""
        self.stack_args = (
            "--compose-file docker-compose.yml"
            " "
            f"--compose-file envs/{self.c.env}/docker-compose.override.yml"
        )
        """
        The arguments when executing `docker stack`.
        These are usually building the compose files
        """

    def run(self, command: str, **kwargs):
        """Execute a shell command"""
        return self.c.run(command, **kwargs)

    def configs_create(self, name: str, in_stream) -> str:
        """
        Create a config

        Return the docker config id
        """
        command = f"{self.cmd_prefix}docker config create {name} -"
        result = self.run(command, in_stream=in_stream, hide="stdout")
        return result.stdout.strip()

    def configs_list(self, stack_name: str) -> list:
        """List the configs"""
        configs = []
        command = f"{self.cmd_prefix}docker config list --format json --filter name={stack_name}"
        result = self.run(command, hide="stdout")
        for line in result.stdout.splitlines():
            configs.append(json.loads(line))
        return configs

    def show(self) -> None:
        """Show the docker compose"""
        command = f"{self.cmd_prefix}docker stack config {self.stack_args}"
        self.run(command)

    def ps(self, stack_name, cmd_args=None):
        """docker stack ps"""
        command = f"{self.cmd_prefix}docker stack ps {stack_name}"
        if cmd_args:
            command = " ".join([command, cmd_args])
        return self.run(command, hide="stdout")

    def rm(self, stack_name):
        """rm a stack"""
        command = f"{self.cmd_prefix}docker stack rm {stack_name}"
        return self.run(command)

    def deploy(self, stack_name):
        """deploy a stack"""
        command = f"{self.cmd_prefix}docker stack deploy --prune {stack_name} {self.stack_args}"
        return self.run(command)
