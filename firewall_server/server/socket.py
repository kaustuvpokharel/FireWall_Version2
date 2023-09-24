import socket

from thread_management import thread_manager
from utils.logging import LoggerMixIn

CLIENT_ADDRESS = any


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
