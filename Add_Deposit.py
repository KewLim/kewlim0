import pyautogui
import time
import re

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
        "Test": "Test"
    }

    if gateway_name in gateway_map:
        enter_gateway_name(gateway_map[gateway_name])


def enter_gateway_name(gateway_text):
    pyautogui.moveTo(354, 239, duration=.1)
    pyautogui.click()
    time.sleep(0.2)
    pyautogui.keyDown('delete')
    time.sleep(3)
    pyautogui.keyUp('delete')
    time.sleep(0.2)
    pyautogui.write(gateway_text, interval=.1)
    time.sleep(0.2)
    pyautogui.press('enter')




def add_transaction_details(record):
    """Fill Order ID, Phone Number, and Amount into form."""
    print(f"Processing Record: {record}")

    pyautogui.moveTo(1768, 504, duration=.1)  # Add New Bank Transaction
    time.sleep(0.2)
    pyautogui.click()


    pyautogui.moveTo(524, 462, duration=.1)  # Order ID field
    pyautogui.click()
    pyautogui.write(record["Order ID"], interval=0.05)

    pyautogui.moveTo(833, 592, duration=.1)  # Phone Number field
    pyautogui.click()
    pyautogui.write(record["Phone Number"], interval=0.05)

    pyautogui.moveTo(528, 365, duration=.1)  # Amount field
    pyautogui.click()
    pyautogui.write(record["Amount"], interval=0.05)

    pyautogui.moveTo(1340, 914, duration=.1)  # Apply button
    pyautogui.click()
    time.sleep(0.5)



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
        "MOHAMMED AMEER ABBAS", "Test"
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

                # After Time line, append the record
                current_records.append({
                    "Order ID": order_id,
                    "Phone Number": phone,
                    "Amount": amount,
                    "Time": time_str
                })

    # Process any remaining records for the last gateway
    for record in current_records:
        add_transaction_details(record)



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

