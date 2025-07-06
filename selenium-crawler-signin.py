from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



options = Options()
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


time.sleep(5)
