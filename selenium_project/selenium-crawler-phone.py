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



driver.get("https://bo.backofficeltaj.com/")

wait = WebDriverWait(driver, 40)
merchant_input = wait.until(EC.presence_of_element_located((By.ID, "mer_code")))
merchant_input.send_keys("lucky")

wait = WebDriverWait(driver, 40)
username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
username_input.send_keys("test_8899")

wait = WebDriverWait(driver, 40)
password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
password_input.send_keys("Mcd6033035!")





def get_captcha_number(driver, timeout=40):
    # Wait for the outer span with all digits to appear
    wait = WebDriverWait(driver, timeout)
    outer_span = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "captchaNum")))
    
    # Now safely collect child <span> elements
    digits = outer_span.find_elements(By.TAG_NAME, "span")
    
    return ''.join([d.text for d in digits])




# Wait for CAPTCHA input field to appear

wait = WebDriverWait(driver, 40)
captcha_input = wait.until(EC.presence_of_element_located((By.ID, "captcha")))
captcha_code = get_captcha_number(driver)
captcha_input.send_keys(captcha_code)

print("\033[92mExtracted CAPTCHA:", captcha_code, "\033[0m")
captcha_input.send_keys(captcha_code + Keys.ENTER)

# ======== Entered Main Page ========

# Wait for sidebar to appear

wait = WebDriverWait(driver, 40)
menu_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.treeview.a-1 > a')))


WebDriverWait(driver, 20).until(
    EC.invisibility_of_element_located((By.CLASS_NAME, "ajaxLoader"))
)
print("\033[94m[INFO] ajaxLoader complete\033[0m")
time.sleep(2)


menu_link.click()

# Step 2: Wait for submenu item to be visible and clickable
submenu_item = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.as.done > a[href="member-info"]')))
submenu_item.click()



# ======== Entered 2.1 Deposit =======


# Wait for panel loading
WebDriverWait(driver, 20).until(
    EC.invisibility_of_element_located((By.CLASS_NAME, "box box-info"))
)
print("[INFO] Panel load complete")


time.sleep(2)

# Wait for ajax loader loading
WebDriverWait(driver, 20).until(
    EC.invisibility_of_element_located((By.CLASS_NAME, "ajaxLoader"))
)
print("\033[94m[INFO] ajaxLoader complete\033[0m")

time.sleep(2)


# Manual date selection pause
print("⏸️ Paused for manual date selection.")
input("👉 Please select the date manually in the browser, then press ENTER here to continue...")
print("✅ Date selected, continuing...")

# Wait for 'No Record' Icon dissapeared

WebDriverWait(driver, 20).until(
    EC.invisibility_of_element_located((By.CLASS_NAME, "box box-info no-record-holder"))
)
print("\033[94m[INFO] Table load complete\033[0m")


# ======= Print Logic Here =======

phone_groups = defaultdict(list)


def extract_phone_data(driver, wait_timeout=20):
    """Waits for transaction table rows to appear and extracts phone/email/affiliate data."""

    WebDriverWait(driver, wait_timeout).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "table.tableInfo tbody tr")) > 0
    )
    print("[INFO] Table load complete")

    # ⛔ DON'T STORE OLD references
    rows = driver.find_elements(By.CSS_SELECTOR, "table.tableInfo tbody tr")
    print(f"[INFO] Total rows found: {len(rows)}")

    grouped = defaultdict(list)
    seen_numbers = set()

    for idx in range(len(rows)):
        try:
            # ✅ Re-fetch row to avoid stale reference
            rows = driver.find_elements(By.CSS_SELECTOR, "table.tableInfo tbody tr")
            row = rows[idx]
            cols = row.find_elements(By.TAG_NAME, 'td')

            if len(cols) < 19:
                print(f"[WARNING] Row {idx+1} has only {len(cols)} columns. Skipping.")
                continue

            phone_number = cols[16].text.strip()
            email = cols[18].text.strip()
            affiliate_code = cols[6].text.strip()

            if phone_number and phone_number not in seen_numbers:
                record = {
                    "Phone Number": phone_number,
                    "Email": email,
                    "Affiliate Code": affiliate_code
                }
                grouped["All"].append(record)
                seen_numbers.add(phone_number)

        except Exception as e:
            print(f"[ERROR] Failed processing row {idx+1}: {e}")
            continue

    return grouped



def print_grouped_phone_results(grouped_data):
    total_records = sum(len(records) for records in grouped_data.values())
    print(f"\n[INFO] Writing {total_records} total records to file.")

    with open("selenium_project/selenium-phone-number.txt", "w", encoding="utf-8") as f:
        for group, records in grouped_data.items():
            header = f"\n==== {group} ({len(records)} records) ====\n"
            print(f"\033[92m{header}\033[0m")
            f.write(header)

            for i, record in enumerate(records, 1):
                line = (
                    f"#{i} - Phone: {record['Phone Number']}, "
                    f"Email: {record['Email']}, Affiliate: {record['Affiliate Code']}\n"
                )
                print(line.strip())
                f.write(line)

        footer = f"\n==== TOTAL: {total_records} phone numbers collected ====\n"
        print(f"\033[95m{footer}\033[0m")
        f.write(footer)


def click_next_page(driver, wait_timeout=10):
    try:
        next_button = WebDriverWait(driver, wait_timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.page-link.next"))
        )
        next_button.click()
        time.sleep(1)
        print("[INFO] Clicked on the Next button.")
        return True
    except Exception as e:
        print(f"[WARNING] Could not click Next button: {e}")
        return False


def run_full_phone_extraction(driver):
    global phone_groups
    phone_groups = defaultdict(list)

    page_counter = 1
    while True:
        print(f"\033[92m[INFO] Scraping page {page_counter}...\033[0m")

        current_page_data = extract_phone_data(driver)

        for group, records in current_page_data.items():
            phone_groups[group].extend(records)

        has_next = click_next_page(driver)
        if not has_next:
            print("[INFO] No more pages found. Finishing extraction.")
            break

        page_counter += 1
        time.sleep(1)

    print_grouped_phone_results(phone_groups)

run_full_phone_extraction(driver)



time.sleep(5)  
driver.quit()