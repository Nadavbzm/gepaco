import socket

UDP_CONNECTION = "UDP"
TCP_CONNECTION = "TCP"

def create_udp_socket():
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  
    sock.bind(("127.0.0.1", 8080))
    return sock

def create_socket(connection_type, ip, port):
    if connection_type == UDP_CONNECTION:
        return create_udp_socket(), True
