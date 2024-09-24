import os
from typing import Any

from django.apps import AppConfig
from django.core.checks import CheckMessage, Error, register
from django.utils.module_loading import import_string

from smart_env import SmartEnv


def missing_explicit(var):
    return Error(
        f"{var} is not set",
        # hint=f"set {var} env var",
        id="smart_env.E001",
    )


@register("config")
def check_environment(app_configs: AppConfig, **kwargs: Any) -> list[CheckMessage]:
    settings = os.environ["DJANGO_SETTINGS_MODULE"]
    instance = os.environ.get("SMART_ENV_INSTANCE", f"{settings}.env")
    env: SmartEnv = import_string(instance)
    errors = []
    for entry in env.check_explicit():
        errors.append(missing_explicit(entry))

    return errors
