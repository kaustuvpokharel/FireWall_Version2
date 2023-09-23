import socket
import time
from threading import Thread
from firewall import LLSM

CLIENT_ADDRESS = any


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


class LoggerMixIn:
    def __init__(self, display_logs: bool):
        self.display_logs: bool = display_logs

    def _log(self, identifier: str, msg: str):
        if self.display_logs is True:
            print(f"[{identifier}] {msg}")

    def log_msg(self, msg: str):
        self._log("*", msg)


class SocketManager(LoggerMixIn):
    MAX_CLIENTS: int = 10
    CHECK_FOR_NEW_CLIENTS: float = 0.4  # times in seconds: To recheck for new clients!

    def __init__(self, server_ip: str, server_port: int, display_logs: bool = False):
        super().__init__(display_logs)

        self.server_ip = server_ip
        self.server_port = server_port

        self.clients: (socket, any) = []
        self.active_clients: set[str] = set()

        self.server_socket: socket.socket | None = None

    def _initialize_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(self.MAX_CLIENTS)

        self.log_msg(f"Server listening on {self.server_ip}:{self.server_port}")

    @thread_manager.run_in_thread(execute_when_called=True)
    def _accept_connection(self):
        while True:
            client_data: (socket, CLIENT_ADDRESS) = self.server_socket.accept()
            self.clients.append(client_data)

            self.log_msg(f"Accepted connection from {client_data[1]}")

    def handle_request(self):
        raise NotImplementedError("Please implement handle_request")

    def accept_requests(self):
        self._initialize_socket()
        self._accept_connection()
        self.handle_request()


class Brain(SocketManager):
    @thread_manager.run_in_thread(execute_when_called=True)
    def _handle_connected_client(self, client_socket: socket):
        while True:
            # Receive a message from the client
            message = client_socket.recv(1024).decode('utf-8')
            print(f"Client: {message}")

            # Send a response back to the client
            response = input("Server: ")
            client_socket.send(response.encode('utf-8'))

    def handle_request(self):
        while True:
            for client_socket, client_ip in self.clients:
                if client_ip not in self.active_clients:
                    self._handle_connected_client(client_socket)
                    self.active_clients.add(client_ip)

            time.sleep(self.CHECK_FOR_NEW_CLIENTS)


if __name__ == "__main__":
    brain = Brain("127.0.0.1", 12345, display_logs=True)
    brain.accept_requests()
