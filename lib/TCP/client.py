import socket
import sys

def connect(addr=None, port=None):
    s = socket
    server = (addr or '0.0.0.0'), (port or 2021)
    client = s.socket(s.AF_INET, s.SOCK_STREAM)
    return client, server

