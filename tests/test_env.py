import os
from unittest import mock

import pytest

from smart_env import SmartEnv
from smart_env.exceptions import SmartEnvMissingVarError


def test_base():
    config = {
        "KEY": (str, ""),
        "DEFAULT": (str, "1"),
        "INT": int,
    }
    with mock.patch.dict(os.environ, {"KEY": "value", "INT": "10"}):
        env = SmartEnv(**config)
        assert env("KEY") == "value"
        assert env("DEFAULT") == "1"
        assert env("INT") == 10


@pytest.mark.parametrize("arg", ["1", "true", "T", "yes", "y", "Y", "abc", "True", "TRUE"])
def test_bool_true(arg):
    config = {"arg": (bool, arg), "arg1": bool}
    with mock.patch.dict(os.environ, {"arg": arg, "arg1": arg}):
        env = SmartEnv(**config)
        assert env("arg") is True
        assert env("arg1") is True
        assert env.bool("arg") is True


@pytest.mark.parametrize("arg", ["0", "False", "F", "no", "n", "N", "FALSE", ""])
def test_bool_false(arg):
    config = {"arg": (bool, arg), "arg1": bool}
    with mock.patch.dict(os.environ, {"arg": arg, "arg1": arg}):
        env = SmartEnv(**config)
        assert env("arg") is False
        assert env("arg1") is False
        assert env.bool("arg") is False


@pytest.mark.parametrize("arg", ["0", "False", "F", "no", "n", "N", "FALSE", ""])
def test_storage(arg):
    config = {"arg": (bool, arg, False), "arg1": bool}
    with mock.patch.dict(os.environ, {"arg": arg, "arg1": arg}):
        env = SmartEnv(**config)
        assert env("arg") is False
        assert env("arg1") is False


def test_extras():
    config = {
        "optional1": (str, "default_value"),
        "optional2": (str, "default_value", False),
        "explicit": (bool, "default_value", "", True),
        "with_help": (bool, "default_value", "", True, "help"),
    }
    with mock.patch.dict(os.environ, {}):
        env = SmartEnv(**config)
        assert env.config["optional1"] == {
            "cast": str,
            "default": "default_value",
            "develop": "default_value",
            "explicit": False,
            "help": "",
        }
        assert env.config["explicit"] == {
            "cast": bool,
            "default": "default_value",
            "develop": "",
            "explicit": True,
            "help": "",
        }
        assert env.config["with_help"] == {
            "cast": bool,
            "default": "default_value",
            "develop": "",
            "explicit": True,
            "help": "help",
        }


def test_check_explicit():
    config = {
        "optional1": (str, "default_value"),
        "optional2": (str, "default_value", "", False),
        "explicit": (str, "default_value", "", True),
        "arg1": bool,
    }
    with mock.patch.dict(os.environ, {}):
        env = SmartEnv(**config)
        assert env.check_explicit() == ["explicit"]
        assert not env.is_valid()


def test_missing():
    with mock.patch.dict(os.environ, {}):
        env = SmartEnv()
        with pytest.raises(SmartEnvMissingVarError) as e:
            env("MISSING")
        assert str(e.value) == "Missing MISSING"
