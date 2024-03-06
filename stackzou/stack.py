"""
On gère la stack docker par ici
"""

import os
import json
from types import SimpleNamespace


def name(env):
    """Return the name of the stack"""
    value = os.path.basename(os.getcwd())
    value = value.removesuffix("-deploy")
    value = f"{value}-{env}"
    return value


Col = SimpleNamespace(
    PURPLE="\033[95m",
    GREY="\033[92m",
    WARNING="\033[93m",
    FAIL="\033[91m",
    ENDC="\033[0m",
    UNDERLINE="\033[4m",
    RED="\033[31m",
    BLUE="\033[34m",
    MAGENTA="\033[35m",
    CYAN="\033[36m",
    WHITE="\033[37m",
    ORANGE="\033[91m",
)


def col(color, words):
    """colorize a string"""
    color = color.upper()
    return f"{getattr(Col, color)}{words}{getattr(Col, 'ENDC')}"


def first_word(phrase):
    """Return the first word of a phrase"""

    # special case where there is no word
    if phrase == "":
        return ""

    return phrase.split(None, 1)[0]


def cut(phrase, length):
    """make a string "length" short"""
    return phrase[:length]


def colorize_ps_fields(ps_task):
    """
    colorize the fields of "docker stack ps"
    """

    t = ps_task

    # colorize Name
    if first_word(t["CurrentState"]) == "Running":
        if "second" in t["CurrentState"]:
            # it is running and new
            t["Name"] = col("GREY", t["Name"])
        elif "second" in t["CurrentState"]:
            t["Name"] = col("WHITE", t["Name"])
    else:
        # not running
        t["Name"] = col("red", t["Name"])

    # Colorize Error
    if t["Error"]:
        t["Error"] = col("FAIL", t["Error"])

    # Colorize Desired state
    elif first_word(t["DesiredState"]) != "Running":
        # the state is not "Running"
        t["DesiredState"] = col("ORANGE", t["DesiredState"])

    # Colorize Current state
    if first_word(t["CurrentState"]) != first_word(t["DesiredState"]):
        # the desired state is not applied. Make it shiny
        t["CurrentState"] = col("red", t["CurrentState"])
    else:
        # the desired state is applied. make it green
        if "second" in t["CurrentState"]:
            t["CurrentState"] = col("blue", t["CurrentState"])

    return t


def format_ps_lines(ps_stdout, colorize, history, error_on_new_line, shorten_id=6):

    formatted_lines = []

    # keep track of the names for the history
    names = []

    for ps_task in ps_stdout:

        # at the end of the loop, add the name in the list of used names
        current_name = ps_task["Name"]

        if current_name in names and history is False:
            # do not show history tasks
            continue

        if shorten_id:
            ps_task["ID"] = cut(ps_task["ID"], shorten_id)

        if colorize:
            fields = colorize_ps_fields(ps_task)
        else:
            fields = ps_task

        formatted = " ".join(
            [
                fields["ID"],
                fields["Name"],
                fields["Node"],
                fields["DesiredState"],
                fields["CurrentState"],
            ]
        )
        if fields["Error"]:
            if error_on_new_line:
                formatted += "\n"
            else:
                formatted += " "
            formatted += f"{fields['Error']}"
        names.append(current_name)
        formatted_lines.append(formatted)
    return "\n".join(formatted_lines)


def parse_ps(ps_out):
    """
    Return the output of "docker stack ps"
    """
    data = []
    for line in ps_out.split("\n"):
        if line:
            data.append(json.loads(line))
    return data
