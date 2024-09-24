from typing import Any


class SmartEnvException(Exception):
    def __init__(self, key):
        self.msg = key


class SmartEnvMissing(SmartEnvException):

    def __str__(self):
        return f"Missing {self.msg}"


class SmartEnvConfigTypeError(SmartEnvException):
    def __init__(self, key: str, arg: int, t: type, value: Any):
        self.msg = key
        self.arg = arg + 2
        self.type = t.__name__
        self.value = value

    def __str__(self):
        return f"Invalid configuration for {self.msg}. Argument #{self.arg} should be {self.type}. It is {self.value}"
