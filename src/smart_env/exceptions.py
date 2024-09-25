class SmartEnvException(Exception):
    def __init__(self, key: str) -> None:
        self.msg = key


class SmartEnvMissing(SmartEnvException):

    def __str__(self) -> str:
        return f"Missing {self.msg}"
