
"""
A chat message is either a plain header, or header + "\r\n" + body
a header is code<space>user<space>meta, 1024 bytes max
a body is a message that's also 1024 bytes max

codes: client                 server
    10 announce username      -
    11 set password           give me password
    12 logout                 -
    20 message (outgoing)     message (incoming)
    21 -                      password auth success
    22 -                      password change success
    23 -                      username registry success
    24 -                      message delivered
    30 change username        -
    41 -                      password auth failure
    43 -                      username taken
    44 -                      user doesn't exist
    52 -                      general server error, try again
    53 -                      fatal error, don't try again
"""
