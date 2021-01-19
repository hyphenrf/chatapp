import socket

server_address = ("127.0.0.1", 2021)
bufferSize = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind(server_address)

print("UDP server up and listening")

# Listen for incoming datagrams

if __name__ == '__main__':
    print(f"Server's IP adress: {socket.gethostbyname(socket.gethostname())}")

    while (True): #main loop that echoes messages sent by the client
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        print(f"Received from client <{address}> message: {message}")

        UDPServerSocket.sendto(message, address)