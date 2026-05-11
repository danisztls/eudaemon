#!/usr/bin/env python

"""
Eudaemon: Monitor and log activity, improve awareness and empower user to improve it's habits.
"""

import signal
import sys
import threading
from .idleness import main as idleness_monitor
from .brightness import main as brightness_monitor

def stop(signum, frame):
    print("Caught signal %d. Exiting..." % signum)
    sys.exit(signum)

def main():
    signal.signal(signal.SIGINT, stop)
    idleness = threading.Thread(target=idleness_monitor)
    brightness = threading.Thread(target=brightness_monitor)
    idleness.start()
    brightness.start()
    idleness.join()
    brightness.join()


if __name__ == "__main__":
    main()
