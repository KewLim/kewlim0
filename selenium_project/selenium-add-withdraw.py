from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from selenium.webdriver.support.ui import Select
from datetime import datetime
from collections import defaultdict
import re
from selenium.webdriver import ActionChains
import pyautogui





profile_path = "/Users/admin/Library/Application Support/Firefox/Profiles/7oz304au.default-release"
firefox_profile = webdriver.FirefoxProfile(profile_path)

options = Options()
options.set_preference("profile", profile_path)
# Optional: Use a separate Firefox profile
# Replace 'selenium-profile' with the name of a Firefox profile you’ve created
# or comment out if you want a fresh profile every time
# options.profile = "/Users/admin/Library/Application Support/Firefox/Profiles/xxxxxxxx.selenium-profile"

# Headless mode if needed
# options.add_argument('--headless')

# Setup the driver
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)
driver.maximize_window()



driver.get("https://www.rocketgo.asia/login")

wait = WebDriverWait(driver, 40)
merchant_input = wait.until(EC.presence_of_element_located((By.NAME, "merchant_code")))
merchant_input.send_keys("luckytaj")

wait = WebDriverWait(driver, 40)
username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
username_input.send_keys("Admin_Json")

wait = WebDriverWait(driver, 40)
password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
password_input.send_keys("json8888"+ Keys.ENTER)



