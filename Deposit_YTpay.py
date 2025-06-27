import pyautogui
import time
from datetime import datetime
import pytz
import os
import sys


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
pyautogui.moveTo(965, 150, duration=.5)
pyautogui.scroll(100)   

time.sleep(0.5)  

#Select payment method
pyautogui.moveTo(1550, 225, duration=.5)
time.sleep(0.5)  
pyautogui.click() 
time.sleep(0.5) 
pyautogui.moveTo(1550, 510, duration=.5)
time.sleep(0.5)  
pyautogui.click() 

#Select date 1
pyautogui.moveTo(260, 274, duration=.5)
time.sleep(0.5) 
pyautogui.tripleClick()
tz = pytz.timezone("Asia/Kolkata")
today = datetime.now(tz)

# Format as YYYY-MM-DD
formatted_date = today.strftime("%Y-%m-%d")

time.sleep(.5)

# Type the date using pyautogui
pyautogui.write(formatted_date, interval=0.1)
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
pyautogui.write(formatted_date, interval=0.1)
time.sleep(.5)
pyautogui.press('enter')

time.sleep(.5)

#Check order status
pyautogui.moveTo(1110, 270, duration=.5)
time.sleep(.5)
pyautogui.click() 

time.sleep(.5)

#Select 'Approved' status
pyautogui.moveTo(1110, 367, duration=.5)
time.sleep(.5)
pyautogui.click() 

time.sleep(.5)

# Perform 'search' button
pyautogui.moveTo(1826, 466, duration=.5)
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

# Move to table
pyautogui.moveTo(888, 650, duration=.5)
time.sleep(1)


# Target Page Summary
def scroll_until_page_summary(
    image_path='img/page_summary.png',
    target_x=230,
    target_y=970,
    max_scrolls=10,       # Increase max scrolls for patience
    scroll_amount=-500,
    pause=1.0
):
    print("Scrolling to find 'Page Summary'...")

    region_width = max(150, 77)
    region_height = max(800, 20)
    region_x = target_x - region_width // 2
    region_y = target_y - region_height // 2
    region = (region_x, region_y, region_width, region_height)

    for i in range(max_scrolls):
        print(f"Scroll attempt {i+1}...")

        try:
            # Try locating image on screen in the region
            found = pyautogui.locateOnScreen(image_path, region=region, confidence=0.8)
        except pyautogui.ImageNotFoundException:
            found = None

        if found is not None:
            print(f"'Page Summary' found with confidence >= 0.8 after {i+1} scroll(s).")
            return True

        pyautogui.scroll(scroll_amount)
        time.sleep(pause)

    print("Failed to find 'Page Summary' after maximum scrolls.")
    sys.exit()


scroll_until_page_summary()





# Go for first order ID
image_path = 'img/page_summary.png'  
move_up_pixels = 30  

print("Looking for 'Page Summary'...")
location = pyautogui.locateOnScreen(image_path, confidence=0.8)

if location is None:
    print("Image not found on screen. Exiting.")
    sys.exit()


center_x, center_y = pyautogui.center(location)
pyautogui.moveTo(center_x, center_y, duration=0.3)
pyautogui.moveTo(center_x, center_y - move_up_pixels, duration=0.3)


print(f"Mouse moved to {move_up_pixels}px above 'Page Summary'.")

time.sleep(0.5) 
pyautogui.doubleClick()
pyautogui.hotkey('ctrl', 'c')


time.sleep(0.5) 

#Switch 2 tab
pyautogui.keyDown('alt')
pyautogui.press('tab')
time.sleep(0.5) 
pyautogui.press('tab')
time.sleep(0.5)  
pyautogui.keyUp('alt')

time.sleep(.5)

#Go for 'Add Transaction' button
pyautogui.moveTo(1726, 504, duration=.5)
time.sleep(.5)
pyautogui.click() 

