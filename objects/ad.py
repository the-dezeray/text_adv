import psutil
import pygetwindow as gw
import time

def get_active_window():
    window = gw.getActiveWindow()
    if window:
        return window.title
    return None

while True:
    active_window = get_active_window()
    if active_window:
        print(f"Active Window: {active_window}")
    time.sleep(2)  # Check every 2 seconds
