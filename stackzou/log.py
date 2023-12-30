"""
On gère la gestion des logs ici
"""


def log1(c, message):
    """Print a log"""
    if "loglevel" not in c:
        return
    if c.loglevel >= 1:
        print(message)
