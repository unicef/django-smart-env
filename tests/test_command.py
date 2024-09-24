import os
from unittest import mock

import pytest
from io import StringIO

from django.core.management import call_command


@pytest.mark.parametrize("develop", [0, 1], ids=["0", "1"])
@pytest.mark.parametrize("check", [0, 1], ids=["0", "1"])
def test_env(check, develop):
    out = StringIO()
    environ = {
        "DJANGO_SETTINGS_MODULE": "demo.settings",
        "ADMIN_URL_PREFIX": "test",
        "SECURE_SSL_REDIRECT": "1",
        "SECRET_KEY": "" * 120,
        "SESSION_COOKIE_SECURE": "1",
    }
    with mock.patch.dict(os.environ, environ, clear=True):
        call_command(
            "env",
            ignore_errors=True if check == 1 else False,
            stdout=out,
            check=check,
            develop=develop,
        )
        assert "error" not in str(out.getvalue())


def test_develop():
    out = StringIO()
    environ = {
        "DJANGO_SETTINGS_MODULE": "demo.settings",
        "ADMIN_URL_PREFIX": "test",
        "SECURE_SSL_REDIRECT": "1",
        "SECRET_KEY": "" * 120,
        "SESSION_COOKIE_SECURE": "1",
    }
    with mock.patch.dict(os.environ, environ, clear=True):
        call_command("env", stdout=out, develop=True)
        assert str(out.getvalue()) == """DEBUG=True
DATABASE_URL=sqlite:///demo.db
USE_TZ=True
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
"""
