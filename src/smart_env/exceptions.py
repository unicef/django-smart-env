class SmartEnvError(Exception):
    def __init__(self, key: str) -> None:
        self.msg = key


class SmartEnvMissingVarError(SmartEnvError):
    def __str__(self) -> str:
        return f"Missing {self.msg}"
