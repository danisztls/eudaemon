#!/usr/bin/env python

"""
Monitor and log usage, detect bad habits, warn user about it and act as last resort on extreme cases.
"""

__author__  = "Daniel Souza <me@posix.dev.br>"
__license__ = "MIT"

import asyncio
import time

# Design

# 1. I stay for hours sitted in the computer. Doing exercises from time to time it is critical for blood flow and health. When I'm focused I have no control over that.

# 2. Everything nowadays farms for our attention. I'm particularly vulnerable to this and addicted to games.

# Implementation

# NOTE: Will not have the time to develop a complex software. Need this in a hurry.

# Monitor

# TODO: Implement async clock procedure.

period = 60 # 1 min?

def agent():
    def worker():
        loop.call_later(period, worker)
        ...        
        return

    loop = asyncio.new_event_loop()
    loop.call_soon(worker)
    loop.run_forever()
    loop.close()

    return


# TODO: Detect user activity. Use mouse/keyboard activity.

# Log

# TODO: Set up a database.

# A TSDB like InfluxDB would be nice to have as a complementary integration but to bloated to have as default.
# The ideal would a no-server local DB. SQLite in the lack of a better alternative.

# Warn

# TODO: Send desktop notifications with libnotify

# Act

# Log Out
subprocess.run(["gnome-session-quit", "logout"])
# subprocess.run(["gnome-session-quit", "logout --force"])
# subprocess.run([ "dbus-send", "--session --type=method_call --print-reply --dest=org.gnome.SessionManager /org/gnome/SessionManager org.gnome.SessionManager.Logout uint32:1"])

# Analyze

# TODO: Graph logged time. 


# Strings.

# Whatever you're doing prolly can wait t'll tomorrow. Forcing yourself to be awaken doesn't make sense. Sooner or later you will have to sleep and this bad habit is unproductive and unhealthy.

# Oww, champion. You're playing too much. Haven't got anything more important to do gonk?
