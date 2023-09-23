import socket
import   # Import your neural model code

# Create a socket server to listen for Qt C++ data
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("ip here", port here))  # Use the same IP and port as in Qt C++ code
server.listen(1)

print("Waiting for Qt C++ connection...")
connection, address = server.accept()
print("Connected by", address)

while True:
    data = connection.recv(1024)  # Adjust buffer size as needed

    if not data:
        break

    # Perform prediction using your neural model
    packet_data = data.decode('utf-8')
    prediction = your_neural_model_module.predict(packet_data)

    # Send the prediction result back to Qt C++
    connection.send(prediction.encode())

connection.close()
