import os
from unittest import mock
from unittest.mock import Mock

from smart_env import SmartEnv
from smart_env.checks import check_environment

pippo = SmartEnv(DEBUG=(bool, False, False, True))


def test_check():
    environ = {
        "DJANGO_SETTINGS_MODULE": "demo.settings",
        "SMART_ENV_INSTANCE": "test_check.pippo"
    }
    with mock.patch.dict(os.environ, environ, clear=True):
        assert check_environment(Mock())
