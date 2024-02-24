import subprocess
import time
import asyncio


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


def poweroff(env: str):
    """Power off the machine."""
    if env == "gnome":
        subprocess.run(["gnome-session-quit", "logout"])
        # subprocess.run(["gnome-session-quit", "logout --force"])
        # subprocess.run(
        #     [
        #         "dbus-send",
        #         "--session --type=method_call --print-reply --dest=org.gnome.SessionManager /org/gnome/SessionManager org.gnome.SessionManager.Logout uint32:1",
        #     ]
        # )
    else:
        raise Exception(f"Power off from {env} isn't implemented")


def run_periodic_task(loop, delay, func, *args):
    """Run a function periodically without drifting."""
    start = time.monotonic()
    while True:
        now = time.monotonic()
        error = (now - start) % delay
        time.sleep(max(0, delay - error))
        loop.create_task(func(*args))


async def run_periodic_task_async(background_tasks, delay, func, *args):
    """Run an async function periodically without blocking or drifting."""
    start = time.monotonic()
    while True:
        now = time.monotonic()
        error = (now - start) % delay
        await asyncio.sleep(max(0, delay - error))
        task = asyncio.create_task(func(*args))
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)
