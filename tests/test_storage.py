import os
from unittest import mock

import pytest

from smart_env import SmartEnv


@pytest.fixture()
def env():
    return SmartEnv(STORAGE_DEFAULT=(str, ""))


@pytest.mark.parametrize(
    "storage",
    [
        "storage.SampleStorage?bucket=container&option=value&connection_string=Defaul",
        "storage.SampleStorage?bucket=container&option=value&connection_string=DefaultEndpointsProtocol=http;Account"
        "Name=devstoreaccount1;AccountKey=ke1==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;",
    ],
)
def test_storage_options(storage, env):
    with mock.patch.dict(os.environ, {"STORAGE_DEFAULT": storage}, clear=True):
        ret = env.storage("STORAGE_DEFAULT")

    assert ret["BACKEND"] == "storage.SampleStorage"
    assert sorted(ret["OPTIONS"].keys()) == ["bucket", "connection_string", "option"]


@pytest.mark.parametrize("storage", ["storage.SampleStorage"])
def test_storage(storage, env):
    with mock.patch.dict(os.environ, {"STORAGE_DEFAULT": storage}, clear=True):
        ret = env.storage("STORAGE_DEFAULT")

    assert ret["BACKEND"] == "storage.SampleStorage"


def test_storage_empty(env):
    with mock.patch.dict(os.environ, {}, clear=True):
        assert not env.storage("STORAGE_DEFAULT")
