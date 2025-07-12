import time
import re
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



def extract_phone_data_from_text(text):
    """Extracts phone records from formatted text input."""
    records = []

    # Pattern matches lines like: #1 - Phone: 916360881357, Email: -, Affiliate: APK006
    pattern = re.compile(r"#\d+\s+-\s+Phone:\s+(\d+),\s+Email:\s+([^,]+),\s+Affiliate:\s+(.+)")
    
    lines = text.strip().splitlines()
    for line in lines:
        match = pattern.match(line)
        if match:
            phone, email, affiliate = match.groups()
            records.append({
                "Phone Number": phone.strip(),
                "Email": email.strip(),
                "Affiliate Code": affiliate.strip()
            })
        else:
            print(f"⚠️ Skipping malformed line: {line}")
    
    return records




