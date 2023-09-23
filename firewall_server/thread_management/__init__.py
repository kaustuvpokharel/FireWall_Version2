from threading import Thread


class ThreadManager:
    def __init__(self):
        self.active_threads: list[Thread] = []
        self.inactive_threads: list[Thread] = []

    def run_in_thread(self, execute_when_called: bool = False):
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
        for thread in self.inactive_threads:
            thread.start()
            self.inactive_threads.append(thread)

        self.inactive_threads = []

    def wait_for_all_active_threads(self):
        for thread in self.active_threads:
            thread.join()


thread_manager = ThreadManager()
