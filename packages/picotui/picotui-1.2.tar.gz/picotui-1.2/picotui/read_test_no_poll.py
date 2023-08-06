import sys
if sys.implementation.name == "micropython":
    import pycopy
    from os import read
else:
    from posixread import read
import signal
import errno

resized = False

def sig_winch(sig, stk=None):
    print("winch")
    global resized
    resized = True

signal.signal(signal.SIGWINCH, sig_winch)

while True:
    try:
        data = None
        data = read(0, 32)
    except OSError as e:
        print("OSError")
        if e.args[0] != errno.EINTR:
            raise

    if resized:
        print("resized")
        resized = False
    print("data:", data)
