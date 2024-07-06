"""
Test stackzou.docker

See:
https://docs.pyinvoke.org/en/stable/concepts/testing.html
"""

import os
from io import StringIO
from pathlib import Path
import pytest
from invoke import MockContext, Result
from tests.lib import chdir
from stackzou import docker


@pytest.fixture(name="touch_remove")
def fixture_touch_remove():
    """
    https://docs.pytest.org/en/latest/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization
    """
    filename = "examples/envs/simple/test_docker.env"
    Path(filename).touch()
    yield filename
    os.remove(filename)


def test_docker_docker_init(touch_remove):
    c = MockContext()
    c.env = "simple"
    with chdir("examples"):
        client = docker.Docker(c)
    assert isinstance(client, docker.Docker)
    _ = touch_remove
    assert isinstance(client.cmd_prefix, str)
    assert " envs/simple/test_docker.env " in client.cmd_prefix


def test_docker_docker_run():
    c = MockContext(run=Result())
    c.env = "simple"
    with chdir("examples"):
        client = docker.Docker(c)
        res = client.run("test-command")
    assert res.command == "test-command"


def test_docker_docker_configs_create():
    """
    C'est too much pour un truc qu'on peut même pas bien tester :/
    """
    c = MockContext(run=Result("abcdef"))
    c.env = "simple"
    with chdir("examples"):
        client = docker.Docker(c)
        res = client.configs_create(name="test_config1", in_stream=StringIO("salut"))
    assert res == "abcdef"


def test_docker_docker_configs_list():
    config_list = """{"a": 1 }
    {"b": 2 }"""

    c = MockContext(run=Result(config_list))
    c.env = "simple"
    with chdir("examples"):
        client = docker.Docker(c)
        res = client.configs_list("dummy-value")
    assert res == [{"a": 1}, {"b": 2}]


# def test_docker_docker_configs_show():
# def test_docker_docker_configs_ps():
# def test_docker_docker_configs_rm():
# def test_docker_docker_configs_deploy():


# je me souviens plus comment ça fonctionne ces tests.
# def test_docker_docker_compose_show_skip_interpolation():
#     c = MockContext(run=Result())
#     c.env = "simple"
#     with chdir("examples"):
#         client = docker.Docker(c)
#         #client.stack_args += "--skip-interpolation"
#         # res = client.run("test-command")
#         client.show()
#
#     # assert res.command == "test-command"
