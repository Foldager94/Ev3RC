import socket

def create_server_socket(port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)
    return server_socket

def accept_connection(server_socket):
    print("Waiting for connection...")
    client_socket, addr = server_socket.accept()
    print("Connected to:", addr)
    return client_socket


def read_from_arduino():
    try:
        # Read one byte from the Arduino
        data = i2c.read(1)
        print("Received data:", data)
    except Exception as e:  
        print("Failed to read from Arduino:", e)

def write_to_arduino(value):
    try:
        # Write one byte to the Arduino
        i2c.write(value)
        print("Sent data:", value)
    except Exception as e:
        print("Failed to write to Arduino:", e)