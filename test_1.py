import pyautogui
import time
from datetime import datetime, timedelta
import pytz

print("Switching window in 3 seconds...")
time.sleep(3)

# Simulate Alt+Tab
pyautogui.keyDown('alt')
pyautogui.press('tab')
time.sleep(0.5)  
pyautogui.keyUp('alt')

print("Switched window!")

time.sleep(.1)
india_tz = pytz.timezone('Asia/Kolkata')
now = datetime.now(india_tz)

yesterday = now - timedelta(days=1)
formatted_date = yesterday.strftime("%d/%m/%Y")

message = f"Kiosk Transaction Report Withdrawal {formatted_date}"

time.sleep(3)

pyautogui.write(message, interval=0.1)
pyautogui.press('enter')
