import pyautogui
import time

# Step 1: Load phone numbers from the text file
def load_phone_numbers(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

phone_numbers = load_phone_numbers("phone_numbers.txt")

# Switch 1 tab (assuming you want to switch to the browser/app)
pyautogui.keyDown('alt')
pyautogui.press('tab')
time.sleep(0.1)  
pyautogui.keyUp('alt')
print("Switched window!")

# Step 2: Paste phone number into both fields using pyautogui.write()
def paste_phone_number_twice(phone_number):
    print(f"Pasting phone number: {phone_number}")  # Debug output

    # Click 'Add New Player'
    pyautogui.moveTo(1796, 231, duration=0.1)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(1)

    # Enter first phone number field
    pyautogui.moveTo(987, 271, duration=0.1)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.write(phone_number, interval=0.05)

    # Enter second phone number field
    pyautogui.moveTo(987, 360, duration=0.1)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.write(phone_number, interval=0.05)

    # Click the Apply button
    pyautogui.moveTo(1224, 928, duration=0.1)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(5)  # Adjust if the system needs more time to process

# Step 3: Main loop
for number in phone_numbers:
    paste_phone_number_twice(number)
