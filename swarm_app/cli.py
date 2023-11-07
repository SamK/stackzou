#!/usr/bin/env python3
"""
Beaucoup trop genial
"""
import pprint

import invoke

from invoke import Program, Collection, task, Config, config as invoke_config
from swarm_app import compose, configs, docker, env_files,   __version__
from swarm_app import stack
from invoke import __version__ as invoke_version
import sys

ns = Collection()
ns.add_collection(compose)
ns.add_collection(configs)
ns.add_collection(docker)
ns.add_collection(env_files)
ns.add_collection(stack)
#ns.configure({'key': 'value'}) # yes, it is possible to configure from here

version = f"""{__version__}

Python: {sys.version}
Invoke {invoke_version}"""

"""
class Invoke_Config(invoke.config.Config):

    @staticmethod
    def global_defaults():
        their_defaults = Config.global_defaults()
        my_defaults = {
            'project_location': '/tmp',
            'run': {
                'echo': True,
            },
        }
        return invoke.config.merge_dicts(their_defaults, my_defaults)
"""

program = Program(
    name="Your Swarm app",
    binary="swarm-app",
    version=version,
    #namespace=Collection.from_module(sys.modules[__name__]), # why?
    namespace=ns,
    #config_class=Invoke_Config,
)

#program.load_collection()

#print(program.config) # set_project_location
# program.set_project_location
#print("loglbal defaults:")
#pprint.pprint (Invoke_Config.global_defaults())

#print("runtime_path: ")
#pprint.pprint(Invoke_Config.runtime_path)


#print("project_location: ")
#pprint.pprint(Invoke_Config.project_location)

"""
print("__dict")
pprint.pprint(program.__dict__)

print("dir()")
pprint.pprint(dir(program))

print("COnfig class:")
pprint.pprint(dir(program.config_class))
print("prefix")
pprint.pprint(program.config_class.prefix)



print("env prefix")
pprint.pprint(program.config_class.env_prefix)

print("file_prefix")
pprint.pprint(program.config_class.file_prefix)
"""

#print("set location")
#pprint.pprint(program.config_class.set_project_location(path="/tmp"))

if __name__ == "__main__":
    program.run()
