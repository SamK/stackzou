#!/usr/bin/env python3
"""
Beaucoup trop genial
"""
import sys
from invoke import Program, Collection, __version__ as invoke_version
from stackzou import docker, __version__
from stackzou import tasks
from stackzou.tasks import configs, stack, compose, env_files

ns = Collection()
ns.add_collection(compose)
ns.add_collection(configs)
ns.add_collection(docker)
ns.add_collection(env_files)
ns.add_collection(stack)
ns.add_task(tasks.deploy)
ns.add_task(tasks.set_env)
ns.add_task(tasks.verbose)
# ns.configure({'key': 'value'}) # yes, it is possible to configure from here

version = f"""{__version__}

Python: {sys.version}
Invoke {invoke_version}"""

program = Program(
    name="Your Swarm app",
    binary="stackzou",
    version=version,
    namespace=ns,
)

if __name__ == "__main__":
    program.run()
