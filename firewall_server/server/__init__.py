import re
import time
from json import loads, dumps

from firewall.LSTM import LSTMPacketThreadDetection, ThreadDetection
from server.socket import SocketManager
from thread_management import thread_manager


class Brain(SocketManager):
    def __init__(
            self,
            server_ip: str,
            server_port: int,
            display_logs: bool = False,
            packet_per_batch: int = 100,
            thread_detector: ThreadDetection | None = None
    ):
        super().__init__(server_ip, server_port, display_logs)

        self.packet_per_batch = packet_per_batch
        self.packet_data = {
            "Timestamp": [],
            "PacketSize": [],
            "SourceIP": [],
            "DestinationIP": [],
            "SourcePort": [],
            "DestinationPort": []
        }

        self.thread_detector = thread_detector or LSTMPacketThreadDetection()

    @thread_manager.run_in_thread(execute_when_called=True)
    def _handle_connected_client(self, client_socket: socket):
        # try:
        pattern = r"\{[^}]*\}"
        faulty_data_count = 0

        while True:
            # Receive a message from the client
            message: str = client_socket.recv(1024).decode("utf-8").strip()
            parsed_data = re.findall(pattern, message, re.MULTILINE | re.DOTALL)
            # print(len(parsed_data))
            print(message, "@@@@@@@@@@@")
            if len(parsed_data) < 1:
                faulty_data_count += 1

            if faulty_data_count > 100:
                client_socket.close()
                self.log_warning(f"Session closed!")

                return

            for raw_json in parsed_data:
                try:
                    parsed_json = loads(raw_json)

                    self.packet_data["Timestamp"].append(parsed_json.get("Timestamp"))
                    self.packet_data["PacketSize"].append(parsed_json.get("Length"))
                    self.packet_data["SourceIP"].append(parsed_json.get("SourceIP"))
                    self.packet_data["DestinationIP"].append(parsed_json.get("DestinationIP"))
                    self.packet_data["SourcePort"].append(parsed_json.get("SourcePort"))
                    self.packet_data["DestinationPort"].append(parsed_json.get("DestinationPort"))
                except Exception as e:
                    print(e)

            if len(self.packet_data["Timestamp"]) > self.packet_per_batch:
                thread_level = self.thread_detector.predict(
                    timestamps=self.packet_data["Timestamp"],
                    packet_sizes=self.packet_data["PacketSize"],
                    source_ip=self.packet_data["SourceIP"],
                    destination_ip=self.packet_data["DestinationIP"],
                    source_port=self.packet_data["SourcePort"],
                    destination_port=self.packet_data["DestinationPort"],
                )

                print(dumps({
                    "threadLevel": thread_level,
                    "data": self.packet_data
                }))

                client_socket.send(dumps({
                    "threadLevel": thread_level,
                    "data": self.packet_data
                }).encode("utf-8"))
                self.packet_data = {
                    "Timestamp": [],
                    "PacketSize": [],
                    "SourceIP": [],
                    "DestinationIP": [],
                    "SourcePort": [],
                    "DestinationPort": []
                }
                # except Exception as _:
                #     print(_)
                #     client_socket.close()
                #     self.log_warning(f"Session closed!")

    def handle_request(self):
        while True:
            for client_socket, client_ip in self.clients:
                if client_ip not in self.active_clients:
                    self._handle_connected_client(client_socket)
                    self.active_clients.add(client_ip)

            time.sleep(self.CHECK_FOR_NEW_CLIENTS)
