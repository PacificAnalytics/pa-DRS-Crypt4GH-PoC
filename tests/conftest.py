import pathlib

import pytest


def _datapath(fname):
    return pathlib.Path(__file__).parent / "data" / fname


@pytest.fixture
def server_sk():
    return _datapath("server-sk.key")


@pytest.fixture
def server_pk():
    return _datapath("server-pk.key")


@pytest.fixture
def patch_env(monkeypatch, server_pk, server_sk):
    monkeypatch.setenv("ACCESS_KEY", "accesskey")
    monkeypatch.setenv("SECRET_KEY", "secretkey")
    monkeypatch.setenv("SEC_KEY", _read(server_sk))
    monkeypatch.setenv("PUB_KEY", _read(server_pk))


def _read(fname):
    with open(fname, "rt") as fp:
        return fp.read()
