class LoggerMixIn:
    """
    A mixin class for adding logging capabilities to other classes.

    This mixin provides a simple logging mechanism to display messages and warnings
    based on a specified display_logs flag.

    Attributes:
        display_logs (bool): A boolean flag indicating whether to display logs.
            If True, logs will be displayed; if False, logs will be suppressed.

    Methods:
        __init__(self, display_logs: bool):
            Initialize the LoggerMixIn instance with the specified display_logs flag.

        _log(self, identifier: str, msg: str):
            Internal method to log a message with a given identifier.

        log_msg(self, msg: str):
            Log a general message with an asterisk (*) identifier.

        log_warning(self, msg: str):
            Log a warning message with an exclamation mark (!) identifier.
    """

    def __init__(self, display_logs: bool):
        """
        Initialize a LoggerMixIn instance.

        Args:
            display_logs (bool): A boolean flag to control log display.
                If True, logs will be printed; if False, logs will be suppressed.
        """
        self.display_logs: bool = display_logs

    def _log(self, identifier: str, msg: str):
        """
        Log a message with a specified identifier.

        Args:
            identifier (str): The log identifier character.
            msg (str): The message to be logged.
        """
        if self.display_logs is True:
            print(f"[{identifier}] {msg}")

    def log_msg(self, msg: str):
        """
        Log a general message with an asterisk (*) identifier.

        Args:
            msg (str): The message to be logged.
        """
        self._log("*", msg)

    def log_warning(self, msg: str):
        """
        Log a warning message with an exclamation mark (!) identifier.

        Args:
            msg (str): The warning message to be logged.
        """
        self._log("!", msg)
