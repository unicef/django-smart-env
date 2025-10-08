import os
from typing import TYPE_CHECKING

from django.core.management import BaseCommand, CommandError, CommandParser
from django.utils.module_loading import import_string

if TYPE_CHECKING:
    from typing import Any

    from smart_env import SmartEnv

DEVELOP = {
    "DEBUG": True,
    "SECRET_KEY": "only-development-secret-key",
}


class Command(BaseCommand):
    requires_migrations_checks = False
    requires_system_checks = []

    def add_arguments(self, parser: "CommandParser") -> None:
        parser.add_argument(
            "-f",
            "--format",
            action="store",
            dest="format",
            default="{key}={value}",
            help="Pattern to use to print variables (default: '{key}={value}{space}",
        )
        parser.add_argument("--develop", action="store_true", help="Display development values")
        parser.add_argument("--changed", action="store_true", help="Display only changed values")

        parser.add_argument(
            "--check",
            action="store_true",
            dest="check",
            default=False,
            help="Check env for variable availability",
        )
        parser.add_argument(
            "--ignore-errors",
            action="store_true",
            dest="ignore_errors",
            default=False,
            help="Do not fail",
        )

    def handle(self, *args: "Any", **options: "Any") -> None:  # noqa C901
        settings = os.environ["DJANGO_SETTINGS_MODULE"]
        instance = os.environ.get("SMART_ENV_INSTANCE", "env")
        env: SmartEnv = import_string(f"{settings}.{instance}")
        check_failure = False
        pattern = options["format"]
        if options["develop"] and options["changed"]:
            self.stderr.write("--develop and --changed cannot be used together.")
            return
        if options["check"]:
            for entry in env.check_explicit():
                self.stdout.write(self.style.ERROR(f"- Missing env variable: {entry}"))

        elif options["develop"]:
            for entry in env.config:
                self.stdout.write(f"{entry}={env.get_develop_value(entry)}")

        elif options["changed"]:
            for entry, cfg in env.config.items():
                if cfg["default"] != env(entry):
                    self.stdout.write(f"{entry}={env.get_develop_value(entry)}")
        else:
            for k, cfg in sorted(env.config.items()):
                self.stdout.write(pattern.format(key=k, value=env.get_value(k), **cfg))

        if check_failure and not options["ignore_errors"]:
            raise CommandError("Env check command failure!")
