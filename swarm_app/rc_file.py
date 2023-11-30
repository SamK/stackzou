class RC_File(object):
    """
    Un rc file / vars file
    """

    def __init__(self, filename):
        self.filename = filename

    def read(self):
        vars = {}
        with open(os.path.expanduser(self.filename), "r") as f:
            for line in f:
                if line.strip() and not line.strip().startswith("#"):
                    key, value = line.split("=", 1)
                    vars[key] = value
        return vars

    def write(self, variables, append=False, export=False):
        mode = "a" if append else "w"

        prefix = ""
        if export:
            prefix = "export "

        with open(self.filename, mode) as f:
            for key, value in variables.items():
                f.write(f"{prefix}{key}={value}\n")
