"""
On gère la stack docker par ici
"""
import os


def name(env):
    """Return the name of the stack"""
    value = os.path.basename(os.getcwd())
    value = value.removesuffix("-deploy")
    value = f"{value}-{env}"
    return value
