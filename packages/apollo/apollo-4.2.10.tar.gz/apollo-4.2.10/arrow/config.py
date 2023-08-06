from __future__ import absolute_import

import os

import yaml

DEFAULT_CONFIG = {
}


def global_config_path():
    config_path = os.environ.get(
        "ARROW_GLOBAL_CONFIG_PATH",
        "~/.apollo-arrow.yml"
    )
    config_path = os.path.expanduser(config_path)
    return config_path


def read_global_config():
    config_path = global_config_path()
    if not os.path.exists(config_path):
        return DEFAULT_CONFIG

    with open(config_path) as f:
        return yaml.safe_load(f)
