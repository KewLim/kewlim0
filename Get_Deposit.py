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


def copy_table_html_from_devtools():
    """Automates copying table HTML from Chrome DevTools with RGB color check."""

    pyautogui.moveTo(1010, 600, duration=.5)  
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.write('tbody', interval=.1)
    pyautogui.moveTo(1041, 131, duration=.5)  # Make sure on first row

    # ✅ Wait for expected RGB before proceeding
    check_x, check_y = 488, 430
    expected_rgb = (255, 255, 255)  # <- Replace with the actual RGB you expect
    timeout = 20  # seconds
    interval = 0.2  # check interval

    print(f"⏳ Waiting for RGB at ({check_x}, {check_y}) to be {expected_rgb}...")

    start_time = time.time()
    while True:
        current_rgb = pyautogui.pixel(check_x, check_y)
        if current_rgb == expected_rgb:
            print(f"✅ RGB matched: {current_rgb}")
            break
        elif time.time() - start_time > timeout:
            print(f"❌ Timeout! Expected RGB {expected_rgb} not found.")
            return  # or raise an exception if you want to stop the script
        time.sleep(interval)

    # ✅ Proceed after RGB is matched
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'c')  # Copy HTML
    time.sleep(1)

    






gateway_groups = defaultdict(list)

def extract_and_group_by_gateway():
    """Extracts order data from clipboard HTML and appends to global gateway_groups."""
    global gateway_groups  # Needed to modify the global variable

    html_data = pyperclip.paste()
    soup = BeautifulSoup(html_data, "html.parser")
    rows = soup.find_all("tr")

    for i, row in enumerate(rows):
        tds = row.find_all("td")
        if len(tds) < 22:
            continue

        order_id = tds[0].text.strip()
        phone_number = tds[6].text.strip()
        amount = tds[10].text.strip()
        time_str = tds[20].text.strip()
        payment_gateway = tds[21].text.strip()

        # Prevent duplicates (optional: skip if order ID already exists in the same gateway)
        existing_ids = [r["Order ID"] for r in gateway_groups[payment_gateway]]
        if order_id in existing_ids:
            continue

        gateway_groups[payment_gateway].append({
            "Order ID": order_id,
            "Phone Number": phone_number,
            "Amount": amount,
            "Time": time_str
        })




def print_grouped_results():
    """Prints all grouped data and writes it to 'transaction_history.txt'."""
    grand_total = 0  # <-- Make sure this is declared at the top

    with open("transaction_history.txt", "w", encoding="utf-8") as f:
        for gateway, records in gateway_groups.items():
            total_amount = sum(float(record["Amount"].replace(",", "")) for record in records)
            grand_total += total_amount  # <-- Accumulate total for grand total

            header = f"\n==== {gateway} ({len(records)} record{'s' if len(records) != 1 else ''}) | Total Amount: Rs {total_amount:,.2f} ====\n"
            print(f"\033[92m{header}\033[0m")
            f.write(header)

            # Sort records by time (latest first)
            sorted_records = sorted(
                records,
                key=lambda r: datetime.strptime(r["Time"], "%Y-%m-%d %H:%M:%S"),
                reverse=True
            )

            # Enumerate only once per record
            for i, record in enumerate(sorted_records, 1):
                entry = (
                    f"\nRecord #{i}\n"
                    f"Order ID: {record['Order ID']}\n"
                    f"Phone Number: {record['Phone Number']}\n"
                    f"Amount: {record['Amount']}\n"
                    f"Time: {record['Time']}\n"
                )
                print(f"\033[94m{entry}\033[0m")
                f.write(entry)

            footer = f"\n>> Total Amount for {gateway}: Rs {total_amount:,.2f}\n"
            print(f"\033[93m{footer}\033[0m")
            f.write(footer)

        # ✅ Add grand total at the end
        grand_footer = f"\n==== GRAND TOTAL for All Gateways: Rs {grand_total:,.2f} ====\n"
        print(f"\033[95m{grand_footer}\033[0m")
        f.write(grand_footer)





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
# image_path = 'img/Approved.png'
search_region = (635, 929, 500, 500)


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
extract_and_group_by_gateway()
click_if_next_button_found(image_path, search_region, click_x=643, click_y=938)
wait_for_overlay_to_disappear()

while True:
    copy_table_html_from_devtools()
    extract_and_group_by_gateway()

    # Wait for the overlay to clear before looking for the next button
    wait_for_overlay_to_disappear()

    success = click_if_next_button_found(image_path, search_region, click_x=0, click_y=0)

    if not success:
        print("No next button found. Stopping.")
        break

    # Give the next page time to load
    time.sleep(0.5)

# Called after loop ends
print_grouped_results()