def remove_bom(line):
    BOM = '\ufeff'
    if line.startswith(BOM):
        return line.lstrip(BOM)
    return line



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
    # Step 1: Wait for preloader to disappear
    WebDriverWait(driver, 30).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "app-preloader"))
    )
    time.sleep(2)  # slight delay for DOM settle

    # Step 2: Click container to open dropdown
    container = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ts-control"))
    )
    container.click()
    time.sleep(0.5)

    # Step 3: Find actual input (not always interactable)
    gateway_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "selectBank-ts-control"))
    )

    # Optional: Scroll it into view
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", gateway_input)
    time.sleep(0.3)

    print("Displayed:", gateway_input.is_displayed())
    print("Enabled:", gateway_input.is_enabled())
    print("Size:", gateway_input.size)
    print("Location:", gateway_input.location)

    try:
        # Try normal input method first
        gateway_input.send_keys(gateway_text)
    except Exception as e:
        print(f"[WARN] Normal input failed, using JS. Reason: {e}")
        # Fallback to JS-based input
        driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        """, gateway_input, gateway_text)

    time.sleep(0.5)  # Wait for dropdown options

    # Step 4: Press Enter to select the first matching option
    gateway_input.send_keys(Keys.ENTER)
    print(f"[INFO] Gateway '{gateway_text}' entered and selected.")
    time.sleep(0.5)





    # --- Check Table load ---
    wait = WebDriverWait(driver, 30)
    table_presence = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gridjs-wrapper")))
    print("[INFO] Table loaded")

    time.sleep(1)


# ======== Add Details HERE =======


def add_transaction_details(record):

    """Fill Order ID, Phone Number, and Amount into form."""
    print(f"Processing Record: {record}")

    time.sleep(2)
    wait = WebDriverWait(driver, 20)  # Add this line
    add_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(text(), 'Add New Bank Transaction')]"
    )))
    add_button.click()
    print("[INFO] Add Transaction button clicked")

    time.sleep(1)


    # ===== Transaction Out =====

    out_radio = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="radio"][value="out"]'))
    )
    out_radio.click()
    print("[INFO] Clicked on the 'out' radio button.")
    time.sleep(.5)



    # ===== Order ID =====

    order_id_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Bank Reference']"))
    )
    order_id_input.clear()
    order_id_input.send_keys(record["Order ID"])
    print(f"[INFO] Order ID entered: {record['Order ID']}")



    # ===== Phone Number =====

    phone_number_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Player ID']"))
    )
    phone_number_input.clear()
    phone_number_input.send_keys(record["Phone Number"])
    print(f"[INFO] Order ID entered: {record['Phone Number']}")



    # ===== Amount =====

    amount_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='amount']"))
    )
    amount_input.clear()
    amount_input.send_keys(str(record["Amount"]).replace(",", ""))
    print(f"[INFO] Order ID entered: {record['Amount']}")


    # ===== Datepicker =====

    calendar_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Choose datetime...']"))
    )
    calendar_input.click()
    print(f"[INFO] Calendar input clicked...")

    calendar_popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "flatpickr-calendar"))
    )

    if "open" in calendar_popup.get_attribute("class"):
        print("[INFO] Calendar popup is OPEN")

        target_date = record["Datetime"].strftime("%B %-d, %Y")  # e.g. "July 6, 2025"
        all_days = driver.find_elements(By.CSS_SELECTOR, ".flatpickr-day")

        for day in all_days:
            if day.get_attribute("aria-label") == target_date:
                driver.execute_script("arguments[0].scrollIntoView(true);", day)
                day.click()
                print(f"[INFO] Clicked date: {target_date}")
                break
        else:
            print(f"[ERROR] Date '{target_date}' not found in picker.")

    else:
        print("[WARN] Calendar popup did NOT open")


    # ===== Hour =====
    wait = WebDriverWait(driver, 40)
    merchant_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.flatpickr-hour")))
    merchant_input.send_keys(record["Hour"])


    # ===== Minutes =====
    wait = WebDriverWait(driver, 40)
    merchant_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.flatpickr-minute")))
    merchant_input.send_keys(record["Minute"])




    # ===== Decide AM or PM from the record =====

    ampm_target = "AM" if int(record.get("Hour", 0)) < 12 else "PM"
    ampm_toggle = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "flatpickr-am-pm"))
    )

    # Check and click if needed
    current_ampm = ampm_toggle.text.strip().upper()
    if current_ampm != ampm_target:
        ampm_toggle.click()
        print(f"[INFO] AM/PM toggled to {ampm_target}")
    else:
        print(f"[INFO] AM/PM already set to {ampm_target}")

    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(.5)
    pyautogui.press('enter')
    time.sleep(.5)










def parse_and_execute(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_gateway = None
    current_records = []
    performed_gateways = set()

    supported_gateways = {
        "XYPAY", "SKPAY", "YTPAY", "OSPAY", "SIMPLYPAY", "VADERPAY",
        "PASSPAY", "MULTIPAY", "U9PAY", "BOMBAYPAY", "EPAY", 
        "MOHAMMED AMEER ABBAS", "Test", "Test2"
    }

    # Temporary variables for one record
    order_id = phone = amount = time_str = None
    dt = hour_str = minute_str = None

    for raw_line in lines:
        line = remove_bom(raw_line.strip())

        if not line:
            continue

        # Stop condition — flush records first
        if line.startswith("==== GRAND TOTAL for All Gateways:"):
            print("[INFO] Reached GRAND TOTAL line. Stopping processing.")
            break

        # Detect gateway header line
        if line.startswith("====") and "Total Amount" in line:
            if current_records:
                print(f"[DEBUG] Flushing {len(current_records)} records under gateway '{current_gateway}'")
                for record in current_records:
                    add_transaction_details(record)
            current_records = []

            match = re.match(r"==== (.*?) \(", line)
            if match:
                detected_gateway = match.group(1)
                if detected_gateway in supported_gateways:
                    current_gateway = detected_gateway
                    if current_gateway not in performed_gateways:
                        gateway_setup_movement(current_gateway)
                        performed_gateways.add(current_gateway)
                else:
                    print(f"[WARNING] Unsupported gateway '{detected_gateway}', skipping records.")
                    current_gateway = None
            continue

        # Skip if gateway not set
        if not current_gateway:
            continue

        # Parse record fields
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
                hour_str = f"{dt.hour:02d}"
                minute_str = f"{dt.minute:02d}"

                # ✅ Only append once all fields are known
                if all([order_id, phone, amount, time_str]):
                    current_records.append({
                        "Order ID": order_id,
                        "Phone Number": phone,
                        "Amount": amount,
                        "Time": time_str,
                        "Hour": hour_str,
                        "Minute": minute_str,
                        "Datetime": dt
                    })
                    # Reset vars for next record
                    order_id = phone = amount = time_str = None
                    dt = hour_str = minute_str = None
            except ValueError:
                print(f"[ERROR] Invalid datetime: {time_str}")
                continue

    # ✅ Final flush at EOF
    if current_records:
        print(f"[DEBUG] Final flush: {len(current_records)} records under gateway '{current_gateway}'")
        for record in current_records:
            add_transaction_details(record)



# ===== Function call HERE =====
parse_and_execute("selenium_project/wd-selenium-transaction_history.txt")
time.sleep(2)  
driver.quit()

