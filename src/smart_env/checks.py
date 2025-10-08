import os
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from django.apps import AppConfig
from django.core.checks import CheckMessage, Error, register
from django.utils.module_loading import import_string

if TYPE_CHECKING:
    from smart_env import SmartEnv


def missing_explicit(var: str) -> Error:
    return Error(f"{var} is not set", hint=f"set {var} env var", id="smart_env.E001")


@register("config")
def check_environment(app_configs: Sequence[AppConfig] | None, **kwargs: Any) -> list[CheckMessage]:
    settings = os.environ["DJANGO_SETTINGS_MODULE"]
    instance = os.environ.get("SMART_ENV_INSTANCE", f"{settings}.env")
    env: SmartEnv = import_string(instance)
    return [missing_explicit(entry) for entry in env.check_explicit()]
