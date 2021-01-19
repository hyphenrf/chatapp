import lib
import socket
import threading
import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from lib.handling import encode
from lib.crc import verify

buffer_size = 1024

ip = "0.0.0.0" #Of the server (Change to your pcs address)
tcp_port = 2021
udp_port = 65432

start_time = 0
n = 500 #number of messages to send for each message
s = 1000 #size of a message
udp_x_axis = []
udp_y_axis = []
tcp_x_axis = []
tcp_y_axis = []


#Starting UDP related code

def client_server_loop(message):
    # A function that performs a message round trip (client side)
    #    Client         --------------- Server
    # 1) send(msg)      --------------> recv(msg)
    # 2) recv(msg)      <-------------- send(msg)
    UDPClientSocket.sendto(encode(20, body=message), (ip, udp_port))
    try:
        msgFromServer = UDPClientSocket.recvfrom(buffer_size)
        if verify(msgFromServer[0]):
            return 1
        else:
            print("UDP: packet altered")
            time.sleep(0.15)
    except socket.timeout:
        print("UDP: packet dropped")

    return 0 #will be returned if packet is dropped or altered

def start_udp_client():
    global UDPClientSocket
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.settimeout(0.75)
    
    while True:
        UDPClientSocket.sendto(encode(10, "udptest"), (ip, udp_port))
        print(f"UDP: Sending packets with message width of {s} bytes")
        success = 0
        for i in range(n):
            message = str(time.time()) * 100
            message = message[::-1]
            message = message[:s]
            success += client_server_loop(message)
        success_percentage = success/n*100
        udp_x_axis.append(time.time()-start_time)
        udp_y_axis.append(success_percentage)
        #print(f"Efficiency for message size s of {s}b is {success_percentage}%")
        #print('-----------------------------------------------')


#Ending UDP related code

#Starting TCP related code

def start_tcp_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
        TCPClientSocket.connect((ip, tcp_port))
        while True:
            print(f"TCP: Sending packets with message width of {s} bytes")
            success = 0
            for i in range(n):
                message = str(time.time()) * 100
                message = message[::-1]
                message = message[:s]
                TCPClientSocket.sendall(encode(20, body=message))
                data = TCPClientSocket.recv(1024)
                if data:
                    success += 1
            success_percentage = success/n*100
            tcp_x_axis.append(time.time()-start_time)
            tcp_y_axis.append(success_percentage)
            
##            data = TCPClientSocket.recv(1024)
##            print('Received', repr(data))

#Ending TCP related code


def live_draw(i):
    plt.cla()

    plt.plot(udp_x_axis, udp_y_axis, label='UDP')
    plt.plot(tcp_x_axis, tcp_y_axis, label='TCP')
    plt.legend(loc='upper left')
    plt.xlabel('time') 
    plt.ylabel('efficiency percentage %')
    plt.title(f'Stress Test Efficiency for TCP/UDP protocols')
    plt.tight_layout()


def draw():
    plt.style.use('fivethirtyeight')
    ani = FuncAnimation(plt.gcf(), live_draw, interval=100)
    plt.show()


def runtest():
    start_time = time.time()
    t1 = threading.Thread(target=start_udp_client)
    t2 = threading.Thread(target=start_tcp_client)
    t1.start()
    t2.start()
    draw()
    t1.join()
    t2.join()
    print("Finished tests")

