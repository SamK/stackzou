"""
Subcommands related to the Docker Stack
"""

import sys
from textwrap import dedent
from invoke import task
from stackzou import docker, stack


@task(name="name")
def name_(c):
    """
    Print the name of the stack

    Requires a defined environment.
    """
    print(stack.name(c.env))


@task(
    name="ps",
    help={
        "command_args": dedent(
            """\
            Additional options to the ps command:
            Example 1: -c "--no-trunc --no-resolve --format 'table {{ .Name }}'"
            Example 2: -c "--filter name=semaphore-prod_semaphore"
            """
        ),
        "format": "des super mise en page: lines|clines|cclines",
    },
    optional=["format", "command_args"],
)
def ps_(c, command_args=None, format_=None):
    """
    Show the current tasks: execute "docker stack ps"
    """
    client = docker.Docker(c)

    if format_:
        command_args = "--format json --no-trunc"

    result = client.ps(stack.name(c.env), command_args)

    data = []

    if format_ == "lines":
        data = stack.parse_ps(result.stdout)
        print(
            stack.format_ps_lines(
                data, colorize=False, history=True, error_on_new_line=False
            )
        )
    elif format_ == "clines":  # color lines
        data = stack.parse_ps(result.stdout)
        print(
            stack.format_ps_lines(
                data, colorize=True, history=True, error_on_new_line=True
            )
        )
    elif format_ == "cclines":  # current color lines
        data = stack.parse_ps(result.stdout)
        print(
            stack.format_ps_lines(
                data, colorize=True, history=False, error_on_new_line=False
            )
        )
    elif format_ is not None:
        print(f'Command line error: unknown formatting: "{format}".', file=sys.stderr)
    else:
        print(result.stdout)


@task
def rm(c):
    """Remove a stack: execute "docker stack rm" """
    client = docker.Docker(c)
    client.rm(stack.name(c.env))


@task
def deploy(c):
    """
    Deploy the Docker Stack
    """
    client = docker.Docker(c)
    client.deploy(stack.name(c.env))
