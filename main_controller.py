from RocketGO_add_deposit import find_and_hover_image_in_region
import time
import os
import pyautogui

# Define your task list
tasks = [
    {"type": "text", "copy": (230, 818), "paste": (562, 450)}, # Order ID
    {"type": "text", "copy": (656, 818), "paste": (858, 582)}, # Phone Number
    {
        "type": "date",
        "copy": (1644,824),
        "region": (512, 370, 275, 210) # Date String
    },
    {"type": "text", "copy": (955, 816), "paste": (543, 372)}, # Amount
]

def switch_window_to_website2():
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')
    time.sleep(0.5)  # Give time for window to switch

def main():
    for i, task in enumerate(tasks):
        print(f"\n=== Task {i+1}: {task['type'].upper()} ===")

        # --- Website 1 ---
        data = copy_from_coords(*task["copy"])
        print(f"Copied data: {data}")

        # --- Switch to Website 2 ---
        switch_window_to_website2()

        # --- Paste or select date ---
        if task["type"] == "text":
            paste_to_coords(*task["paste"], data)
            print("Pasted.")

        elif task["type"] == "date":
            try:
                day = data.split(" ")[0].split("-")[2]  # Extract day from full timestamp
                image_path = f"rocketgo_date_select/{day}.png"

                if not os.path.exists(image_path):
                    print(f"Date image not found: {image_path}")
                    continue

                find_and_hover_image_in_region(image_path, task["region"], confidence=0.95)

            except Exception as e:
                print(f"Error handling date: {e}")
                continue

        time.sleep(0.5)


