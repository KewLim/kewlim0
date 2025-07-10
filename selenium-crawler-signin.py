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
menu_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.treeview.a-2 > a')))


WebDriverWait(driver, 20).until(
    EC.invisibility_of_element_located((By.CLASS_NAME, "ajaxLoader"))
)
print("\033[94m[INFO] ajaxLoader complete\033[0m")
time.sleep(2)


menu_link.click()

# Step 2: Wait for submenu item to be visible and clickable
submenu_item = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.as.done > a[href="deposit"]')))
submenu_item.click()



# ======== Entered 2.1 Deposit =======


# Wait for panel loading
WebDriverWait(driver, 20).until(
    EC.invisibility_of_element_located((By.CLASS_NAME, "box box-info"))
)
print("[INFO] Panel load complete")


time.sleep(3)

# Wait for ajax loader loading
WebDriverWait(driver, 20).until(
    EC.invisibility_of_element_located((By.CLASS_NAME, "ajaxLoader"))
)
print("\033[94m[INFO] ajaxLoader complete\033[0m")

time.sleep(3)

# Wait for the <select> element to be present
status_select_element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "status"))
)

select = Select(status_select_element)
select.select_by_visible_text("Approved")

# Select date section

select_date = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-type="today"]')))
select_date.click()

# Wait for 'No Record' Icon dissapeared

WebDriverWait(driver, 20).until(
    EC.invisibility_of_element_located((By.CLASS_NAME, "box box-info no-record-holder"))
)
print("\033[94m[INFO] Table load complete\033[0m")


# ======= Print Logic Here =======

# Wait for table to be visible (adjust selector if needed)
# Wait until at least one row is present inside the table
WebDriverWait(driver, 20).until(
    lambda d: len(d.find_elements(By.CSS_SELECTOR, "table.tableInfo tbody tr")) > 0
)

rows = driver.find_elements(By.CSS_SELECTOR, "table.tableInfo tbody tr")
print(f"[INFO] Total rows found: {len(rows)}")


gateway_groups = defaultdict(list)

rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')


for idx, row in enumerate(rows, 1):
    cols = row.find_elements(By.TAG_NAME, 'td')
    if len(cols) < 22:
        print(f"[WARNING] Row {idx} has only {len(cols)} columns. Skipping.")
        continue  # Skip rows that don't have enough columns

    record = {
        "Gateway": cols[21].text.strip(),
        "Order ID": cols[0].text.strip(),
        "Phone Number": cols[6].text.strip(),
        "Amount": float(cols[10].text.strip().replace("Rs", "").replace(",", "").strip()),
        "Time": cols[20].text.strip()
    }
    gateway_groups[record["Gateway"]].append(record)



def print_grouped_results():
    """Prints all grouped data and writes it to 'selenium-transaction_history.txt'."""
    grand_total = 0

    with open("selenium-transaction_history.txt", "w", encoding="utf-8") as f:
        for gateway, records in gateway_groups.items():
            
            total_amount = sum(record["Amount"] if isinstance(record["Amount"], (int, float)) else float(record["Amount"].replace(",", "")) for record in records)
            grand_total += total_amount

            header = f"\n==== {gateway} ({len(records)} record{'s' if len(records) != 1 else ''}) | Total Amount: Rs {total_amount:,.2f} ====\n"
            print(f"\033[92m{header}\033[0m")
            f.write(header)

            # Sort records by time (latest first)
            sorted_records = sorted(
                records,
                key=lambda r: datetime.strptime(r["Time"], "%Y-%m-%d %H:%M:%S"),
                reverse=True
            )

            for i, record in enumerate(sorted_records, 1):
                # print(f"[DEBUG] Record {i} in {gateway}: {record}")  # ✅ Keep for debugging

                entry = (
                    f"\nRecord #{i}\n"
                    f"Order ID: {record['Order ID']}\n"
                    f"Phone Number: {record['Phone Number']}\n"
                    f"Amount: {record['Amount']:,.2f}\n"
                    f"Time: {record['Time']}\n"
                )
                print(f"\033[94m{entry}\033[0m")
                f.write(entry)

            footer = f"\n>> Total Amount for {gateway}: Rs {total_amount:,.2f}\n"
            print(f"\033[93m{footer}\033[0m")
            f.write(footer)

        total_records = sum(len(records) for records in gateway_groups.values())

        # ✅ Only once at the end
        grand_footer = f"\n==== GRAND TOTAL for All Gateways: Rs {grand_total:,.2f} | Total Records: {total_records} ====\n"
        print(f"\033[95m{grand_footer}\033[0m")
        f.write(grand_footer)


print_grouped_results()

time.sleep(5)  
driver.quit()