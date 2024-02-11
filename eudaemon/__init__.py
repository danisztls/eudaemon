#!/usr/bin/env python

"""
Eudaemon: Monitor and log activity, improve awareness and empower user to improve it's habits.
"""

import asyncio
import time
import subprocess
import os
import dbus  # https://dbus.freedesktop.org/doc/dbus-python/

# dbus-python is deprecated, use dasbus instead
# https://dasbus.readthedocs.io/en/latest/index.html

"""Detect desktop enviroment and initialize accordingly."""
def get_desktop_env():
    # TODO: Detect if X11, Gnome or KDE Wayland.
    return "gnome"

"""Detect user idleness."""
class Monitor():
    def get_idle_time():
        if (desktop_env == "gnome"):
            return bus_interface.GetIdletime() / 1000

        else:
            # TODO: Use https://github.com/g0hl1n/xprintidle/ for X11
            # TODO: Use https://github.com/swaywm/swayidle for KDE Wayland
            return "not implemented"

    def print_idle():
        idle_time = Monitor.get_idle_time()
        print(idle_time)

""" A clock that runs a sub-procedure at a periodic rate. """
def clock(delay=1):
    loop.call_later(delay, clock, delay)
    Monitor.print_idle()
    return

# Warn

# TODO: Send desktop notifications with libnotify

# Act

# Log Out
# subprocess.run(["gnome-session-quit", "logout"])
# subprocess.run(["gnome-session-quit", "logout --force"])
# subprocess.run([ "dbus-send", "--session --type=method_call --print-reply --dest=org.gnome.SessionManager /org/gnome/SessionManager org.gnome.SessionManager.Logout uint32:1"])

# Strings.

# Whatever you're doing prolly can wait till tomorrow. Forcing yourself to be awaken doesn't make sense. Sooner or later you will have to sleep and this bad habit is unproductive and unhealthy.

def main():
    desktop_env = get_desktop_env()

    if (desktop_env == "gnome"):
        session_bus = dbus.SessionBus()
        bus_object = session_bus.get_object('org.gnome.Mutter.IdleMonitor', '/org/gnome/Mutter/IdleMonitor/Core')
        bus_interface = dbus.Interface(bus_object, 'org.gnome.Mutter.IdleMonitor')

    loop = asyncio.new_event_loop()
    loop.call_soon(clock, 1)
    loop.run_forever()
    loop.close()

if __name__ == "__main__":
    main()
