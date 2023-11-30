#!/usr/bin/env python3
"""
Beaucoup trop genial
"""
import pprint

import invoke

from invoke import Program, Collection, task, Config, config as invoke_config
from swarm_app import compose, configs, docker, env_files, __version__
from swarm_app import stack
from invoke import __version__ as invoke_version
import sys

ns = Collection()
ns.add_collection(compose)
ns.add_collection(configs)
ns.add_collection(docker)
ns.add_collection(env_files)
ns.add_collection(stack)
# ns.configure({'key': 'value'}) # yes, it is possible to configure from here

version = f"""{__version__}

Python: {sys.version}
Invoke {invoke_version}"""

program = Program(
    name="Your Swarm app",
    binary="swarm-app",
    version=version,
    # namespace=Collection.from_module(sys.modules[__name__]), # why?
    namespace=ns,
    # config_class=Invoke_Config,
)

if __name__ == "__main__":
    program.run()
