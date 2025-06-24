import requests
import json
import keyboard
import tkinter as tk
import threading
import os
import pickle
import base64
import hashlib

# Check for updates
def download_latest_version(save_path, repo_owner, repo_name, file_path, branch="main"):
    script_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{file_path}"
    try:
        response = requests.get(script_url, timeout=10)
        response.raise_for_status()
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print("Successfully updated to the latest version.")
    except requests.RequestException as e:
        print(f"Error downloading the latest version: {e}")

def generate_sha256_checksum_github(repo_owner, repo_name, file_path, branch="main"):
    url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{file_path}"
    response = requests.get(url, stream=True)
    response.raise_for_status()

    sha256_hash = hashlib.sha256()
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def generate_sha256_checksum_file(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

print("Checking for online updates.")
if generate_sha256_checksum_github("LunaZaps", "Ctrl-Z-ap", "main.py") != generate_sha256_checksum_file(os.path.abspath(__file__)):
    print("A newer version is available! Updating...")
    download_latest_version(os.path.abspath(__file__), "LunaZaps", "Ctrl-Z-ap", "main.py")
    input("Done. Please restart the script by pressing enter and reopening again.")
    quit()
else:
    print("You are using the latest version.")

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

def encode_file(path):
    with open(path, "rb") as f:
        encoded_data = base64.b64encode(f.read())
    with open(path, "wb") as f:
        f.write(encoded_data)

def decode_file(path):
    with open(path, "rb") as f:
        decoded_data = base64.b64decode(f.read())
    with open(path, "wb") as f:
        f.write(decoded_data)

def main():
    global USERNAME, API_KEY, SHOCK_DURATION, SHOCK_INTENSITY
    if not os.path.exists('./TOKEN'):
        # PiShock API credentials
        USERNAME = input("Your Pishock username: ")
        API_KEY = input("Your API key (you can find that at https://pishock.com/#/account): ")
        dmp = {"usr": USERNAME, "api": API_KEY}
        pickle.dump(dmp, open( "TOKEN", "wb" ) )
        encode_file('TOKEN')
    else:
        decode_file("TOKEN")
        dmp = pickle.load( open( "TOKEN", "rb" ) )
        encode_file("TOKEN")
        USERNAME = dmp["usr"]
        API_KEY = dmp["api"]
    global DEVICE_CODES
    DEVICE_CODES = []
    codea = input("Shocker share codes (Each on diffrent line. If you are done, just leave this blank): ")
    while True:
        DEVICE_CODES.append(codea)
        codea = input("Shocker share codes (Each on diffrent line. If you are done, just leave this blank): ")
        if codea is None or codea == "":
            break
    # Shock settings
    SHOCK_INTENSITY = int(input("Shock intensity (in percent): "))
    SHOCK_DURATION = int(input("Shock duration (in seconds): "))
    print("Press 'Ctrl+Z' to send shocks to all devices.")
    gui_thread = threading.Thread(target=setup_gui)
    gui_thread.daemon = True
    gui_thread.start()
    while True:
        if keyboard.is_pressed('ctrl+z'):
            send_shock()

main()
