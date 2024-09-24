from typing import Any


class SmartEnvException(Exception):
    def __init__(self, key):
        self.msg = key


class SmartEnvMissing(SmartEnvException):

    def __str__(self):
        return f"Missing {self.msg}"
