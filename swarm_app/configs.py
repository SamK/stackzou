"""
Manipule les "docker configs" et génère les fichiers vars qui vont bien.
"""
import os
import hashlib
from slugify import slugify


def local_files():
    """
    Return a list of config files dicts.

    The dicts have these keys:
    - path: the path to the file
    - key: the key of the file (without hash)
    - value: the content
    - hash: a unique identifier based on the file properties
    """
    config_files_path = "configs"
    result = []
    for dir_path, _, file_names in os.walk(config_files_path):
        for file_name in file_names:
            this_config = {}
            this_config["path"] = "/".join([dir_path, file_name])

            # define the key (limited to 64 chars)
            key = this_config["path"]
            # remove config_files_path:
            if key.startswith(config_files_path):
                key = key.removeprefix(config_files_path)
            key = key.strip("/")
            this_config["key"] = slugify(key, separator="_").upper()

            with open(this_config["path"], mode="r", encoding="utf-8") as file:
                this_config["value"] = file.read()
            this_config["hash"] = hashlib.md5(
                this_config["path"].encode() + this_config["value"].encode()
            ).hexdigest()[:8]
            result.append(this_config)
    return result
