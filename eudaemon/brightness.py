import time
import subprocess
import datetime
import re
import asyncio
from .utils import run_periodic_task, notify_desktop

DEBUG = False
UPDATE_INTERVAL = 15 * 60  #  time in seconds between updates
STEPS_N = 10  # number of update smoothing steps


def check_env() -> bool:
    """Check if dccutil is available"""
    try:
        subprocess.check_output(["ddcutil", "--version"])
    except FileNotFoundError:
        print(
            "ddcutil is not installed. Please install it to manage display brightness."
        )
        return False

    return True


def get_brightness() -> int:
    """Get display brightness"""
    output = subprocess.run(["ddcutil", "getvcp", "10"], capture_output=True)
    text = str(output.stdout)
    match = re.search(r"current value = [ ]+([0-9]+)", text)
    if match:
        value = int(match.group(1))
        if value >= 0 and value <= 100:
            return value
    return None


def set_brightness(value: int) -> None:
    """Set display brightness"""
    subprocess.run(["ddcutil", "setvcp", "10", str(value)])


def calc_brightness() -> int:
    """Calculate and return the desired brightness value"""
    # TODO: Get sunrise/sunset data via astral
    now = datetime.datetime.now().time()
    sunrise = datetime.time(5, 40)
    sunset = datetime.time(18, 15)

    # brightness is a value between 0 and 100
    if now < sunrise or now > sunset:
        brightness = 0
    elif now >= sunrise and now <= sunset:
        brightness = 50

    return brightness


def manage_brightness():
    initial = get_brightness()
    target = calc_brightness()

    if initial == target:
        return

    notify_desktop(
        f"Adjusting display brightness. Current: {initial}. Target {target}."
    )

    delta = target - initial

    if delta >= STEPS_N:
        steps = STEPS_N
    else:
        steps = delta

    increment = int(delta / steps)

    for n in range(steps):
        set_brightness(initial + increment * (n + 1))
        time.sleep(60)

    # ensure
    set_brightness(target)


loop = asyncio.new_event_loop()


def start() -> None:
    args = [loop, UPDATE_INTERVAL, manage_brightness]
    loop.call_soon(run_periodic_task, *args)
    loop.run_forever()


def stop():
    loop.close()


def main() -> None:
    if not check_env():
        return

    start()
    stop()


if __name__ == "__main__":
    main()
