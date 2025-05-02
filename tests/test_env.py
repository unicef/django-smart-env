import os
from unittest import mock

import pytest

from smart_env import SmartEnv
from smart_env.exceptions import SmartEnvMissing


def test_base():
    CONFIG = {
        "KEY": (str, ""),
        "DEFAULT": (str, "1"),
        "INT": int,
    }
    with mock.patch.dict(os.environ, {"KEY": "value", "INT": "10"}):
        env = SmartEnv(**CONFIG)
        assert env("KEY") == "value"
        assert env("DEFAULT") == "1"
        assert env("INT") == 10


@pytest.mark.parametrize("arg", ["1", "true", "T", "yes", "y", "Y", "abc", "True", "TRUE"])
def test_bool_true(arg):
    CONFIG = {"arg": (bool, arg), "arg1": bool}
    with mock.patch.dict(os.environ, {"arg": arg, "arg1": arg}):
        env = SmartEnv(**CONFIG)
        assert env("arg") is True
        assert env("arg1") is True
        assert env.bool("arg") is True


@pytest.mark.parametrize("arg", ["0", "False", "F", "no", "n", "N", "", "FALSE", "False", ""])
def test_bool_false(arg):
    CONFIG = {"arg": (bool, arg), "arg1": bool}
    with mock.patch.dict(os.environ, {"arg": arg, "arg1": arg}):
        env = SmartEnv(**CONFIG)
        assert env("arg") is False
        assert env("arg1") is False
        assert env.bool("arg") is False


@pytest.mark.parametrize("arg", ["0", "False", "F", "no", "n", "N", "", "FALSE", "False", ""])
def test_storage(arg):
    CONFIG = {"arg": (bool, arg, False), "arg1": bool}
    with mock.patch.dict(os.environ, {"arg": arg, "arg1": arg}):
        env = SmartEnv(**CONFIG)
        assert env("arg") is False
        assert env("arg1") is False


def test_extras():
    CONFIG = {
        "optional1": (str, "default_value"),
        "optional2": (str, "default_value", False),
        "explicit": (bool, "default_value", "", True),
        "with_help": (bool, "default_value", "", True, "help"),
    }
    with mock.patch.dict(os.environ, {}):
        env = SmartEnv(**CONFIG)
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
    CONFIG = {
        "optional1": (str, "default_value"),
        "optional2": (str, "default_value", "", False),
        "explicit": (str, "default_value", "", True),
        "arg1": bool,
    }
    with mock.patch.dict(os.environ, {}):
        env = SmartEnv(**CONFIG)
        assert env.check_explicit() == ["explicit"]
        assert not env.is_valid()


# @pytest.mark.parametrize("cfg", [{"error_explicit": (bool, "default_value", "", "")},
#                                  {"error_help": (str, "default_value", "", False, False)}
#                                  ])
# def test_check_config(cfg):
#     with pytest.raises(SmartEnvException) as e:
#         SmartEnv(**cfg)
#     assert str(e.value)
#     assert e.value.args


def test_missing():
    with mock.patch.dict(os.environ, {}):
        with pytest.raises(SmartEnvMissing) as e:
            env = SmartEnv()
            env("MISSING")
        assert str(e.value) == "Missing MISSING"


#
# def test_develop():
#     CONFIG = {"optional1": (str, "default_value"),
#               "optional2": (str, "default_value", "", False),
#               "explicit": (str, "default_value", "", True),
#               "arg1": bool
#               }
#     with mock.patch.dict(os.environ, {}):
#         with pytest.raises(SmartEnvMissing) as e:
#             env = SmartEnv()
#             env("MISSING")
#         assert str(e.value) == "Missing MISSING"

def test_set_environ_for_test():

    example_variables = {
    'VAR_1': (str, 'default_1', 'develop_1'),
    'VAR_2': (int, 1, 2),
    'VAR_3': (str, 'default_3', 'develop_3'),
    'VAR_4': (bool, 0, 1),
    }

    env = SmartEnv(**example_variables)

    changed_variables = {
    'VAR_1': 'changed_value_1',
    'VAR_2': 333,
    'VAR_4': False
    }

    env.set_environ_for_test(changed_variables)

    assert os.environ['VAR_1'] == 'changed_value_1'
    assert os.environ['VAR_2'] == '333'
    assert os.environ['VAR_3'] == 'develop_3'
    assert os.environ['VAR_4'] == 'False'


@pytest.mark.parametrize("new_val", [('VAR_1', '44'), ('VAR_2', 0)])
def test_environ_for_test_wrong_type(key, new_val):
    example_variables = {
    'VAR_1': (int, 2, 22),
    'VAR_2': (bool, 0, 1),
    }

    env = SmartEnv(**example_variables)

    changed_variables = {key: new_val}

    with pytest.raises(ValueError, match=f'Value for {key} must be {example_variables[key][0].__name__}'):
        env.set_environ_for_test(changed_variables)

