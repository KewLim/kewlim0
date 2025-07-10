import pyautogui
import time


# python mouse.py
# python mouse2.py
# python RocketGO_add_deposit.py
# python Action_FIND.py
# python main.py 
# python test_2.py
# python main_controller.py
# python new_inspect.py
# python Get_phonenumber.py
# python Add_Player.py
# python Add_Deposit.py


# 'Add New Player' button = pyautogui.moveTo(1796, 231, duration=.1)
# 'Phone Number 01' button = pyautogui.moveTo(987, 271, duration=.1)
# 'Phone Number 02' button = pyautogui.moveTo(987, 360, duration=.1)
# 'Apply' button = pyautogui.moveTo(1224, 928, duration=.1)

# ====  | Deposit Panel UI Coordinates |  ====

# PG Search Bar = pyautogui.moveTo(1224, 928, duration=.1)
# Add 'Bank Transaction' button = pyautogui.moveTo(1224, 928, duration=.1)
# 'Amount' = pyautogui.moveTo(528, 365, duration=.1)
# 'Bank Reference' = pyautogui.moveTo(524, 462, duration=.1)
# 'Player ID' = pyautogui.moveTo(833, 592, duration=.1)
# 'Calendar' = pyautogui.moveTo(553, 280, duration=.1)
# 'Apply' button = pyautogui.moveTo(1340, 914, duration=.1)



#1. Get screen size in pixels

#screen_width, screen_height = pyautogui.size()
#print(f"Screen size: {screen_width}x{screen_height}")

#2. Scroll (custom units: positive = up, negative = down)

#pyautogui.scroll(-300)  # Scroll down
#pyautogui.scroll(500)   # Scroll up

# 3. Move mouse to (x, y)
#pyautogui.moveTo(400, 300, duration=1)  # Move to (400,300) over 1 second



#4. Double-click at current or specific location
#pyautogui.click() 
#pyautogui.doubleClick()
#pyautogui.tripleClick()   # At current mouse location
# OR
#pyautogui.press('enter')


#5. Copy (Ctrl + C)

#pyautogui.hotkey('ctrl', 'c')  # Simulates Ctrl+C

#6. Paste (Ctrl + V)

#pyautogui.hotkey('ctrl', 'v')  # Simulates Ctrl+V

# 7. Switch tab (e.g., browser/app tab — Ctrl + Tab or Alt + Tab)

#pyautogui.keyDown('alt')
#pyautogui.press('tab')
#pyautogui.keyUp('alt')

