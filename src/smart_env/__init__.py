from typing import TYPE_CHECKING, Any, Union, Optional

from environ.environ import Env

from smart_env.exceptions import SmartEnvMissing

if TYPE_CHECKING:
    ItemValue = Union[str, bool, int, list[str], None]
    ConfigItem = Union[
        tuple[type, ItemValue],  # type, value
        tuple[type, ItemValue, str],  # type, value, help,
        tuple[type, ItemValue, str, Any],  # type, value, hell, develop_value
    ]


def smart_bool(value: str) -> Union[bool, str]:
    if value in (True, False):
        return value
    if not value:
        ret = False
    elif value.lower()[0] in ["t", "y", "1"]:
        ret = True
    elif value.lower()[0] in ["f", "n", "0"]:
        ret = False
    else:
        ret = True
    return ret


class SmartEnv(Env):
    def __init__(self, **scheme: "ConfigItem") -> None:
        self.raw: "dict[str, ConfigItem]" = scheme
        self.explicit: list[str] = []
        values: dict[str, Any] = {}
        self.config = {}
        for k, v in scheme.items():
            self.config.setdefault(
                k,
                {
                    "cast": None,
                    "default": Env.NOTSET,
                    "develop": Env.NOTSET,
                    "explicit": False,
                    "help": "",
                },
            )
            try:
                cast, default_value, *extras = v
                self.config[k]["cast"] = cast
                self.config[k]["default"] = default_value
                self.config[k]["develop"] = default_value
                values[k] = (cast, default_value)
                if len(extras) >= 1:
                    self.config[k]["develop"] = extras[0]
                if len(extras) >= 2:
                    # if not isinstance(extras[1], bool):
                    #     raise SmartEnvConfigTypeError(k, 1, bool, extras[1])
                    self.config[k]["explicit"] = extras[1]
                if len(extras) >= 3:
                    self.config[k]["help"] = extras[2]
                    # if not isinstance(extras[2], str):
                    #     raise SmartEnvConfigTypeError(k, 2, str, extras[2])

            except TypeError:
                values[k] = v

        super().__init__(**values)

    def get_develop_value(
        self, var: str, cast: callable = None, default: Any = Env.NOTSET, parse_default: bool = False
    ) -> Any:
        return self.config[var]["develop"]

    def get_value(self, var: str, cast: callable = None, default: Any = Env.NOTSET, parse_default: bool = False) -> Any:
        try:
            cast = self.scheme[var][0]
        except KeyError:
            raise SmartEnvMissing(var)
        except TypeError:
            cast = self.scheme[var]
            if cast is bool:
                cast = smart_bool
        value = super().get_value(var, cast, default, parse_default)
        if cast is bool:
            value = smart_bool(value)
        return value

    def bool(self, var: str, default: Any = Env.NOTSET) -> bool:
        return self.get_value(var, cast=smart_bool, default=default)

    def storage(self, value: str) -> Optional[Union[dict[str, Any]]]:
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

    def is_valid(self) -> bool:
        return not self.check_explicit()

    def check_explicit(self) -> list[str]:
        missing = []
        for k, cfg in sorted(self.config.items()):
            if cfg["explicit"] and k not in self.ENVIRON:
                missing.append(k)
        return missing
