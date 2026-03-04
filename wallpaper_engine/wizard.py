import json
import os
import subprocess

CONFIG_FILE = "config.json"


def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


def start_engine():
    subprocess.run(["python3", "controller.py", "start"])


def stop_engine():
    subprocess.run(["python3", "controller.py", "stop"])


def status_engine():
    subprocess.run(["python3", "controller.py", "status"])


def change_folder():
    config = load_config()

    new_folder = input("Enter wallpaper folder path: ")

    if os.path.exists(new_folder):
        config["folder"] = new_folder
        save_config(config)
        print("Folder updated.")
    else:
        print("Folder does not exist.")


def change_interval():
    config = load_config()

    new_interval = input("Enter interval in seconds: ")

    try:
        config["interval"] = int(new_interval)
        save_config(config)
        print("Interval updated.")
    except ValueError:
        print("Invalid number.")


def toggle_mode():
    config = load_config()

    if config["mode"] == "random":
        config["mode"] = "sequential"
    else:
        config["mode"] = "random"

    save_config(config)
    print("Mode changed to:", config["mode"])


def menu():

    while True:

        print("\nWallpaper Engine Control Panel\n")

        print("1 Start Engine")
        print("2 Stop Engine")
        print("3 Engine Status")
        print("4 Change Wallpaper Folder")
        print("5 Change Interval")
        print("6 Toggle Random/Sequential Mode")
        print("7 Exit")

        choice = input("\nSelect option: ")

        if choice == "1":
            start_engine()

        elif choice == "2":
            stop_engine()

        elif choice == "3":
            status_engine()

        elif choice == "4":
            change_folder()

        elif choice == "5":
            change_interval()

        elif choice == "6":
            toggle_mode()

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    menu()
