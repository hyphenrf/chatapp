import socket
import sys

def connect(addr=None, port=None):
    s = socket
    global server
    server = (addr or '0.0.0.0'), (port or 2021)
    client = s.socket(s.AF_INET, s.SOCK_STREAM)
    client.connect(server)
    return client

if __name__ == '__main__':
    with connect() as client:
        try:
            while 1:
                myname = input("username: ")
                client.send(f"10 {myname} \r\n".encode())
                reply = client.recv(2050).decode()
                while not reply:
                    print("waiting reply")
                    reply = client.recv(2050).decode()
                if reply[0] == '2':
                    print("username ok.")
                    break
                if reply[0] == '5':
                    raise ConnectionError
                if reply[0] == '4':
                    print("username taken.")

            while 1:
                cmd = input("> ")
                client.send(f"20 {myname} \r\n{cmd}".encode())
                reply = client.recv(2050).decode()
                if reply[0] == '2':
                    header, message = reply.split("\r\n")
                    _, sender, _ = header.split(" ")
                    print(f"{sender}: {message}")

        except ConnectionError:
            print('server unavailable.')
        except Exception as e:
            print(e)
            pass
