#!/usr/bin/env python

"""
Eudaemon: Monitor and log activity, improve awareness and empower user to improve it's habits.
"""

import threading
from .idleness import main as idleness_monitor
from .brightness import main as brightness_monitor


def main():
    idleness = threading.Thread(target=idleness_monitor)
    brightness = threading.Thread(target=brightness_monitor)
    idleness.start()
    brightness.start()
    idleness.join()
    brightness.join()


if __name__ == "__main__":
    main()
