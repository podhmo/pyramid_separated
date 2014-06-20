# -*- coding:utf-8 -*-
import os.path
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser
from pyramid.exceptions import ConfigurationError
from pyramid.path import AssetResolver


def normalize_path(config, keyname):
    try:
        resolver = AssetResolver()
        path = config.registry.settings[keyname]
        return resolver.resolve(path).abspath()
    except KeyError:
        raise ConfigurationError("{} is not found in settings".format(keyname))


def settings_from_path(path, category):
    parser = ConfigParser()
    parser.read(path)
    return dict(parser.items(category))


def merge_dict(d1, d2, overwrite=False):
    if overwrite:
        d1.update(d2)
    else:
        for k, v in d2.items():
            if k not in d1:
                d1[k] = v


def add_config_file(config, keyname, category="main", overwrite=False):
    path = normalize_path(config, keyname)
    if not os.path.exists(path):
        raise ConfigurationError("config file: {} is not found".format(path))

    another_settings = settings_from_path(path, category)
    merge_dict(config.registry.settings, another_settings, overwrite=overwrite)


def includeme(config):
    config.add_directive("add_config_file", add_config_file)
