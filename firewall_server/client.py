import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server's IP address and port
server_ip = '192.168.88.148'
server_port = 12345

# Connect to the server
client_socket.connect((server_ip, server_port))

while True:
    # Send a message to the server
    message = input("Client: ")
    client_socket.send(message.encode('utf-8'))
