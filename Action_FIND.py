import pyautogui
import time
from datetime import datetime
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
                pyautogui.moveTo(1022, 430, duration=1)  # Safe scroll area
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

