"""
Un RC file c'est un fichier avec des lignes du genre `KEY=value`
"""


# import os
class RCFile:
    """
    Un rc file / vars file
    """

    def __init__(self, filename):
        self.filename = filename

    def read(self):
        """
        variables = {}
        with open(os.path.expanduser(self.filename), "r") as f:
            for line in f:
                if line.strip() and not line.strip().startswith("#"):
                    key, value = line.split("=", 1)
                    variables[key] = value
        return variables
        """

    def write(self, variables, append=False, export=False):
        """
        Write variables in a RC file
        """
        mode = "a" if append else "w"

        prefix = ""
        if export:
            prefix = "export "

        with open(self.filename, mode=mode, encoding="utf-8") as f:
            for key, value in variables.items():
                f.write(f"{prefix}{key}={value}\n")
