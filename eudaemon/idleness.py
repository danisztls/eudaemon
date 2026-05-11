import asyncio
from collections import deque
from dbus_fast.aio import MessageBus  # https://dbus-fast.readthedocs.io/
import os
import sys
import threading
from .utils import get_desktop_env, notify_desktop, run_periodic_task_async


DEBUG = os.environ.get("EUDAEMON_DEBUG", False)
POLLING_RATE = 2  # pollings per second
POLLING_INTERVAL = 1 / POLLING_RATE  # interval in seconds between each polling
ACTIVITY_THRESHOLD = 10  # time in seconds without activity required to consider as idle
EVALUATION_WINDOW = 60 * 60  # length in seconds of the window used for evaluation
EVALUATION_INTERVAL = 10 * 60  # time in seconds between evaluations
NOTIFICATION_THRESHOLD = 0.75  # percent
HISTORY_LENGTH = POLLING_RATE * EVALUATION_WINDOW  # max length of deque
HISTORY_BUFFER = deque(maxlen=HISTORY_LENGTH)
DESKTOP_ENV = get_desktop_env()
LOOP = asyncio.new_event_loop()
TASKS = set()
BUS = None


async def init_dbus_interface():
    """Init D-Bus for polling"""
    try:
        # TODO: Make this a class to better manage it instead of relying on globals
        global BUS
        BUS = await MessageBus().connect()

        if DESKTOP_ENV == "gnome":
            introspection = await BUS.introspect(
                "org.gnome.Mutter.IdleMonitor", "/org/gnome/Mutter/IdleMonitor/Core"
            )

            proxy_object = BUS.get_proxy_object(
                "org.gnome.Mutter.IdleMonitor",
                "/org/gnome/Mutter/IdleMonitor/Core",
                introspection,
            )
            interface = proxy_object.get_interface("org.gnome.Mutter.IdleMonitor")
            return interface

    except Exception as e:
        print(f"Error initializing D-Bus interface: {e}")
        return None

    else:
        # TODO: Use https://github.com/g0hl1n/xprintidle/ for X11
        # TODO: Use https://github.com/swaywm/swayidle for KDE Wayland
        raise Exception(f"Getting idle time for {DESKTOP_ENV} isn't implemented")


async def poll():
    """Poll D-Bus for idleness"""
    if DESKTOP_ENV == "gnome":
        interface = await init_dbus_interface()
        idle_time = await interface.call_get_idletime() / 1000
        store(idle_time)


def store(idle_time):
    """Store idleness data in memory"""
    # TODO: Store time data (use nanoseconds as unit)
    # TODO: Rework idle/active detection
    # Noisy input like small mouse movements caused by vibration will reset the idleness counter registering false activity.
    # Instead of using an actitivity threshold which is good only to filter out small periods of inactivity it would be better to log raw data with high resolution and filter out those outliers.
    # I can do data smoothing or even use statistical methods like bayesian filters.
    if idle_time >= ACTIVITY_THRESHOLD:
        state = "IDLE"
    else:
        state = "ACTIVE"
    HISTORY_BUFFER.append(state)
    if DEBUG:
        print(state)    except KeyboardInterrupt:
        print('Aborted manually.', file=sys.stderr)
        return 1

    except Exception as err:
        # (in real code the `except` would probably be less broad)
        # Turn exceptions into appropriate logs and/or console output.

        # non-zero return code to signal error
        # Can of course be more fine grained than this general
        # "something went wrong" code.
        return 1


async def evaluate():
    """Evaluate if data fits notification trigger criteria."""
    # TODO: Handle non-continuous data (e.g. when a machine is suspended)
    freq = HISTORY_BUFFER.count("ACTIVE") / HISTORY_LENGTH

    if freq > NOTIFICATION_THRESHOLD:
        notify(freq)


def notify(freq):
    """Trigger user notification providing activty frequency and reminder to take a reak"""
    freq_str = "{:.2f}".format(freq * 100)
    interval_str = "{:.0f}".format(EVALUATION_WINDOW / 60)
    message = f"{freq_str}% active in past {interval_str}m.\nConsider taking a break."
    print(message)
    notify_desktop(message)

def start_poll():
    asyncio.run(run_periodic_task_async(TASKS, POLLING_INTERVAL, poll))

def start_eval():
    asyncio.run(run_periodic_task_async(TASKS, EVALUATION_INTERVAL, evaluate))

thread_poll = threading.Thread(target=start_poll)
thread_eval = threading.Thread(target=start_eval)

# TODO: Just use daemon mode?
# https://stackoverflow.com/questions/58910372/script-stuck-on-exit-when-using-atexit-to-terminate-threads
def start():
    """Start threads"""
    thread_eval.start()
    thread_poll.start()

async def stop():
    """Terminate threads and close bus"""
    await BUS.wait_for_disconnect()
    thread_poll.join()
    thread_eval.join()

def main():
    try:
        start()

    except KeyboardInterrupt:
        print('Aborted manually.')
        sys.exit(1)

    except Exception as e:
        print(e)
        sys.exit(1)

    finally:
        asyncio.run(stop())

if __name__ == "__main__":
    main()
