import os
import time
from test import crc, client, server

if __name__ == "__main__":
    crc.runtest()
    input("Press Enter to test server & client")

    sp = os.fork()
    if sp == 0:
        server.runtest()
    else:

        cp = os.fork()
        if cp == 0:
            time.sleep(1)
            client.runtest()
        else:
            os.wait()
    
        os.wait()
