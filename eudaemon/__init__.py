#!/usr/bin/env python

"""
Eudaemon: Monitor and log activity, improve awareness and empower user to improve it's habits.
"""

# from .idle_monitor import main as idle_monitor
from .idle_monitor import start as idle_monitor


# TODO: Set monitor brightness based on local time of day using I2C.

def main():
    idle_monitor()


if __name__ == "__main__":
    main()
