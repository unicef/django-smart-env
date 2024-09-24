from django.apps import AppConfig


class Config(AppConfig):
    verbose_name = "Smart Env"
    name = "smart_env"

    def ready(self) -> None:
        from . import checks  # noqa
