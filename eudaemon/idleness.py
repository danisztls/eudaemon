import asyncio
import threading
from collections import deque
from dbus_fast.aio import MessageBus  # https://dbus-fast.readthedocs.io/
from .utils import run_periodic_task_async, notify_desktop, get_desktop_env

DEBUG = False 
POLLING_RATE = 2  # pollings per second
POLLING_INTERVAL = 1 / POLLING_RATE  # interval in seconds between each polling
ACTIVITY_THRESHOLD = 10  # time in seconds without activity required to consider as idle
EVALUATION_WINDOW = 60 * 60  # length in seconds of the window used for evaluation
EVALUATION_INTERVAL = 10 * 60  # time in seconds between evaluations
HISTORY_LENGTH = POLLING_RATE * EVALUATION_WINDOW  # max length of deque
HISTORY_BUFFER = deque(maxlen=HISTORY_LENGTH)
NOTIFICATION_THRESHOLD = 0.75  # percent
DESKTOP_ENV = get_desktop_env()

LOOP = asyncio.new_event_loop()
TASKS = set()

async def init_dbus_interface():
    """Init D-Bus for polling"""
    try:
        bus = await MessageBus().connect()

        if DESKTOP_ENV == "gnome":
            introspection = await bus.introspect(
                "org.gnome.Mutter.IdleMonitor", "/org/gnome/Mutter/IdleMonitor/Core"
            )

            proxy_object = bus.get_proxy_object(
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
        print(state)


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

def start():
    """Start threads"""
    thread_poll = threading.Thread(target=start_poll)
    thread_eval = threading.Thread(target=start_eval)
    thread_eval.start()
    thread_poll.start()
    thread_poll.join()
    thread_eval.join()

    
def main():
    start()

if __name__ == "__main__":
    main()
