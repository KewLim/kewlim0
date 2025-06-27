import pyautogui
import time

print("Press Ctrl+C to stop.")

try:
    while True:
        x, y = pyautogui.position()
        pixel_color = pyautogui.screenshot().getpixel((x, y))
        print(f"X: {x} Y: {y} RGB: {pixel_color}", end="\r")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopped.")