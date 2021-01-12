import socket
from getpass import getpass

myname = input("username: ")
mypass = getpass("password? [hit enter to login without password] ")

recipient = ""

def connect(addr=None, port=None):
    s = socket
    inet = addr or '0.0.0.0'
    port = port or 2021
    addr = inet, port
    client = s.socket(s.AF_INET, s.SOCK_STREAM | s.SOCK_NONBLOCK)
    client.connect(addr)
    return client

def recv_loop(client):
    while True:
        data = client.recv(2050).decode()
        header, body = data.split('\r\n')
        code, user, meta = header.split(' ')
        code = int(code)
        if code == 20:
            body and print(body)

def send_loop(client):
    while True:
        header = f"20 {myname} "
        message = input(myname + "> ")
        data = header + "\r\n" + message
        client.send(data.encode())

while __name__ == '__main__':
    try:
        with connect() as client:
            tx = Thread(target=send_loop, args=client)
            rx = Thread(target=recv_loop, args=client)
            break
    except:
        continue

if __name__ == '__main__':
    rx.join()
    tx.join()
