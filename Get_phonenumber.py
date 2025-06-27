import pyautogui
import time
from datetime import datetime
import re
import pyperclip
import pytz
import pyperclip
from bs4 import BeautifulSoup
from collections import defaultdict
import sys
from pyautogui import ImageNotFoundException  # Needed to catch the specific exception


def copy_table_html_from_devtools():
    """Automates copying table HTML from Chrome DevTools."""

    pyautogui.moveTo(1010, 600, duration=.5)  
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.write('tbody', interval=.1)
    pyautogui.moveTo(1041, 131, duration=.5)  # Make sure on first row

 
    pyautogui.click()

    # Copy the selected element's HTML
    pyautogui.hotkey('ctrl', 'c')  
    # pyautogui.hotkey('ctrl', 'shift', 'c')  # Close DevTools Arrow to prevent blue overlay

    time.sleep(1) 


def hover_on_image(image_path, search_region, timeout=10):
    """
    Repeatedly searches for an image in a region and hovers the mouse over it if found.
    Stops if not found within the timeout period.
    
    Parameters:
        image_path (str): Path to the image to search for.
        search_region (tuple): (left, top, width, height) defining the search area.
        timeout (int): Maximum time to wait in seconds.
    """
    start_time = time.time()

    while time.time() - start_time < timeout:
        location = pyautogui.locateOnScreen(image_path, region=search_region, confidence=0.8)
        if location:
            center = pyautogui.center(location)
            pyautogui.moveTo(center.x, center.y, duration=0.2)
            print(f"Hovered on image at: {center}")
            return
        time.sleep(0.2)

    print("Image not found within timeout.")


phone_numbers = []

def extract_and_group_by_phone_number():
    """Extracts only phone numbers from clipboard HTML and stores in phone_numbers list."""
    global phone_numbers

    html_data = pyperclip.paste()
    soup = BeautifulSoup(html_data, "html.parser")
    rows = soup.find_all("tr")

    for row in rows:
        tds = row.find_all("td")
        if len(tds) < 17:
            continue

        phone_number = tds[16].text.strip()
        if phone_number and phone_number not in phone_numbers:
            phone_numbers.append(phone_number)

def print_grouped_results():
    """Prints only phone numbers from the list."""
    for number in phone_numbers:
        print(number)



def click_if_next_button_found(image_path, search_region, click_x, click_y, confidence=0.9):
    """
    Click the center of the found image if it exists in the region. 
    If not found, call print_grouped_results() and exit the program.
    """
    print(f"Searching for '{image_path}' in region {search_region}...")
    try:
        location = pyautogui.locateOnScreen(image_path, region=search_region, confidence=confidence)
        if location:
            center_x, center_y = pyautogui.center(location)
            print(f"Image found. Moving to center at ({center_x}, {center_y}) and clicking...")
            pyautogui.moveTo(center_x, center_y, duration=0.2)
            time.sleep(0.1)  # small pause for stability
            pyautogui.click()
            print("\033[93mCLICKED NEXT BUTTON\033[0m")
            return True
        else:
            raise ImageNotFoundException  # Explicitly raise if None (optional safety)
    except ImageNotFoundException:
        print("Image not found. Calling print_grouped_results() and exiting.")
        print_grouped_results()
        sys.exit()



image_path = 'img/next_button.png'
search_region = (631, 917, 500, 500)


def wait_for_overlay_to_disappear(x=447, y=438, loading_color=(102, 102, 102), timeout=20, check_interval=0.2):
    """
    Waits until the pixel at (x, y) is no longer the loading color.
    Proceeds only when the loading overlay has disappeared.
    """
    print("Waiting for loading overlay to disappear...")
    start_time = time.time()

    while True:
        current_color = pyautogui.pixel(x, y)

        print("DEBUG COLOR:", current_color)

        if current_color != loading_color:
            print(f"Overlay finished. Current color: {current_color}")
            time.sleep(0.5)  # Let the page settle before clicking
            break
        if time.time() - start_time > timeout:
            print("Timeout: Loading overlay did not disappear.")
            sys.exit()
        time.sleep(check_interval)




# ==== Function called here ====

# Switch 1 tab
pyautogui.keyDown('alt')
pyautogui.press('tab')
time.sleep(0.1)  
pyautogui.keyUp('alt')

print("Switched window!")

time.sleep(0.5)  

pyautogui.hotkey('ctrl', 'shift', 'i')  # Opens DevTools
pyautogui.moveTo(378, 500, duration=.1)
pyautogui.scroll(-300) # Make sure at bottom
# pyautogui.hotkey('ctrl', 'shift', 'c')  # Opens DevTools


time.sleep(1) 


copy_table_html_from_devtools()
extract_and_group_by_phone_number()
click_if_next_button_found(image_path, search_region, click_x=643, click_y=928)
wait_for_overlay_to_disappear()

while True:
    copy_table_html_from_devtools()
    extract_and_group_by_phone_number()

    # Wait for the overlay to clear before looking for the next button
    wait_for_overlay_to_disappear()

    success = click_if_next_button_found(image_path, search_region, click_x=0, click_y=0)

    if not success:
        print("No next button found. Stopping.")
        break

    # Give the next page time to load
    time.sleep(0.5)

# Called after loop ends