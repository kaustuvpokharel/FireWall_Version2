class LoggerMixIn:
    def __init__(self, display_logs: bool):
        self.display_logs: bool = display_logs

    def _log(self, identifier: str, msg: str):
        if self.display_logs is True:
            print(f"[{identifier}] {msg}")

    def log_msg(self, msg: str):
        self._log("*", msg)
