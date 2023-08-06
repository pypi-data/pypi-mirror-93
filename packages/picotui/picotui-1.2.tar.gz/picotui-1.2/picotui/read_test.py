import sys
if sys.implementation.name == "micropython":
    import pycopy
    from os import read
    import uselect as select
    USE_POLL = 1
else:
    from posixread import read
    import select
    USE_POLL = 0
import signal
import errno

resized = False

def sig_winch(sig, stk=None):
    print("winch")
    global resized
    resized = True

signal.signal(signal.SIGWINCH, sig_winch)

stdin_poller = select.poll()
stdin_poller.register(0, select.POLLIN)

while True:
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
            data = read(0, 32)
    except OSError as e:
#        print("OSError")
        if e.args[0] != errno.EINTR:
            raise

    if resized:
        print("resized")
        resized = False
    print("data:", data)
