"""Test suite"""

from tests.lib import chdir
from stackzou import stack


def test_stack_name():
    with chdir("examples"):
        res = stack.name("testenv")
    assert res == "examples-testenv"


def test_first_word():
    assert stack.first_word("Hello World!") == "Hello"
    assert stack.first_word("Foo") == "Foo"
    assert stack.first_word("Two  spaces") == "Two"
    assert stack.first_word("Tab    is also a word separator") == "Tab"
    assert stack.first_word(" Untrimmed") == "Untrimmed"
    assert stack.first_word("") == ""


def test_cut():
    # cut same as input
    assert stack.cut("a", 1) == "a"
    # cut greater than input
    assert stack.cut("a", 2) == "a"
    # smaller than input
    assert stack.cut("ABCDEF", 4) == "ABCD"
    # test empty string
    assert stack.cut("", 4) == ""
