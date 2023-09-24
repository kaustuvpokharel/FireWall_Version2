import socket

from thread_management import thread_manager
from utils.logging import LoggerMixIn


class SocketManager(LoggerMixIn):
    """
    A class for managing server sockets and handling client connections.

    This class provides functionality for creating a server socket, accepting client
    connections, and handling client requests. It also includes basic logging capabilities.

    Attributes:
        MAX_CLIENTS (int): The maximum number of clients that the server can handle.
        CHECK_FOR_NEW_CLIENTS (float): The time interval (in seconds) for rechecking
            for new client connections.

    Methods:
        __init__(self, server_ip: str, server_port: int, display_logs: bool = False):
            Initialize a SocketManager instance.

        _initialize_socket(self):
            Initialize the server socket and start listening for client connections.

        _accept_connection(self):
            Accept incoming client connections and log them.

        handle_request(self):
            Handle client requests. This method should be implemented by subclasses.

        accept_requests(self):
            Start the server socket, accept incoming connections, and handle requests.

    """

    MAX_CLIENTS: int = 10
    CHECK_FOR_NEW_CLIENTS: float = 0.4  # times in seconds: To recheck for new clients!

    def __init__(self, server_ip: str, server_port: int, display_logs: bool = False):
        """
        Initialize a SocketManager instance.

        Args:
            server_ip (str): The IP address to bind the server socket to.
            server_port (int): The port number to bind the server socket to.
            display_logs (bool): A boolean flag indicating whether to display logs.
                If True, logs will be printed; if False, logs will be suppressed.
        """
        super().__init__(display_logs)

        self.server_ip = server_ip
        self.server_port = server_port

        self.clients: list[(socket.socket, any)] = []
        self.active_clients: set[str] = set()

        self.server_socket: socket.socket | None = None

    def _initialize_socket(self):
        """
        Initialize the server socket and start listening for client connections.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(self.MAX_CLIENTS)

        self.log_msg(f"Server listening on {self.server_ip}:{self.server_port}")

    @thread_manager.run_in_thread(execute_when_called=True)
    def _accept_connection(self):
        """
        Accept incoming client connections and log them.
        """
        while True:
            client_data: (socket, any) = self.server_socket.accept()
            self.clients.append(client_data)

            self.log_msg(f"Accepted connection from {client_data[1]}")

    def handle_request(self):
        """
        Handle client requests.

        This method should be implemented by subclasses to define the behavior
        when handling client requests.
        """
        raise NotImplementedError("Please implement handle_request")

    def accept_requests(self):
        """
        Start the server socket, accept incoming connections, and handle requests.
        """
        self._initialize_socket()
        self._accept_connection()
        self.handle_request()
