# -*- coding: utf-8 -*-

import requests
import tuxsuite.config
import pytest


@pytest.fixture(autouse=True)
def session(mocker):
    mocker.patch("requests.Session.get")
    mocker.patch("requests.Session.post")
    return requests.Session


@pytest.fixture
def response():
    r = requests.Response()
    r.status_code = 200
    return r


@pytest.fixture
def post(session, response):
    session.post.return_value = response
    return session.post


@pytest.fixture
def get(session, response):
    session.get.return_value = response
    return session.get


@pytest.fixture
def sample_token():
    return "Q9qMlmkjkIuIGmEAw-Mf53i_qoJ8Z2eGYCmrNx16ZLLQGrXAHRiN2ce5DGlAebOmnJFp9Ggcq9l6quZdDTtrkw"


@pytest.fixture
def sample_url():
    return "https://foo.bar.tuxbuild.com/v1"


@pytest.fixture(autouse=True)
def home(monkeypatch, tmp_path):
    h = tmp_path / "HOME"
    h.mkdir()
    monkeypatch.setenv("HOME", str(h))
    return h


@pytest.fixture
def config(monkeypatch, sample_token, sample_url):
    monkeypatch.setenv("TUXSUITE_TOKEN", sample_token)
    monkeypatch.setenv("TUXSUITE_URL", sample_url)
    config = tuxsuite.config.Config("/dev/null")
    config.kbapi_url = sample_url
    config.auth_token = sample_token
    return config
