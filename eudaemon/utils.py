import subprocess


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
    """ "Power off the machine."""
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


def clock(loop, delay, func, *func_args):
    """A clock that runs a sub-procedure at a periodic rate."""
    args = [loop, delay, func]
    loop.call_later(delay, clock, *args)
    func(*func_args)
