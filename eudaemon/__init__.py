#!/usr/bin/env python

"""
Eudaemon: Monitor and log activity, improve awareness and empower user to improve it's habits.
"""

from .idleness import main as idleness_monitor
from .brightness import main as brightness_monitor

def main():
    idleness_monitor()
    brightness_monitor()


if __name__ == "__main__":
    main()
