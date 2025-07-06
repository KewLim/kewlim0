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


# Entered 2.1 Deposit 

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
