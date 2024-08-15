#!/usr/bin/env python3
"""
This file is the main CLI.

It is using [PyInvoke](https://www.pyinvoke.org/) for argument parsing.
"""
import sys
from invoke import Program, Collection, __version__ as invoke_version  # type: ignore[attr-defined]
from stackzou import __version__
from stackzou import tasks
from stackzou.tasks import configs, stack, compose, env_files

ns = Collection()
"""
The Invoke *namespace* contains a *collections* of tasks.

All collections are added into this namespace.

See: https://docs.pyinvoke.org/en/stable/concepts/namespaces.html
"""

ns.add_collection(compose)  # type: ignore[arg-type]
ns.add_collection(configs)  # type: ignore[arg-type]
ns.add_collection(env_files)  # type: ignore[arg-type]
ns.add_collection(stack)  # type: ignore[arg-type]
ns.add_task(tasks.deploy)
ns.add_task(tasks.set_env)
ns.add_task(tasks.verbose)  # type: ignore[arg-type]
ns.add_task(tasks.ps)

# ns.configure({'key': 'value'}) # yes, it is possible to configure from here

version = f"""{__version__}

Python: {sys.version}
Invoke {invoke_version}"""
"""The version string as showed to the user"""

program = Program(
    name="StackZou",
    binary="stackzou",
    version=version,
    namespace=ns,
)
"""
Create Invoke *Program*

Allows Invoke to understand that the created namespace is running inside a binary.

See: https://docs.pyinvoke.org/en/stable/api/program.html
"""

if __name__ == "__main__":
    program.run()
