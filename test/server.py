import lib.TCP.server as tcp
import lib.UDP.server as udp
import socket as s
import threading

from lib.handling import ServerHandler

def start_udp_server(ip, port):
    with udp.listen(ip, port) as s:
        while True:
            try:
                c = ServerHandler(s, None)
                c.handle()
            except Exception as e:
                print(e)

def start_tcp_server(ip, port):
    with tcp.listen(ip, port) as s:
        while True:
            try:
                conn, addr = s.accept()
                c = ServerHandler(conn, addr)
                c.handle()
            except Exception as e:
                print(e)

def runtest():
    print("Answer the following or hit enter for default\n")
    # ip = input("IP address: ") or "0.0.0.0"
    # ud = input("UDP port: ")   or 65432
    # tc = input("TCP port: ")   or 2021
    ip = "0.0.0.0"
    ud = 65432
    tc = 2021

    print(f"\nServer's IP adress: {s.gethostbyname(s.gethostname())}")

    t1 = threading.Thread(target=start_udp_server, args=(ip, ud))
    t2 = threading.Thread(target=start_tcp_server, args=(ip, tc))
    t1.start()
    t2.start()
    t1.join()
    t2.join() 

