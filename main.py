import pyautogui
import time
from datetime import datetime
import pytz
import os
import sys
import tkinter as tk
from tkinter import simpledialog
from PIL import Image


print("Switching window in 3 seconds...")
time.sleep(1)
print("Switching window in 2 seconds...")
time.sleep(1)
print("Switching window in 1 seconds...")
time.sleep(1)



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

#Select payment method
pyautogui.moveTo(1550, 225, duration=.1)
time.sleep(0.5)  
pyautogui.click() 
time.sleep(0.5) 
pyautogui.moveTo(1550, 510, duration=.1)
time.sleep(0.5)  
pyautogui.click() 

#Select date 1
pyautogui.moveTo(260, 274, duration=.1)
time.sleep(0.5) 
pyautogui.tripleClick()
tz = pytz.timezone("Asia/Kolkata")
today = datetime.now(tz)

# Format as YYYY-MM-DD
formatted_date = today.strftime("%Y-%m-%d")

time.sleep(.5)

# Type the date using pyautogui
pyautogui.write(formatted_date, interval=0.01)
time.sleep(.5)
pyautogui.press('enter')



#Select date 2
pyautogui.moveTo(260, 322, duration=.5)
time.sleep(0.5) 
pyautogui.tripleClick()
tz = pytz.timezone("Asia/Kolkata")
today = datetime.now(tz)

# Format as YYYY-MM-DD
formatted_date = today.strftime("%Y-%m-%d")

# Optional: delay to focus the target window/input
time.sleep(.5)

# Type the date using pyautogui
pyautogui.write(formatted_date, interval=0.01)
time.sleep(.5)
pyautogui.press('enter')

time.sleep(.5)

#Check order status
pyautogui.moveTo(1110, 270, duration=.5)
time.sleep(.1)
pyautogui.click() 

time.sleep(.5)

#Select 'Approved' status
pyautogui.moveTo(1110, 367, duration=.1)
time.sleep(.5)
pyautogui.click() 

time.sleep(.5)

# Perform 'search' button
pyautogui.moveTo(1826, 466, duration=.1)
time.sleep(.5)
pyautogui.click()



# Wait for loading overlay to disappear
x, y = 187, 643  # Replace with the actual coordinates to monitor


# Known RGB color value after loading is complete (brighter version)
loaded_color = (102, 102, 102)  # Replace with the expected post-loading color


print("Waiting for loading overlay to disappear...")

# Loop until the pixel color matches the loaded state
while True:
    current_color = pyautogui.pixel(x, y)
    if current_color == loaded_color:
        print("Overlay finished.")
        break
    if time.time() - start_time > 10:  # Timeout after 10 seconds
        print("Timeout: Loading overlay did not disappear.")
        sys.exit()  # Exit the entire program
    time.sleep(0.2)


time.sleep(3)



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
def find_color_and_hover_fast(region, target_rgb, pixel_step=4):
    """
    region: (left, top, width, height)
    target_rgb: (R, G, B)
    pixel_step: number of pixels to skip per step
    """
    print(f"Scanning region {region} for color {target_rgb}...")

    # Capture screenshot using fast method
    img = ImageGrab.grab(bbox=region)
    img_np = np.array(img)

    color_pixels = []

    for y in range(0, img_np.shape[0], pixel_step):
        for x in range(0, img_np.shape[1], pixel_step):
            r, g, b = img_np[y, x][:3]
            if (r, g, b) == target_rgb:
                color_pixels.append((x, y))

    if not color_pixels:
        print("No matching color found.")
        return

    avg_x = sum(p[0] for p in color_pixels) // len(color_pixels) + region[0]
    avg_y = sum(p[1] for p in color_pixels) // len(color_pixels) + region[1]

    pyautogui.moveTo(avg_x, avg_y)  # Instant move
    print(f"Mouse moved to center of match at ({avg_x}, {avg_y})")

# --- USER CONFIGURATION ---
# Define your search region here: (left, top, width, height)
region = (195, 520, 80, 337)

# Define the target RGB color to look for
target_rgb = (255, 150, 50)  # yellow (change as needed)

# Run the function
find_color_and_hover_fast(region, target_rgb)