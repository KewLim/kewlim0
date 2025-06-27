import pyautogui
import time
from datetime import datetime
import re
import pyperclip
import pytz
import os
import sys
import tkinter as tk
from tkinter import simpledialog

# Switch 1 tab
pyautogui.keyDown('alt')
pyautogui.press('tab')
time.sleep(0.5)  
pyautogui.keyUp('alt')

print("Switched window!")

time.sleep(0.5)  

# === COPY date string from screen ===
pyautogui.click(1705, 814)  # example coordinate to select date string
time.sleep(0.2)
pyautogui.hotkey('ctrl', 'c')
time.sleep(0.2)
clipboard_text = pyperclip.paste()

# === Switch to Tab 1 ===
pyautogui.hotkey('ctrl', '1')

# === Extract Day from Date String ===
def extract_day_from_datetime(text):
    match = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", text)
    if match:
        try:
            dt = datetime.strptime(match.group(), "%Y-%m-%d %H:%M:%S")
            return str(dt.day).zfill(2)  # e.g. "23"
        except ValueError:
            return None
    return None

day_str = extract_day_from_datetime(clipboard_text)
if not day_str:
    print("❌ Could not extract date from clipboard.")
    sys.exit()

# === Build image path dynamically ===
image_path = f"rocketgo_date_select/{day_str}.png"
print(f"✅ Using image path: {image_path}")

# === Define function (will run LATER) ===
def find_and_hover_image_in_region(
    image_path,
    region,
    confidence=0.8,
    timeout=10,
    check_interval=0.5
):
    print(f"Looking for '{image_path}' in region {region} with confidence >= {confidence}...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, region=region, confidence=confidence)
        except Exception as e:
            print(f"Error: {e}")
            location = None

        if location is not None:
            center = pyautogui.center(location)
            print(f"Image found at {center}. Moving mouse.")
            pyautogui.moveTo(center)
            return

        time.sleep(check_interval)

    print(f"Timeout: '{image_path}' not found in region.")
    sys.exit()


# Select PG
pyautogui.moveTo(460, 240, duration=.5)
time.sleep(0.5)  
pyautogui.click() 
time.sleep(0.5)  
pyautogui.moveTo(460, 520, duration=.5)
time.sleep(0.5)  
pyautogui.scroll(-250) # Select YTpay
time.sleep(1)  
pyautogui.click() 
time.sleep(.5)  



# Coordinates RGB Validation
def color_matches(c1, c2, tolerance=5):
    return all(abs(a - b) <= tolerance for a, b in zip(c1, c2))

def wait_for_pixel_color(x, y, target_color, timeout=30, check_interval=0.2):
    print(f"Waiting for pixel at ({x}, {y}) to become {target_color}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        current_color = pyautogui.pixel(x, y)
        print(f"Current color at ({x}, {y}): {current_color}")
        if color_matches(current_color, target_color):
            print(f"Pixel changed to approximately {target_color}. Proceeding.")
            return
        time.sleep(check_interval)

    print(f"Timeout: Pixel at ({x}, {y}) did not change to {target_color} within {timeout} seconds.")
    pyautogui.screenshot("timeout_debug.png")
    sys.exit()

wait_for_pixel_color(325, 688, (38, 51, 77), check_interval=0.05)
time.sleep(0.5)



#Go for 'Add Transaction' button
pyautogui.moveTo(1726, 504, duration=.5)
time.sleep(.5)
pyautogui.click() 


# Continue with python Deposit_YTpay.py to get information


# Add details in RocketGO

# Select date 
pyautogui.moveTo(690, 290, duration=.5)
time.sleep(.5)
pyautogui.click() 
time.sleep(.5)

# Select month
pyautogui.moveTo(580, 325, duration=.5)
time.sleep(.5)
pyautogui.click() 
time.sleep(.5)

# Select month combo box
pyautogui.moveTo(580, 500, duration=.5)
time.sleep(.5)
pyautogui.click() 
time.sleep(.5)


# Select year
pyautogui.moveTo(727, 330, duration=.5)
time.sleep(.5)
pyautogui.doubleClick() 
time.sleep(.5)
pyautogui.write('2025', interval=0.1)
time.sleep(1)



# === Finally run the function ===
search_region = (512, 370, 400, 300)
find_and_hover_image_in_region(image_path, search_region, confidence=0.95)

# Optional: Click after hover
time.sleep(0.5)
pyautogui.click()