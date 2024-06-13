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
