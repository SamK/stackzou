"""Test suite"""

from invoke import MockContext, Result
from stackzou.tasks import configs
from tests.lib import chdir


def test_tasks_configs_list_(capfd):
    """
    Ensure stackzou configs.list can read a list of docker configs
    """
    jsons = """{"CreatedAt": "b", "ID":"line0"}
    {"CreatedAt": "c", "ID":"line1"}"""
    c = MockContext(run=Result(jsons))
    c.env = "simple"
    with chdir("examples"):
        out = configs.list_(c)
    out, _ = capfd.readouterr()
    assert "line0" in out
    assert "line1" in out


def test_tasks_configs_list_empty(capfd):
    """
    Ensure stackzou configs.list can read an *empty* list of docker configs
    """
    jsons = ""
    c = MockContext(run=Result(jsons))
    c.env = "simple"
    with chdir("examples"):
        out = configs.list_(c)
    out, _ = capfd.readouterr()
    assert out.strip() == "[]"  # the output format is not documented


def test_tasks_configs_show(capfd):
    """
    Ensure stackzou configs.show can read an file and show the properties
    """
    c = MockContext()
    c.env = "simple"
    with chdir("examples"):
        out = configs.show(c, "configs/file.txt")
    out, _ = capfd.readouterr()
    assert "configs/file.txt" in out
    assert "This is an example config file." in out
    # TODO:
    # assert id
    # assert key
    # hash


# TODO: this is difficult, the function contains more than one run command
# def test_tasks_configs_create(capfd):
#     jsons = """{"CreatedAt":"3 years ago",
#       "ID":"abcdef0000jc98aiu4tjz7lo7","Labels":"","Name":"test-7c2908b0","UpdatedAt":"3 months ago"}"""
#     jsons = """{"Name": "fu", "asdf": "toto"}"""
#     c = MockContext(run=Result(jsons) )
#     c.echo =True
#     c.env = "simple"
#     with chdir("examples"):
#         out = configs.create(c)
#     out, _ = capfd.readouterr()
#     assert "Config examples-simple_FILE_TXT-683800ca updated with id mimfeiww7mqnwbauwvspg3xpk." in out
#     assert "FILE_TXT=examples-simple_FILE_TXT-683800ca" in out
