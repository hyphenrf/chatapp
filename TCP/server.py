import socket
import threading

myname = "chatserver"
sessions = {
    #"chatserver": <socket>
}

def listen(addr=None, port=None):
    s = socket
    inet = addr or '0.0.0.0'
    port = port or 2021
    addr = inet, port
    server = s.socket(s.AF_INET, s.SOCK_STREAM)
    server.bind(addr)
    server.listen()
    return server

def handle(conn, addr):
    while 1:
        message = conn.recv(2050).decode()
        print("Got connection")
        header, body = message.split('\r\n',1)
        code, user, _ = header.split(' ')
        code = int(code)
        if code == 10:
            print("registering", user)
            if sessions.get(user):
                conn.send(b"43  \r\n")
                continue
            else:
                sessions[user] = conn
                conn.send(b"23  \r\n")

        elif code == 20 and sessions.get(user):
            print("got a message")
            todo = list(sessions.items())
            for user, conn in todo:
                try:
                    conn.send(f"{20} {user} \r\n{body}".encode())
                except BrokenPipeError:
                    del sessions[user]


if __name__ == '__main__':
    with listen() as server:
        while True:
            try: #TODO: I don't know what I'm doing..
                client = server.accept()
                client and threading.Thread(target=handle, args=client).start()
            except Exception as e:
                print(e)
                pass
