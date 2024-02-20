import asyncio
from collections import deque
import dbus  # https://dbus.freedesktop.org/doc/dbus-python/
from .utils import clock, notify_desktop, get_desktop_env

# TODO: dbus-python is deprecated, use dasbus instead
# https://dasbus.readthedocs.io/en/latest/index.html

DEBUG = True
POLLING_RATE = 2  # pollings per second
POLLING_INTERVAL = 1 / POLLING_RATE  # interval in seconds between each polling
ACTIVITY_THRESHOLD = 10  # time in seconds without activity required to consider as idle
EVALUATION_WINDOW = 60 * 60  # length in seconds of the window used for evaluation
EVALUATION_INTERVAL = 10 * 60  # time in seconds between evaluations
HISTORY_SIZE = POLLING_RATE * EVALUATION_WINDOW  # max length of deque
NOTIFICATION_THRESHOLD = 0.9  # 90%

loop = asyncio.new_event_loop()


class IdlenessMonitor:
    """Monitor user idleness"""

    def __init__(self, env):
        self.env = env
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
        # TODO: Store time data (use nanoseconds as unit)
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
        # TODO: Handle non-continuous data (e.g. when a machine is suspended)
        freq = self.history.count("ACTIVE") / HISTORY_SIZE

        if freq > NOTIFICATION_THRESHOLD:
            self.notify(freq)

    def notify(freq):
        """Trigger user notification providing activty frequency and reminder to take a reak"""
        freq_str = "{:.2f}".format(freq * 100)
        interval_str = "{:.0f}".format(EVALUATION_WINDOW / 60)
        message = (
            f"{freq_str}% active in past {interval_str}m.\nConsider taking a break."
        )
        print(message)
        notify_desktop(message)


def start():
    env = get_desktop_env()
    monitor = IdlenessMonitor(env)
    poll_args = [loop, POLLING_INTERVAL, monitor.store]
    loop.call_soon(clock, *poll_args)
    eval_args = [loop, EVALUATION_INTERVAL, monitor.eval]
    loop.call_later(EVALUATION_INTERVAL, clock, *eval_args)
    loop.run_forever()


def stop():
    loop.close()


def main():
    start()
    stop()


if __name__ == "__main__":
    main()
