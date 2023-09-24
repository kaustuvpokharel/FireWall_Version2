from threading import Thread


class ThreadManager:
    """
    A utility class for managing threads in Python applications.

    This class provides a simple way to create and manage threads, allowing
    you to run functions in separate threads and manage their execution.

    Attributes:
        active_threads (list[Thread]): A list of active (running) threads.
        inactive_threads (list[Thread]): A list of inactive (not yet started) threads.

    Methods:
        run_in_thread(self, execute_when_called: bool = False) -> callable:
            A decorator function for running a function in a thread.

        run_inactive_threads(self):
            Start all inactive threads in the queue.

        wait_for_all_active_threads(self):
            Wait for all active threads to complete their execution.
    """

    def __init__(self):
        """
        Initialize a ThreadManager instance with empty active and inactive thread lists.
        """
        self.active_threads: list[Thread] = []
        self.inactive_threads: list[Thread] = []

    def run_in_thread(self, execute_when_called: bool = False) -> callable:
        """
        Decorator function for running a function in a thread.

        Args:
            execute_when_called (bool): If True, the thread starts immediately when
                the decorated function is called. If False, the thread is added to
                the inactive_threads list and can be started later.

        Returns:
            callable: The decorator function.
        """

        def accept_function(func: callable):
            def accept_parameters(*args, **kwargs):
                thread = Thread(target=func, daemon=True, args=args, kwargs=kwargs)

                if execute_when_called:
                    thread.start()
                    self.active_threads.append(thread)
                else:
                    self.inactive_threads.append(thread)

            return accept_parameters

        return accept_function

    def run_inactive_threads(self):
        """
        Start all inactive threads in the queue.
        """
        for thread in self.inactive_threads:
            thread.start()
            self.inactive_threads.append(thread)

        self.inactive_threads = []

    def wait_for_all_active_threads(self):
        """
        Wait for all active threads to complete their execution.
        """
        for thread in self.active_threads:
            thread.join()


thread_manager = ThreadManager()
