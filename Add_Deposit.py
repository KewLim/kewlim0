import cv2
import numpy as np
import pyautogui
import time
import re
from datetime import datetime
import sys
import os



def find_and_hover_image_with_fallback(
    image_paths,
    region,
    confidence=0.95,
    timeout=10,
    check_interval=0.2
):
    start_time = time.time()
    while time.time() - start_time < timeout:
        for path in image_paths:
            try:
                location = pyautogui.locateOnScreen(path, region=region, confidence=confidence)
                if location:
                    center = pyautogui.center(location)
                    pyautogui.moveTo(center, duration=0.2)
                    print(f"✅ Found and hovered: {path}")
                    return path
            except Exception as e:
                print(f"[Error] Matching failed for {path}: {e}")
        time.sleep(check_interval)
    return None


def match_template_in_region(template_path, region, threshold=0.95):
    # 1. Take screenshot of the region
    screenshot = pyautogui.screenshot(region=region)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # 2. Load and convert template to grayscale
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # 3. Edge detection (optional but improves precision)
    screenshot_edges = cv2.Canny(screenshot, 50, 200)
    template_edges = cv2.Canny(template, 50, 200)

    # 4. Perform template matching
    result = cv2.matchTemplate(screenshot_edges, template_edges, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        print(f"✅ Match found with confidence {max_val:.2f}")
        # Return coordinates of the center of the matched region
        template_h, template_w = template.shape
        match_center = (region[0] + max_loc[0] + template_w // 2, region[1] + max_loc[1] + template_h // 2)
        return match_center
    else:
        print(f"❌ No match found (max confidence: {max_val:.2f})")
        return None


def gateway_setup_movement(gateway_name):
    print(f"\033[93m[Gateway Setup] Executing setup for {gateway_name}\033[0m")

    gateway_map = {
        "XYPAY": "XYPAY",
        "SKPAY": "SKPAY",
        "YTPAY": "YTPAY",
        "OSPAY": "OSPAY",
        "SIMPLYPAY": "SIMPLYPAY",
        "VADERPAY": "VADERPAY",
        "PASSPAY": "PASSPAY",
        "MULTIPAY": "MULTIPAY",
        "U9PAY": "U9PAY",
        "BOMBAYPAY": "BOMBAYPAY",
        "EPAY": "EPAY",
        "MOHAMMED AMEER ABBAS": "Karnataka Bank 2",
        "Test": "Test",
        "Test2" : "Test2"
    }

    if gateway_name in gateway_map:
        enter_gateway_name(gateway_map[gateway_name])


def enter_gateway_name(gateway_text):
    pyautogui.moveTo(299, 245, duration=0.1)
    pyautogui.scroll(500)
    time.sleep(0.2)
    pyautogui.moveTo(354, 239, duration=0.1)
    pyautogui.click()
    time.sleep(0.2)
    pyautogui.press('backspace')
    pyautogui.press('backspace')
    time.sleep(0.2)
    pyautogui.write(gateway_text, interval=0.1)
    time.sleep(0.2)
    pyautogui.press('enter')

    # --- RGB color match check (wait until matched) ---
    check_x, check_y = 318, 992
    expected_rgb = (38, 51, 77)
    interval = 0.2  # check every 0.2 seconds

    print("Waiting for color match...")

    while True:
        try:
            current_rgb = pyautogui.pixel(check_x, check_y)
            if current_rgb == expected_rgb:
                print("✅ RGB match found. Proceeding.")
                break
        except Exception as e:
            print(f"⚠️ Error checking pixel color: {e}")
        time.sleep(interval)




# === Define function (will run LATER) ===
def find_and_hover_image_in_region(
    image_path,
    region,
    confidence=0.95,
    timeout=10,
    check_interval=0.5
):
    start_time = time.time()

    while time.time() - start_time < timeout:
        # Take screenshot of the region
        screenshot = pyautogui.screenshot(region=region)
        screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

        # Load and preprocess template
        template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print(f"\033[91m[Error] Failed to load image: {image_path}\033[0m")
            return False

        # Edge detection for both images
        screenshot_edges = cv2.Canny(screenshot_gray, 50, 200)
        template_edges = cv2.Canny(template, 50, 200)

        # Match template
        result = cv2.matchTemplate(screenshot_edges, template_edges, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= confidence:
            print(f"✅ Match found ({image_path}) with confidence {max_val:.2f}")
            h, w = template.shape
            match_center = (region[0] + max_loc[0] + w // 2, region[1] + max_loc[1] + h // 2)
            pyautogui.moveTo(match_center, duration=0.2)
            return True

        time.sleep(check_interval)

    print(f"\033[91m❌ Failed to match {image_path} within {timeout} seconds.\033[0m")
    return False



    





def add_transaction_details(record):
    """Fill Order ID, Phone Number, and Amount into form."""
    print(f"Processing Record: {record}")

    pyautogui.moveTo(1768, 504, duration=.1)  # Add New Bank Transaction
    time.sleep(0.2)
    pyautogui.click()


    pyautogui.moveTo(524, 462, duration=.1)  # Order ID field
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(0.2)
    pyautogui.write(record["Order ID"], interval=0.05)

    pyautogui.moveTo(833, 592, duration=.1)  # Phone Number field
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(0.2)
    pyautogui.write(record["Phone Number"], interval=0.05)

    pyautogui.moveTo(528, 365, duration=.1)  # Amount field
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(0.2)
    pyautogui.write(record["Amount"], interval=0.05)

    pyautogui.moveTo(560, 294, duration=.1)  # Transaction time section
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(0.2)
    time.sleep(0.5)


    image_paths = [record.get("Image Path 1"), record.get("Image Path 2")]
    image_paths = [p for p in image_paths if p and os.path.exists(p)]  # Filter non-existent paths

    if image_paths:
        matched_path = find_and_hover_image_with_fallback(
            image_paths,
            region=(512, 370, 500, 500),  # Adjust if needed
            confidence=0.95,
            timeout=10,
            check_interval=0.2
        )
        if matched_path:
            pyautogui.click()
        else:
            print(f"❌ Date not found on screen for {record['Time']}")
    else:
        print("⚠️ No valid image paths provided — skipping date selection.")




    # Select Hour
    pyautogui.moveTo(564, 602, duration=0.1)
    pyautogui.click()
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(1)
    pyautogui.write(record["Hour"], interval=0.1)

    # Select Minute
    pyautogui.moveTo(682, 602, duration=0.1)
    pyautogui.click()
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    time.sleep(1)
    pyautogui.write(record["Minute"], interval=0.1)
    
    # Safety feature to ensure calendar receive the date
    pyautogui.moveTo(943, 618, duration=.1)  
    pyautogui.click()
    time.sleep(0.5)

    # Apply button
    pyautogui.moveTo(1340, 914, duration=.1)  
    pyautogui.click()
    time.sleep(3)

    check_x, check_y = 1103, 193  # <- Replace with your pixel coordinate
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



def parse_and_execute(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_gateway = None
    current_records = []
    performed_gateways = set()  # Track gateways already set up

    # Define the list of gateways your program can handle
    supported_gateways = {
        "XYPAY", "SKPAY", "YTPAY", "OSPAY", "SIMPLYPAY", "VADERPAY",
        "PASSPAY", "MULTIPAY", "U9PAY", "BOMBAYPAY", "EPAY", 
        "MOHAMMED AMEER ABBAS", "Test", "Test2"
    }

    for line in lines:
        line = line.strip()

        # Detect gateway header line
        if line.startswith("====") and "Total Amount" in line:
            # First, process any records collected under the previous gateway
            for record in current_records:
                add_transaction_details(record)
            current_records = []

            # Extract gateway name from the header line
            match = re.match(r"==== (.*?) \(", line)
            if match:
                detected_gateway = match.group(1)
                if detected_gateway in supported_gateways:
                    current_gateway = detected_gateway

                    # Run gateway setup if not already done
                    if current_gateway not in performed_gateways:
                        gateway_setup_movement(current_gateway)
                        performed_gateways.add(current_gateway)
                else:
                    print(f"\033[91m[Warning] Unsupported gateway '{detected_gateway}' found, skipping setup and records.\033[0m")
                    current_gateway = None  # Reset to ignore records for unsupported gateway


        elif current_gateway:  # Only parse transaction details if we have a valid gateway active

            if line.startswith("Order ID:"):
                order_id = line.split(":", 1)[1].strip()

            elif line.startswith("Phone Number:"):
                phone = line.split(":", 1)[1].strip()

            elif line.startswith("Amount:"):
                amount = line.split(":", 1)[1].strip()

            elif line.startswith("Time:"):
                time_str = line.split(":", 1)[1].strip()

                try:
                    dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                    day_str = str(dt.day)
                    hour_str = f"{dt.hour:02d}"
                    minute_str = f"{dt.minute:02d}"

                    # Store both paths
                    image_folder = os.path.join(os.getcwd(), "rocketgo_date_select")
                    image_path_1 = os.path.join(image_folder, f"{day_str}.png")
                    image_path_2 = os.path.join(image_folder, f"{day_str}(1).png")

                except ValueError:
                    print(f"\033[91m[Error] Invalid date format: '{time_str}'\033[0m")
                    day_str = None
                    image_path_1 = None
                    image_path_2 = None

                # Append the record with both image paths
                current_records.append({
                    "Order ID": order_id,
                    "Phone Number": phone,
                    "Amount": amount,
                    "Time": time_str,
                    "Image Path 1": image_path_1,
                    "Image Path 2": image_path_2,
                    "Hour": hour_str,
                    "Minute": minute_str
                })


    # Process any remaining records for the last gateway
    for record in current_records:
        add_transaction_details(record)

        # Check done applied
        check_x, check_y = 786, 188  # <- Replace with your pixel coordinate
        expected_rgb = (25, 33, 50)  # <- Replace with the RGB value to match
        timeout = 20                       # seconds
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



# ===== MAIN =====
if __name__ == "__main__":
    print("\033[92m[INFO] Starting automation and switching window...\033[0m")


# Switch 1 tab
pyautogui.keyDown('alt')
pyautogui.press('tab')
time.sleep(0.1)  
pyautogui.keyUp('alt')

print("Switched window!")

time.sleep(0.5)  
parse_and_execute("transaction_history.txt")

