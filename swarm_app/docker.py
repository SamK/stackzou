from swarm_app import env_files


class Docker:
    def __init__(self, c):
        self.c = c
        self.c.config.runners.local.input_sleep = 0
        self.cmd_prefix = env_files.cmd_prefix(c.env)

    def run(self, command, **kwargs):
        with self.c.cd(env_files.path(self.c)):
            return self.c.run(command, **kwargs)

    def configs_create(self, name, in_stream):
        """
        Create a config return the docker config id
        """
        command = f"{self.cmd_prefix} time docker config create {name} -"
        result = self.run(command, in_stream=in_stream, hide="both")
        return result.stdout.strip()

    def configs_list(self, stack_name):
        command = f"{self.cmd_prefix} docker config list --format json --filter name={stack_name}"
        return self.run(command)

    def show(self):
        command = f"{self.cmd_prefix} docker-compose config"
        self.run(command)

    def ps(self, stack_name, cmd_args=None):
        command = f"{self.cmd_prefix} docker stack ps {stack_name}"
        if cmd_args:
            command = " ".join([command, cmd_args])
        return self.run(command)

    def deploy(self, stack_name):
        command = f"{self.cmd_prefix} docker stack deploy --prune {stack_name} --compose-file <(docker-compose config)"
        return self.run(command)
