import crc

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
    return f"{code} {user} {meta}\r\n{body}".encode()

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
    sessions = {"server": None}

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr

    """We use raise here as a defer mechanism to jump around the stack, like in Golang"""
    def handle(self):
        try:
            data = self.conn.recv(buffer).decode()
            header, body = data.split('\r\n')
            code, name, meta = header.split(' ')

            if code == 10 or code == 12:
                raise User(code, name)
            if code == 20:
                raise Message(name, body)
            else:
                raise Server(40)

        except User as exn:
            user = str(exn)
            sess = ServerHandler.sessions
            resp = 43
            if not user in sess:
                sess[name] = self.conn
                resp = 23
            self.conn.send(User(resp, name))

        except Message as exn:
            sess = ServerHandler.sessions
            for user, conn in list(sess.items()):
                # we create a copy by issuing list cast
                try:
                    conn.send(exn)
                except BrokenPipeError:
                    del sess[user]

        except Server:
            try:
                self.conn.send(Server)
            except:
                pass

        except Exception as e:
            print(e)

        finally:
            self.conn.close()


class ClientHandler:

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr

    def handle(self):
        data = self.conn.recv(buffer)
        if not crc.verify(data):
            raise Corrupted

        data = data.decode()
        header, body = data.split('\r\n')
        code, name, meta = header.split(' ')


        if code == 20:
            print(f"{name}: {body}")
        elif code == 23:
            print(f"registered as {name}")
            raise User(23, name)
        elif code == 43:
            print(f"username {name} is taken")
            raise User(43, name)
        elif code in {40, 50, 53}:
            print(f"{name}: {meta}")
            if code == 53:
                raise ConnectionError

    def __del__(self):
        self.conn.close()

