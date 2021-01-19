import socket
import time

buffer_size = 1024


def create_udp_socket():
    global server_address
    server_address = ("192.168.1.13", 2021)
    # Create a UDP socket at client side
    global UDPClientSocket
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.settimeout(1)


def sendToServer(message):
    message = str.encode(message)
    UDPClientSocket.sendto(message, server_address)


def client_server_loop(message):
    # A function that performs a message round trip (client side)
    #    Client         --------------- Server
    # 1) send(msg|CRC)  --------------> check(msg|CRC)
    # 2) recv('ack')    <-------------- send('ack')
    sendToServer(message)
    try:
        msgFromServer = UDPClientSocket.recvfrom(buffer_size)
        if msgFromServer[0] == str.encode(message):
            return 1
    except socket.timeout:
        print("packet dropped")
    
    
    return 0


if __name__ == '__main__':
    n = int(input("How many messages to send? "))
    s = int(input("Size (in bytes) of each message? [1-180] "))

    success = 0

    create_udp_socket()

    print("Created udp socket")

    for i in range(n):
        message = str(time.time()) * 10
        message = message[::-1]
        message = message[:s]
        success += client_server_loop(message)
    print(f"Efficiency = {success/n*100}%")
