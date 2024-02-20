import time
import subprocess
import datetime
import re
from .utils import notify_desktop

SUNRISE_TIME = 6
SUNSET_TIME = 18
STEPS_N = 10

def check_env():
    """Check if dccutil is available"""
    try:
        subprocess.run(["ddcutil", "--version"], check=True)
    except FileNotFoundError:
        print("ddcutil is not installed. Please install it to manage display brightness.")
        return False

    return True


def get_display_brightness() -> int:
    """Get display brightness"""
    output = subprocess.run(["ddcutil", "getvcp", "10"], capture_output=True)
    text = str(output.stdout)
    match = re.search(r'current value = [ ]+([0-9]+)', text)
    if match:
        value = int(match.group(1))
        if value >= 0 and value <=100:
            return value
    return None

def set_display_brightness(value: int):
    """Set display brightness"""
    subprocess.run(["ddcutil", "getvcp", "10", value])

def set_brightness(target: int):
    initial = get_display_brightness()

    if initial == target:
        return

    delta = target - initial
    increment = int(delta / STEPS_N)

    for n in range(STEPS_N):
        set_display_brightness(initial + increment * (n + 1))
        time.sleep(60)

    set_display_brightness(target)
    
def start():
    if not check_env():
        return

    # now = datetime.datetime.now()
