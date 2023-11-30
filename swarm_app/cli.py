#!/usr/bin/env python3
"""
Beaucoup trop genial
"""
import sys
from invoke import Program, Collection, __version__ as invoke_version
from swarm_app import compose, configs, docker, env_files, __version__, stack, tasks

ns = Collection()
ns.add_collection(compose)
ns.add_collection(configs)
ns.add_collection(docker)
ns.add_collection(env_files)
ns.add_collection(stack)
ns.add_task(tasks.set_env)
# ns.configure({'key': 'value'}) # yes, it is possible to configure from here

version = f"""{__version__}

Python: {sys.version}
Invoke {invoke_version}"""

program = Program(
    name="Your Swarm app",
    binary="swarm-app",
    version=version,
    namespace=ns,
)

if __name__ == "__main__":
    program.run()
