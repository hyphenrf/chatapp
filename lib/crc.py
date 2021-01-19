from os import path
from ctypes import cdll, create_string_buffer,\
        c_char_p, c_size_t, c_bool, c_byte

_ldpath = path.join("lib", "stubs", "libcrc.so")
_libcrc = cdll.LoadLibrary(_ldpath)

# byte lookup(byte message[static 1], word len);
# byte * chksum(byte message[static 1], word msglen, byte *buffer);
# bool verify(byte message[static 1], word msglen);

_lookup = _libcrc.lookup
_lookup.argtypes = (c_char_p, c_size_t)
_lookup.restype = c_byte

_chksum = _libcrc.chksum
_chksum.argtypes = (c_char_p, c_size_t, )
_chksum.restype = c_char_p

_verify = _libcrc.verify
_verify.argtypes = (c_char_p, c_size_t)
_verify.restype = c_bool

def lookup(s: bytes) -> int:
    return _lookup(s, len(s))

def chksum(s: bytes) -> bytes:
    ba = create_string_buffer(s)
    return _chksum(s, len(s), ba)

def verify(s: bytes) -> bool:
    return _verify(s, len(s))

