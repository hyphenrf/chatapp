import socket
from threading import Thread #TODO: send and receive loops should be
                             #asynchronous for both server and client to
                             #achieve two-way communication.

myname = "chatserver"
sessions = {
    #"chatserver": {'conn':<socket>, 'pass':"passowrd", 'active': True}
}

def listen(addr=None, port=None):
    s = socket
    inet = addr or '0.0.0.0'
    port = port or 2021
    addr = inet, port
    server = s.socket(s.AF_INET, s.SOCK_STREAM | s.SOCK_NONBLOCK)
    server.bind(addr)
    server.listen()
    return server

def handle(conn, addr):
    print("Got connection")
    message = conn.recv(2050)
    header, _, body = message.partition(b'\r\n')
    code, user, meta = header.split(b' ')
    code = int(code)
    if code == 10:
        print("registering", user)
        sessions[user] = {'conn':conn, 'pass':None, 'active':True}
        conn.send(b"%d  %s\r\n" % (23, user))
    if code == 20 and sessions.get(user, None) and sessions.get(meta, None):
        print("got a message")
        print(conn)
        conn = sessions[meta]['conn']
        print(conn)
        conn.send(b"%d %s %s\r\n%s" % (23, "", user, body))

if __name__ == '__main__':
    with listen() as server:
        while True:
            try: #TODO: I don't know what I'm doing..
                client = server.accept()
                t = Thread(target=handle, args=client)
                t.start()
            except:
                pass
