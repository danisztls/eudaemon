#!/usr/bin/env python

"""
Eudaemon: Monitor and log activity, improve awareness and empower user to improve it's habits.
"""

import asyncio
import subprocess
from collections import deque
import dbus  # https://dbus.freedesktop.org/doc/dbus-python/

# TODO: dbus-python is deprecated, use dasbus instead
# https://dasbus.readthedocs.io/en/latest/index.html

DEBUG = False
POLLING_RATE = 2  # pollings per second
POLLING_INTERVAL = 1 / POLLING_RATE  # interval in seconds between each polling
ACTIVITY_THRESHOLD = 10  # time in seconds without activity required to consider as idle
EVALUATION_WINDOW = 60 * 60  # length in seconds of the window used for evaluation 
EVALUATION_INTERVAL = 10 * 60  # time in seconds between evaluations 
HISTORY_SIZE = POLLING_RATE * EVALUATION_WINDOW  # max length of deque
NOTIFICATION_THRESHOLD = 0.9 # 90%


def get_desktop_env():
    """Detect desktop enviroment and initialize accordingly."""
    # TODO: Detect if X11, Gnome or KDE Wayland.
    return "gnome"


def notify_desktop(message) -> None:
    """Send notification to Desktop Environment"""
    summary = "Eudaemon"
    body = message
    cmd_list = ["notify-send", summary, body]

    try:
        subprocess.run(cmd_list, check=True)
    except OSError:
        print("Failed to send desktop notification.")


class IdlenessMonitor:
    """Monitor user idleness"""
    def __init__(self, desktop_env):
        self.env = desktop_env
        self.history = deque(maxlen=HISTORY_SIZE)

    def poll(self):
        """Poll the desktop environment for idleness"""
        if self.env == "gnome":
            session_bus = dbus.SessionBus()
            bus_object = session_bus.get_object(
                "org.gnome.Mutter.IdleMonitor", "/org/gnome/Mutter/IdleMonitor/Core"
            )
            bus_interface = dbus.Interface(bus_object, "org.gnome.Mutter.IdleMonitor")
            idle_time = bus_interface.GetIdletime() / 1000

        else:
            # TODO: Use https://github.com/g0hl1n/xprintidle/ for X11
            # TODO: Use https://github.com/swaywm/swayidle for KDE Wayland
            raise Exception(f"Getting idle time for {self.env} isn't implemented")

        return idle_time

    def store(self):
        """Store idleness data in memory"""
        idle_time = self.poll()
        if idle_time >= ACTIVITY_THRESHOLD:
            state = "IDLE"
        else:
            state = "ACTIVE"
        self.history.append(state)
        if DEBUG:
            print(state)

    def eval(self):
        """Evaluate if data fits notification trigger criteria."""
        freq = self.history.count("ACTIVE") / HISTORY_SIZE

        if freq > NOTIFICATION_THRESHOLD:
            self.notify(freq)

    def notify(freq):
        freq_str = "{:.2f}".format(freq * 100)
        interval_str = "{:.0f}".format(EVALUATION_WINDOW / 60)
        message = f"{freq_str}% active in past {interval_str}m"
        print(message)
        notify_desktop(message)


# Log Out
# subprocess.run(["gnome-session-quit", "logout"])
# subprocess.run(["gnome-session-quit", "logout --force"])
# subprocess.run([ "dbus-send", "--session --type=method_call --print-reply --dest=org.gnome.SessionManager /org/gnome/SessionManager org.gnome.SessionManager.Logout uint32:1"])


def clock(loop, delay, func, *func_args):
    """A clock that runs a sub-procedure at a periodic rate."""
    args = [loop, delay, func]
    loop.call_later(delay, clock, *args)
    func(*func_args)


def main():
    desktop_env = get_desktop_env()
    monitor = IdlenessMonitor(desktop_env)
    loop = asyncio.new_event_loop()
    poll_args = [loop, POLLING_INTERVAL, monitor.store]
    loop.call_soon(clock, *poll_args)
    eval_args = [loop, EVALUATION_INTERVAL, monitor.eval]
    loop.call_later(EVALUATION_INTERVAL, clock, *eval_args)
    loop.run_forever()
    loop.close()  # not needed as the program doesn't terminate gracefully


if __name__ == "__main__":
    main()
