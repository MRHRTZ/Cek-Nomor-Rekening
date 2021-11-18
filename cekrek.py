#!/usr/bin/python3

import signal
from lib.classes import CheckNorek
hz = CheckNorek()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, hz.signal_handler)
    hz = CheckNorek()
    hz.getAllBank()
    hz.main()
    signal.pause()
