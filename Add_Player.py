import pyautogui
import time

# Step 1: Load phone numbers from the text file in descending order
def load_phone_records(filename):
    """Loads phone records from file in descending order."""
    records = []
    with open(filename, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()][::-1]

    for line in lines:
        parts = [p.strip() for p in line.split(',')]
        if len(parts) == 3:
            phone, email, aff_code = parts
            records.append({
                "Phone Number": phone,
                "Email": email,
                "Affiliate Code": aff_code
            })
        else:
            print(f"⚠️ Skipping malformed line: {line}")
    return records

phone_numbers = load_phone_records("phone_numbers.txt")

# Switch 1 tab (assuming you want to switch to the browser/app)
pyautogui.keyDown('alt')
pyautogui.press('tab')
time.sleep(0.1)  
pyautogui.keyUp('alt')
print("Switched window!")

# Step 2: Paste phone number into both fields using pyautogui.write()
def paste_phone_number_twice(record):
    phone_number = record["Phone Number"]
    email = record["Email"]
    affiliate_code = record["Affiliate Code"]

    print(f"Pasting phone number: {phone_number}")  # Debug output

    # Click 'Add New Player'
    pyautogui.moveTo(1796, 231, duration=0.1)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(1)

    # Enter first phone number field
    pyautogui.moveTo(987, 265, duration=0.1)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.write(phone_number, interval=0.05)

    # Enter second phone number field
    pyautogui.moveTo(987, 355, duration=0.1)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.write(phone_number, interval=0.05)

    # ✅ Conditionally enter Email if it's not "-"
    if email != "-":
        pyautogui.moveTo(651, 342, duration=0.1)
        pyautogui.click()
        pyautogui.write(email, interval=0.05)
    else:
        print("⚠️ Email is '-', skipping email input.")

    # (📝 Reserved) Enter Affiliate Code
    pyautogui.moveTo(662, 590, duration=0.1)
    pyautogui.click()
    pyautogui.write(affiliate_code, interval=0.05)

    # (📝 Reserved) Enter Affiliate Code sec
    pyautogui.moveTo(662, 680, duration=0.1)
    pyautogui.click()
    pyautogui.write(affiliate_code, interval=0.05)
    





    # Click the Apply button
    pyautogui.moveTo(1224, 928, duration=0.1)
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(3)  # Adjust if the system needs more time to process

    check_x, check_y = 786, 188  # <- Replace with your pixel coordinate
    expected_rgb = (25, 33, 50)  # <- Replace with the RGB value to match
    timeout = 50                       # seconds
    interval = 0.2                     # check every 0.2 sec

    print("Waiting for color match...")

    start_time = time.time()
    while True:
        current_rgb = pyautogui.pixel(check_x, check_y)
        if current_rgb == expected_rgb:
            print("✅ RGB match found. Proceeding.")
            break
        elif time.time() - start_time > timeout:
            print("⛔ Timeout: RGB match not found after 20 seconds.")
            break
        time.sleep(interval)

    time.sleep(1)








# Step 3: Main loop
for number in phone_numbers:
    paste_phone_number_twice(number)
