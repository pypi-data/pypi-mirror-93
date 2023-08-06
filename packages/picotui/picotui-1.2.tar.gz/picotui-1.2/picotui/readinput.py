import sys
if sys.implementation.name == "micropython":
    import pycopy
    from os import read as read_
    import uselect as select
    USE_POLL = 1
else:
    from .posixread import read as read_
    import select
    USE_POLL = 0
import signal
import errno

stdin_poller = select.poll()
stdin_poller.register(0, select.POLLIN)

def read(fd, sz):
    try:
#        print("in sel")
        res = True
        if USE_POLL:
            res = stdin_poller.poll(-1)
#        print("out sel")
        data = None
#        print(res)
        if res:
#            print("before read")
            data = read_(fd, sz)
    except OSError as e:
#        print("OSError")
        if e.args[0] != errno.EINTR:
            raise

    return data
