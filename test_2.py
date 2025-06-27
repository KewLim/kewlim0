import pyautogui
import time
from datetime import datetime
import pytz
import os
import sys
import tkinter as tk
from tkinter import simpledialog
import numpy as np
from PIL import ImageGrab  # Clean and warning-free


# Switch 1 tab
pyautogui.keyDown('alt')
pyautogui.press('tab')
time.sleep(0.5)  
pyautogui.keyUp('alt')

print("Switched window!")

time.sleep(0.5)  

#Double check panel position
pyautogui.moveTo(965, 150, duration=.1)
pyautogui.scroll(100)   

time.sleep(0.5)  


# === Start to search last Order ID ===
def get_order_id_from_user():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    order_id = simpledialog.askstring("Order ID Input", "Enter the Order ID to search:")
    if not order_id:
        print("No Order ID entered. Exiting.")
        exit()
    return order_id



def find_and_search_order_until_image_disappears(
    image_path,
    region,
    order_id,
    confidence=0.9,
    timeout=10,
    check_interval=0.5
):
    """
    Repeats scrolling and searching for Order ID on each page,
    until the image is no longer found in the given region.
    """

    # Step 0: Open Ctrl+F once and enter the order ID
    pyautogui.keyDown('ctrl')
    pyautogui.press('f')
    pyautogui.keyUp('ctrl')
    time.sleep(0.5)
    pyautogui.write(order_id, interval=0.1)
    time.sleep(0.5)
    

    while True:
        print(f"Looking for '{image_path}' in region {region} with confidence >= {confidence}...")

        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                location = pyautogui.locateOnScreen(image_path, region=region, confidence=confidence)
            except Exception:
                location = None

            if location is not None:
                center = pyautogui.center(location)
                print(f"Image '{image_path}' found at {center}. Proceeding with page scroll and search.")

                # Step 1: Scroll to bottom and click next page
                pyautogui.moveTo(1022, 430, duration=.1)  # Safe scroll area
                pyautogui.scroll(-300)
                pyautogui.moveTo(1857, 938, duration=1)  # Next page button
                pyautogui.click()
                time.sleep(2)

                # Step Last: Ctrl+F search for the order ID
                pyautogui.keyDown('ctrl')
                pyautogui.press('f')
                pyautogui.keyUp('ctrl')
                time.sleep(0.5)
                pyautogui.write(order_id, interval=0.1)
                time.sleep(0.5)

                break  # Go back to the outer loop and check again

            time.sleep(check_interval)

        else:
            # Timeout: image not found
            print(f"Image '{image_path}' no longer found in region. Ending process.")
            break


# === Run the function ===
image_path = 'img/not_found.png'
search_region = (1436, 90, 100, 80)  # Region where the "not found" image appears
order_id = get_order_id_from_user()

find_and_search_order_until_image_disappears(image_path, search_region, order_id, confidence=0.95)  



# == Hover mouse over the highlighted area ==
def find_color_and_hover_fast(region, target_rgb, tolerance=0, pixel_step=1):
    """
    region: (left, top, width, height)
    target_rgb: tuple (R,G,B)
    tolerance: int, how much difference to allow per channel
    pixel_step: int, subsampling step to reduce image size (1 = full res)
    """
    left, top, width, height = region
    right = left + width
    bottom = top + height

    # Grab region screenshot
    img = ImageGrab.grab(bbox=(left, top, right, bottom))

    # Convert to numpy array and subsample if pixel_step > 1
    img_np = np.array(img)[::pixel_step, ::pixel_step, :3]

    # Create mask of pixels within tolerance range of target_rgb
    r, g, b = target_rgb
    lower = np.array([r - tolerance, g - tolerance, b - tolerance])
    upper = np.array([r + tolerance, g + tolerance, b + tolerance])

    # Clip to valid range 0-255
    lower = np.clip(lower, 0, 255)
    upper = np.clip(upper, 0, 255)

    # Create boolean mask where pixels are in range
    mask = np.all((img_np >= lower) & (img_np <= upper), axis=2)

    # Get coordinates of matching pixels
    ys, xs = np.where(mask)

    if len(xs) == 0:
        print("No matching color found.")
        return

    # Calculate average position in original scale
    avg_x = int(xs.mean() * pixel_step) + left
    avg_y = int(ys.mean() * pixel_step) + top

    pyautogui.moveTo(avg_x, avg_y)
    print(f"Mouse moved to center of match at ({avg_x}, {avg_y})")

# --- USER CONFIGURATION ---
region = (195, 520, 80, 337)
target_rgb = (255, 150, 50)
tolerance = 10     # 0 = exact match, increase for color variance
pixel_step = 6     # skip pixels to speed up (try 2 or 3)

find_color_and_hover_fast(region, target_rgb, tolerance, pixel_step)

# 3/6 2:23am end (Done search highlighted area but now takes 11 sec to search and done hover mouse on centre)