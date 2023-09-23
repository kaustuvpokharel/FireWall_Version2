import time

from server.socket import SocketManager
from thread_management import thread_manager


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

