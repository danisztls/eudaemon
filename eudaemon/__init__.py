#!/usr/bin/env python

"""
Eudaemon: Monitor and log activity, improve awareness and empower user to improve it's habits.
"""

import asyncio
import time
import subprocess
import os
import dbus # https://dbus.freedesktop.org/doc/dbus-python/

# TODO: dbus-python is deprecated, use dasbus instead
# https://dasbus.readthedocs.io/en/latest/index.html

"""Detect desktop enviroment and initialize accordingly."""
def get_desktop_env():
    # TODO: Detect if X11, Gnome or KDE Wayland.
    return "gnome"

"""Monitor user idleness."""
class IdlenessMonitor():
    def __init__(self, desktop_env):
        self.env = desktop_env

    def get_idle_time(self):
        if (self.env == "gnome"):
            session_bus = dbus.SessionBus()
            bus_object = session_bus.get_object('org.gnome.Mutter.IdleMonitor', '/org/gnome/Mutter/IdleMonitor/Core')
            bus_interface = dbus.Interface(bus_object, 'org.gnome.Mutter.IdleMonitor')
            return bus_interface.GetIdletime() / 1000

        else:
            # TODO: Use https://github.com/g0hl1n/xprintidle/ for X11
            # TODO: Use https://github.com/swaywm/swayidle for KDE Wayland
            raise Exception(f"Getting idle time for {self.env} isn't implemented")

    def print_idle(self):
        idle_time = self.get_idle_time()
        print(idle_time)

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
def clock(loop, delay, func):
    args = [loop, delay, func]
    loop.call_later(delay, clock, *args)
    func()

def main():
    desktop_env = get_desktop_env()
    monitor = IdlenessMonitor(desktop_env)
    loop = asyncio.new_event_loop()
    args = [loop, 1, monitor.print_idle]
    loop.call_soon(clock, *args)
    loop.run_forever()
    loop.close() # not needed as the program doesn't terminate gracefully

if __name__ == "__main__":
    main()
