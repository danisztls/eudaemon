#!/usr/bin/env python

"""
Eudaemon: Monitor and log activity, improve awareness and empower user to improve it's habits.
"""

import asyncio
import time
import subprocess
import os
from collections import deque
import dbus  # https://dbus.freedesktop.org/doc/dbus-python/

# TODO: dbus-python is deprecated, use dasbus instead
# https://dasbus.readthedocs.io/en/latest/index.html

DEBUG = False
POLLING_RATE = 2  # pollings per second
POLLING_INTERVAL = 1 / POLLING_RATE  # interval in seconds between each polling
ACTIVITY_THRESHOLD = 10  # time in seconds without activity required to consider as idle
EVALUATION_WINDOW = 15 * 60  # period in seconds of evaluations
HISTORY_SIZE = POLLING_RATE * EVALUATION_WINDOW  # max length of deque

"""Detect desktop enviroment and initialize accordingly."""


def get_desktop_env():
    # TODO: Detect if X11, Gnome or KDE Wayland.
    return "gnome"


"""Monitor user idleness."""


class IdlenessMonitor:
    def __init__(self, desktop_env):
        self.env = desktop_env
        self.history = deque(maxlen=HISTORY_SIZE)

    def get_idle_time(self):
        if self.env == "gnome":
            session_bus = dbus.SessionBus()
            bus_object = session_bus.get_object(
                "org.gnome.Mutter.IdleMonitor", "/org/gnome/Mutter/IdleMonitor/Core"
            )
            bus_interface = dbus.Interface(bus_object, "org.gnome.Mutter.IdleMonitor")
            return bus_interface.GetIdletime() / 1000

        else:
            # TODO: Use https://github.com/g0hl1n/xprintidle/ for X11
            # TODO: Use https://github.com/swaywm/swayidle for KDE Wayland
            raise Exception(f"Getting idle time for {self.env} isn't implemented")

    def register_idleness(self):
        idle_time = self.get_idle_time()
        if idle_time >= ACTIVITY_THRESHOLD:
            state = "IDLE"
        else:
            state = "ACTIVE"
        self.history.append(state)
        if DEBUG:
            print(state)

    def evaluate_activeness(self):
        activeness_frequency = self.history.count("ACTIVE") / HISTORY_SIZE
        print(
            f"Eudaemon: {activeness_frequency * 100 }% active in past {int(EVALUATION_WINDOW / 60)}m"
        )


# TODO: Feed data to a time series database. e.g. Postgres TimeScale

# Warn

# TODO: Send desktop notifications with libnotify

# Act

# Log Out
# subprocess.run(["gnome-session-quit", "logout"])
# subprocess.run(["gnome-session-quit", "logout --force"])
# subprocess.run([ "dbus-send", "--session --type=method_call --print-reply --dest=org.gnome.SessionManager /org/gnome/SessionManager org.gnome.SessionManager.Logout uint32:1"])

# Strings.

# Whatever you're doing prolly can wait till tomorrow. Forcing yourself to be awaken doesn't make sense. Sooner or later you will have to sleep and this bad habit is unproductive and unhealthy.

""" A clock that runs a sub-procedure at a periodic rate. """


def clock(loop, delay, func, *func_args):
    args = [loop, delay, func]
    loop.call_later(delay, clock, *args)
    func(*func_args)


def main():
    desktop_env = get_desktop_env()
    monitor = IdlenessMonitor(desktop_env)
    loop = asyncio.new_event_loop()
    polling_args = [loop, POLLING_INTERVAL, monitor.register_idleness]
    loop.call_soon(clock, *polling_args)
    evaluation_args = [loop, EVALUATION_WINDOW, monitor.evaluate_activeness]
    loop.call_later(EVALUATION_WINDOW, clock, *evaluation_args)
    loop.run_forever()
    loop.close()  # not needed as the program doesn't terminate gracefully


if __name__ == "__main__":
    main()
