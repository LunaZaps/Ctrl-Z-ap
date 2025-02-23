import requests
import json
import keyboard
import tkinter as tk
import threading
import os

# PiShock API credentials
USERNAME = "your_username"  # Replace "your_username"
API_KEY = os.getenv("API_KEY")  # Loaded from environment variable

# List of device codes
DEVICE_CODES = ["your_code_1", "your_code_2"]

# Shock settings
SHOCK_INTENSITY = 50
SHOCK_DURATION = 1

# Initialize shock counter
shock_count = 0

# Function to send shock to all devices
def send_shock():
    global shock_count
    print("Sending shock to all devices")

    url = "https://do.pishock.com/api/apioperate/"

    for code in DEVICE_CODES:
        payload = {
            "Username": USERNAME,
            "Name": "Ctrl+Z Shock Script",
            "Code": code,
            "Intensity": SHOCK_INTENSITY,
            "Duration": SHOCK_DURATION,
            "Apikey": API_KEY,
            "Op": 0
        }

        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            print(f"Device with Code {code} Status Code: {response.status_code}")
            print(f"Device with Code {code} Response: {response.text}")

            if response.status_code == 200:
                print(f"Shock sent to device with Code {code} successfully.")
                shock_count += 1
                update_counter()
            else:
                print(f"Error sending shock to device with Code {code}: {response.status_code}")

        except Exception as e:
            print(f"Error occurred while sending shock to device with Code {code}: {e}")

# Function to update shock counter on GUI
def update_counter():
    counter_label.config(text=f"Zap Counter: {shock_count}")

# GUI setup for shock counter
def setup_gui():
    global counter_label

    root = tk.Tk()
    root.title("Zap Counter")
    root.attributes("-topmost", True)
    root.geometry("200x50+0+0")
    root.configure(bg="black")
    root.overrideredirect(True)  # Removes window borders

    # Counter label
    counter_label = tk.Label(root, text=f"Zap Counter: {shock_count}", fg="white", bg="black", font=("Arial", 12))
    counter_label.pack(padx=10, pady=10)

    # Make the window draggable
    def start_move(event):
        root.x = event.x
        root.y = event.y

    def do_move(event):
        deltax = event.x - root.x
        deltay = event.y - root.y
        x = root.winfo_x() + deltax
        y = root.winfo_y() + deltay
        root.geometry(f"+{x}+{y}")

    root.bind("<Button-1>", start_move)
    root.bind("<B1-Motion>", do_move)

    # Run the GUI
    root.mainloop()

# Main function to listen for Ctrl+Z
def main():
    print("Press 'Ctrl+Z' to send shocks to all devices.")

    # Start GUI in a separate thread
    gui_thread = threading.Thread(target=setup_gui)
    gui_thread.daemon = True
    gui_thread.start()

    while True:
        if keyboard.is_pressed('ctrl+z'):
            send_shock()

# Correct usage of if __name__ == "__main__":
if __name__ == "__main__":
    main()
