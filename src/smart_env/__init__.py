from collections.abc import Callable
from typing import TYPE_CHECKING, Any, TypedDict

from environ.environ import Env

from smart_env.exceptions import SmartEnvMissingVarError

if TYPE_CHECKING:
    Cast = Callable[[Any], Any]
    ConfigItem = (
        tuple[Cast, Any]  # original config. type,value
        | tuple[Cast, Any, Any]  # type,value:development value
        | tuple[Cast, Any, Any, bool]  # type,value:development value,explicit
        | tuple[Cast, Any, Any, bool, str]  # type,value:development value,explicit,help_text
        | Cast
    )

    class ConfigVar(TypedDict):
        cast: Cast
        default: Any
        develop: Any
        explicit: bool
        help: str

    SmartConfig = dict[str, ConfigItem]


def smart_bool(value: Any) -> bool:
    if value in (True, False):
        return bool(value)
    if not value:
        ret = False
    elif value.lower()[0] in ["t", "y", "1"]:
        ret = True
    elif value.lower()[0] in ["f", "n", "0"]:
        ret = False
    else:
        ret = True
    return ret


class SmartEnv(Env):  # type: ignore[misc]
    def __init__(self, **scheme: "SmartConfig") -> None:
        self.raw: SmartConfig = scheme  # type: ignore[assignment]
        self.explicit: list[str] = []
        values: dict[str, Any] = {}
        self.config: dict[str, ConfigVar] = {}

        for k, v in scheme.items():
            self.config.setdefault(
                k,
                {
                    "cast": lambda x: x,
                    "default": Env.NOTSET,
                    "develop": Env.NOTSET,
                    "explicit": False,
                    "help": "",
                },
            )
            try:
                cast, default_value, *extras = v
                self.config[k]["cast"] = cast  # type: ignore[typeddict-item]
                self.config[k]["default"] = default_value
                self.config[k]["develop"] = default_value
                values[k] = (cast, default_value)
                if len(extras) >= 1:  # noqa PLR2004
                    self.config[k]["develop"] = extras[0]
                if len(extras) >= 2:  # noqa PLR2004
                    self.config[k]["explicit"] = bool(extras[1])
                if len(extras) >= 3:  # noqa PLR2004
                    self.config[k]["help"] = extras[2]

            except TypeError:
                values[k] = v

        super().__init__(**values)

    def get_develop_value(
        self, var: str, cast: Callable[[Any], Any] | None = None, default: Any = Env.NOTSET, parse_default: bool = False
    ) -> Any:
        return self.config[var]["develop"]

    def get_value(
        self, var: str, cast: Callable[[Any], Any] | None = None, default: Any = Env.NOTSET, parse_default: bool = False
    ) -> Any:
        try:
            cast = self.raw[var][0]  # type: ignore[index]
        except KeyError:
            raise SmartEnvMissingVarError(var) from None
        except TypeError:
            cast = self.raw[var]  # type: ignore[assignment]
            if cast is bool:
                cast = smart_bool
        value = super().get_value(var, cast, default, parse_default)
        if cast is bool:
            value = smart_bool(value)
        return value

    def bool(self, var: str, default: Any = Env.NOTSET) -> bool:
        return bool(self.get_value(var, cast=smart_bool, default=default))

    def storage(self, value: str) -> dict[str, Any] | None:
        raw_value = self.get_value(value, str)
        if not raw_value:
            return None
        options = {}
        if "?" in raw_value:
            value, args = raw_value.split("?", 1)
            for entry in args.split("&"):
                k, v = entry.split("=", 1)
                options[k] = v
        else:
            value = raw_value

        return {"BACKEND": value, "OPTIONS": options}

    def is_valid(self) -> bool:  # type: ignore[valid-type] # noqa: A003
        return not self.check_explicit()

    def check_explicit(self) -> list[str]:
        missing = []
        for k, cfg in sorted(self.config.items()):
            if cfg["explicit"] and k not in self.ENVIRON:
                missing.append(k)
        return missing
