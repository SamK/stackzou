"""
Manipule les "docker configs" et génère les fichiers vars qui vont bien.
"""

import os
import sys
import hashlib
from slugify import slugify
from stackzou import env_files, stack


class Config:
    """
    Create and update Docker Configs

    Arguments:
      c:            the Invoke class
      path:         the path to the local file
      stack_name:   the name of the stack
      configs_path: the location where the files are stored

    Attributes:
      key:     the key of the file
      hash:    a unique identifier based on the file properties
      id:      the Docker Config ID
      content: the content of the file
      value:   the rendered config
    """

    def __init__(self, c, path, stack_name, configs_path="configs"):
        self.c = c
        self.path = path
        self.configs_path = configs_path
        self.stack_name = stack_name

        self.key = None
        self.hash = None
        self.id = None
        self.content = None
        self.value = None
        self.update()

    def update(self):
        """
        Update the properties of the object.

        This method must be executed if properties have changed.
        """
        self.content = self._read_file()
        self.value = self.render()
        self.set_key()
        self.set_hash()
        self.set_id()

    def _read_file(self):
        """Read a file"""
        try:
            with open(self.path, mode="r", encoding="utf-8") as file:
                return file.read()
        except UnicodeDecodeError as e:
            print(
                f"FATAL UnicodeDecodeError: Je peux pas lire le fichier {self.path}: {e}.",
                file=sys.stderr,
            )
            raise

    def set_id(self):
        """Define the Docker Config Spec.Name"""
        self.id = f"{self.stack_name}_{self.key}-{self.hash}"

    def render(self):
        """Define the Docker Config Spec.Data"""
        if self.path.endswith(".subst"):
            result = self.c.run(
                env_files.cmd_prefix(self.c)
                + f"set -o nounset && envsubst < {self.path}",
                hide="stdout",
            )
            return result.stdout
        return self.content

    def set_key(self):
        """Define the Docker Config key"""
        key = self.path
        if self.path.startswith(self.configs_path):
            key = key.removeprefix(self.configs_path)
        key = key.strip("/")
        self.key = slugify(key, separator="_").upper()

    def set_hash(self):
        """
        Define the hash of the Docker Config
        """
        self.hash = hashlib.md5(self.path.encode() + self.value.encode()).hexdigest()[
            :8
        ]

    def __str__(self):
        """Return the class as a string"""
        props = {"path": self.path, "id": self.id, "key": self.key, "hash": self.hash}
        result = []
        for k, v in props.items():
            result.append(f"{k}: {v}")
        result.append(f"value:\n{self.value}")
        return "\n".join(result)


def local_files(c):
    """
    Return a list of Config objects
    """
    stack_name = stack.name(c.env)
    config_files_path = "configs"
    result = []
    for dir_path, _, file_names in os.walk(config_files_path):
        for file_name in file_names:
            config_fullpath = "/".join([dir_path, file_name])
            this_config = Config(c, config_fullpath, stack_name)
            result.append(this_config)
    return result
