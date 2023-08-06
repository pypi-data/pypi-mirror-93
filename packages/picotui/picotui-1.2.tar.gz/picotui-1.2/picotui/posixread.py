import ctypes


libc = ctypes.CDLL("libc.so.6", use_errno=True)
buf = ctypes.create_string_buffer(32)


def read(fd, sz):
    sz = min(sz, 32)
    res = libc.read(0, buf, sz)
    if res >= 0:
        return buf[:res]
    raise OSError(ctypes.get_errno())
