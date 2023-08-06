# -*- coding: utf-8 -*-

from . import build
from . import config
import logging


logging.basicConfig(format="%(levelname)s: %(message)s")


__config__ = None


def load_config():
    global __config__
    if not __config__:
        __config__ = config.Config()
    return __config__


class Configurable:
    def __init__(self, *args, **kwargs):
        cfg = load_config()
        if "token" not in kwargs:
            kwargs["token"] = cfg.auth_token
        if "kbapi_url" not in kwargs:
            kwargs["kbapi_url"] = cfg.kbapi_url
        if "group" not in kwargs:
            kwargs["group"] = cfg.group
        if "project" not in kwargs:
            kwargs["project"] = cfg.project
        super().__init__(*args, **kwargs)


class Build(Configurable, build.Build):
    """
    This class represents individual builds. It should be used to trigger
    builds, and optionally wait for them to finish.
    """


class BuildSet(Configurable, build.BuildSet):
    """
    This class represents a set of builds that can be triggered and watched
    simultaneously.
    """
