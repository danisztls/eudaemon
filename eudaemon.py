#!/usr/bin/env python3

"""
Monitor and log usage, detect bad habits, warn user about it and act as last resort on extreme cases.
"""

__author__  = "Daniel Souza <me@posix.dev.br>"
__license__ = "MIT"

import asyncio
import time
import subprocess
import os
import dbus

# Design

# 1. I stay for hours sitted in the computer. Doing exercises from time to time it is critical for blood flow and health. When I'm focused I have no control over that.

# 2. Everything nowadays farms for our attention. I'm particularly vulnerable to this and addicted to games.

"""Detect desktop enviroment and initialize accordingly."""
def get_desktop_env():
    # LATER: Detect X11, Gnome and KDE Wayland.
    return "gnome"

desktop_env = get_desktop_env()

if (desktop_env == "gnome"):
    session_bus = dbus.SessionBus()
    bus_object = session_bus.get_object('org.gnome.Mutter.IdleMonitor', '/org/gnome/Mutter/IdleMonitor/Core')
    bus_interface = dbus.Interface(bus_object, 'org.gnome.Mutter.IdleMonitor')

"""Detect user activity/idleness."""
class Monitor():
    def get_idle_time():
        if (desktop_env == "gnome"):
            return bus_interface.GetIdletime() / 1000

        else:
            # LATER: Use https://github.com/g0hl1n/xprintidle/ for X11
            # LATER: Use https://github.com/swaywm/swayidle for KDE Wayland
            return "not implemented yet"

    def print_idle():
        idle_time = Monitor.get_idle_time()
        print(idle_time)

""" A clock that runs a sub-procedure at a periodic rate. """
def clock(delay=1):
    loop.call_later(delay, clock, delay)
    Monitor.print_idle()
    return

loop = asyncio.new_event_loop()
loop.call_soon(clock, 1)
loop.run_forever()
loop.close()

# Log

# TODO: Set up a database.

# A TSDB like InfluxDB would be nice to have as a complementary integration but to bloated to have as default.
# The ideal would a no-server local DB. SQLite in the lack of a better alternative.

# Warn

# TODO: Send desktop notifications with libnotify

# Act

# Log Out
# subprocess.run(["gnome-session-quit", "logout"])
# subprocess.run(["gnome-session-quit", "logout --force"])
# subprocess.run([ "dbus-send", "--session --type=method_call --print-reply --dest=org.gnome.SessionManager /org/gnome/SessionManager org.gnome.SessionManager.Logout uint32:1"])

# Analyze

# TODO: Graph logged time. 

# Strings.

# Whatever you're doing prolly can wait t'll tomorrow. Forcing yourself to be awaken doesn't make sense. Sooner or later you will have to sleep and this bad habit is unproductive and unhealthy.

# Oww, champion. You're playing too much. Haven't got anything more important to do gonk?
