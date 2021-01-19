from . import crc

"""
A chat message is either a plain header, or header + "\r\n" + body
a header is code<space>user<space>meta, 1024 bytes max
a body is a message that's also 1024 bytes max

codes: client                 server
    10 announce username      -
    12 logout                 -
    20 message (outgoing)     message (incoming)
    23 -                      username registry success
    40 -                      bad request
    43 -                      username taken
    50 -                      general server error, try again
    53 -                      fatal error, don't try again
"""

buffer = 2050

def encode(code, user='', meta='', body=''):
    return crc.chksum(f"{code} {user} {meta}\r\n{body}".encode())

class Message(Exception):
    def __init__(self, name, body):
        self.value = name, body
    def __bytes__(self):
        return encode(20, self.value[0], body=self.value[1])
    def __eq__(self, other):
        type(self) == type(other)

class User(Exception):
    def __init__(self, code, user):
        self.value = code, user
    def __str__(self):
        return self.value[1]
    def __bytes__(self):
        return encode(*self.value)
    def __eq__(self, other):
        type(self) == type(other)

class Server(Exception):
    def __init__(self, code):
        self.code = code
    def __bytes__(self):
        responses = {40: "Bad Request", 50: "Temporary Error", 53: "Fatal Error"}
        return encode(self.code, "server", responses[self.code])
    def __eq__(self, other):
        type(self) == type(other)

class Corrupted(Exception):
    pass




class ServerHandler:
    sessions = dict()

    def __init__(self, sock, client=None):
        self.client = client

        def sendtcp(data, addr):
            assert addr, "Address must not be empty in sendtcp"
            with sock.connect(addr) as client:
                client.send(data)

        if not client:
            self.send = sock.sendto
            daddr = sock.recvfrom(buffer)
            assert len(daddr) == 2, "Didn't recv in init"
            self.data, self.addr = daddr
        else:
            assert len(client) == 2, "client empty in init"
            conn, self.addr = client
            self.send = sendtcp
            self.data = conn.recv(buffer)
            conn.close()

    """We use raise here as a defer mechanism, like in Golang but weaker"""
    def handle(self):
        try:
            data = self.data[:-1].decode('latin1')
            header, body = data.split('\r\n')
            code, name, meta = header.split(' ')
            code = int(code)

            if code == 10 or code == 12:
                raise User(code, name)
            if code == 20:
                raise Message(name, body)
            else:
                raise Server(40)

        except User as data:
            user = str(data)
            sess = ServerHandler.sessions
            resp = 43
            if not user in sess:
                sess[name] = self.addr
                resp = 23
            self.send(bytes(User(resp, name)), self.addr)

        except Message as data:
            data = bytes(data)
            sess = ServerHandler.sessions
            for user, addr in list(sess.items()):
                # we create a copy by issuing list cast
                try:
                    assert addr, f"{user}: addr is empty in message loop"
                    self.send(data, addr)
                except BrokenPipeError:
                    del sess[user]

        except Server as data:
            data = bytes(data)
            try:
                self.send(data, self.addr)
            except:
                pass

        except Exception as e:
            print(e)
            raise e

class DefaultClient:
    @staticmethod
    def log(text):
        print(text)

    @staticmethod
    def display(text):
        print(text)

    @staticmethod
    def prompt(text):
        return input(text)

class ClientHandler:
    username = None

    def __init__(self, sock, server=None, interface=DefaultClient):
        self.server = server
        self.ifc = interface

        if not server:
            self.data, self.addr = sock.recvfrom(buffer)
        else:
            conn, self.addr = server
            self.data = conn.recv(buffer)
            conn.close()

    def handle(self):
        try:
            data = self.data
            if not crc.verify(data):
                raise Corrupted

            data = data.decode('latin1')
            header, body = data.split('\r\n')
            code, name, meta = header.split(' ')
            code = int(code)


            if code == 20:
                raise Message(name, body)
            elif code == 23 or code == 43:
                raise User(code, name)
            elif code in {40, 50, 53}:
                if code == 53:
                    raise ConnectionError
                raise Server(code)

        except Message as data:
            data = bytes(data)
            self.ifc.display(data.decode('latin1'))

        except User as data:
            if code == 23:
                ClientHandler.username = name
            else:
                self.ifc.display(f"Username {name} Taken.")
                ClientHandler.username = self.ifc.prompt("Enter another username: ")

        except Server as data:
            data = bytes(data)
            self.ifc.log(data.decode('latin1'))

        except ConnectionError:
            self.ifc.log("ConnectionError")

        except Corrupted:
            self.ifc.log("Corrupted message")

