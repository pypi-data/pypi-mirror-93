# -*- coding: utf-8 -*-

import os
import tuxsuite.exceptions
from os.path import expanduser
import configparser
import logging
import re
import yaml
from tuxsuite import requests


def getenv(name, default=None):
    deprecated = os.getenv(f"TUXBUILD_{name}")
    if deprecated:
        logging.warning(
            f"TUXBUILD_{name} is deprecated, please use TUXSUITE_{name} instead"
        )
        return deprecated

    return os.getenv(f"TUXSUITE_{name}", default)


def get_config_file(name):
    config_path = f"~/.config/tuxsuite/{name}"
    deprecated_config_path = f"~/.config/tuxbuild/{name}"
    if os.path.exists(expanduser(deprecated_config_path)):
        logging.warning(
            f"{deprecated_config_path} is deprecated; please rename it to {config_path}."
        )
        return deprecated_config_path
    return config_path


class Config:
    def __init__(self, config_path=None):
        """
        Retrieve tuxsuite authentication token and API url

        TuxSuite requires an API token. Optionally, a API url endpoint may
        be specified. The API url defaults to https://api.tuxbuild.com/v1.

        The token and url may be specified in environment variables, or in
        a tuxsuite config file. If using the config file, the environment
        variable TUXSUITE_ENV may be used to specify which tuxsuite config
        to use.

        Environment variables:
            TUXSUITE_TOKEN
            TUXSUITE_URL (optional)

        Config file:
            Must be located at ~/.config/tuxsuite/config.ini.
            This location can be overriden by setting the TUXSUITE_CONFIG
            environment variable.
            A minimum config file looks like:

                [default]
                token=vXXXXXXXYYYYYYYYYZZZZZZZZZZZZZZZZZZZg

            Multiple environments may be specified. The environment named
            in TUXSUITE_ENV will be chosen. If TUXSUITE_ENV is not set,
            'default' will be used.

            Fields:
                token
                api_url (optional)
        """

        self.default_api_url = (
            "https://api.tuxbuild.com/v1"  # Use production v1 if no url is specified
        )
        self.tuxsuite_env = getenv("ENV", "default")

        (
            self.auth_token,
            self.kbapi_url,
            self.group,
            self.project,
        ) = self._get_config_from_env()

        config_path = getenv("CONFIG", config_path)

        if config_path is None:
            config_path = get_config_file("config.ini")

        if not self.auth_token:
            (
                self.auth_token,
                self.kbapi_url,
                self.group,
                self.project,
            ) = self._get_config_from_config(config_path)

        if not self.auth_token:
            raise tuxsuite.exceptions.TokenNotFound(
                "Token not found in TUXSUITE_TOKEN nor at [{}] in {}".format(
                    self.tuxsuite_env, config_path
                )
            )
        if not self.kbapi_url:
            raise tuxsuite.exceptions.URLNotFound(
                "TUXSUITE_URL not set in env, or api_url not specified at [{}] in {}.".format(
                    self.tuxsuite_env, config_path
                )
            )

    def _get_config_from_config(self, config_path):
        path = expanduser(config_path)
        try:
            open(path, "r")  # ensure file exists and is readable
        except Exception as e:
            raise tuxsuite.exceptions.CantGetConfiguration(str(e))

        config = configparser.ConfigParser()

        config.read(path)
        if not config.has_section(self.tuxsuite_env):
            raise tuxsuite.exceptions.InvalidConfiguration(
                "Error, missing section [{}] from config file '{}'".format(
                    self.tuxsuite_env, path
                )
            )
        kbapi_url = (
            config[self.tuxsuite_env].get("api_url", self.default_api_url).rstrip("/")
        )
        auth_token = config[self.tuxsuite_env].get("token", None)
        group = config[self.tuxsuite_env].get("group", None)
        project = config[self.tuxsuite_env].get("project", None)
        return (auth_token, kbapi_url, group, project)

    def _get_config_from_env(self):
        # Check environment for TUXSUITE_TOKEN
        auth_token = None
        kbapi_url = None
        group = None
        project = None
        if getenv("TOKEN"):
            auth_token = getenv("TOKEN")
            kbapi_url = getenv("URL", self.default_api_url).rstrip("/")
            group = getenv("GROUP")
            project = getenv("PROJECT")
        return (auth_token, kbapi_url, group, project)

    def get_auth_token(self):
        return self.auth_token

    def get_kbapi_url(self):
        return self.kbapi_url

    def get_tuxsuite_env(self):
        return self.tuxsuite_env


InvalidConfiguration = tuxsuite.exceptions.InvalidConfiguration


class BuildSetConfig:
    def __init__(self, set_name, filename=None):
        self.set_name = set_name
        if filename:
            self.filename = filename
        else:
            self.filename = os.path.expanduser(get_config_file("builds.yaml"))
        self.entries = []
        self.__load_config__()

    def __load_config__(self):
        filename = self.filename
        set_name = self.set_name
        try:
            if re.match(r"^https?://", str(filename)):
                contents = self.__fetch_remote_config__(filename)
            else:
                contents = open(filename).read()
            config = yaml.safe_load(contents)
        except (FileNotFoundError, yaml.loader.ParserError) as e:
            raise InvalidConfiguration(str(e))
        if not config:
            raise InvalidConfiguration(
                f"Build set configuration in {filename} is empty"
            )
        if "sets" not in config:
            raise InvalidConfiguration('Missing "sets" key')
        for set_config in config["sets"]:
            if set_config["name"] == set_name:
                if "builds" in set_config:
                    self.entries = set_config["builds"]
                    if not self.entries:
                        raise InvalidConfiguration(
                            f'Build list is empty for set "{set_name}"'
                        )
                    return
                else:
                    raise InvalidConfiguration(
                        f'No "builds" field defined for set "{set_name}"'
                    )
        raise InvalidConfiguration(f'No build set named "{set_name}" in {filename}')

    def __fetch_remote_config__(self, url):
        result = requests.get(url)
        if result.status_code != 200:
            raise InvalidConfiguration(
                f"Unable to retrieve {url}: {result.status_code} {result.reason}"
            )
        return result.text
