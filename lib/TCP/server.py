import socket

def listen(addr=None, port=None):
    s = socket
    inet = addr or '0.0.0.0'
    port = port or 2021
    addr = inet, port
    server = s.socket(s.AF_INET, s.SOCK_STREAM)
    server.bind(addr)
    server.listen()
    return server

