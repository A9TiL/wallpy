import sys
import os
import tkinter as tk
from tkinter import filedialog
import subprocess
import warnings
from PIL import Image, ImageTk

warnings.filterwarnings("ignore")

from wallpaper_engine.utils.config_manager import load_config, save_config
from wallpaper_engine.controller import find_running_engine

def resource_path(relative_path):
    """Return correct path for dev and PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#ICON_PATH = os.path.join(BASE_DIR, "assets", "icons", "icon.png")

ICON_PATH = resource_path("wallpaper_engine/assets/icons/icon.png")



preview_images = []


# ---------------- ENGINE CONTROL ---------------- #

def start_engine_gui():
    subprocess.run(["python3", "-m", "wallpaper_engine.controller", "start"])
    update_engine_buttons()


def stop_engine_gui():
    subprocess.run(["python3", "-m", "wallpaper_engine.controller", "stop"])
    update_engine_buttons()


def update_engine_buttons():
    pid = find_running_engine()

    if pid:
        start_button.config(state="disabled")
        stop_button.config(state="normal")
    else:
        start_button.config(state="normal")
        stop_button.config(state="disabled")


def refresh_status():
    update_engine_buttons()
    root.after(2000, refresh_status)


# ---------------- SETTINGS ---------------- #

def choose_folder():
    folder = filedialog.askdirectory()

    if folder:
        config = load_config()
        config["folder"] = folder
        save_config(config)

        #automatic wallpaper preview loading 
        load_wallpaper_previews()


def set_interval():
    try:
        config = load_config()
        config["interval"] = int(interval_entry.get())
        save_config(config)
    except ValueError:
        pass


def change_mode():
    config = load_config()
    config["mode"] = mode_var.get()
    save_config(config)


# ---------------- WALLPAPER CONTROL ---------------- #

def set_wallpaper(image_path):

    uri = f"file://{image_path}"

    subprocess.run([
        "gsettings",
        "set",
        "org.gnome.desktop.background",
        "picture-uri",
        uri
    ])

    subprocess.run([
        "gsettings",
        "set",
        "org.gnome.desktop.background",
        "picture-uri-dark",
        uri
    ])


# ---------------- WALLPAPER PREVIEW ---------------- #

def load_wallpaper_previews():

    preview_images.clear()

    config = load_config()
    folder = config["folder"]

    if not os.path.exists(folder):
        print("Wallpaper folder not found:", folder)
        return

    for widget in preview_frame.winfo_children():
        widget.destroy()

    valid_ext = (".jpg", ".jpeg", ".png", ".webp")

    image_index = 0

    for file in sorted(os.listdir(folder)):

        if not file.lower().endswith(valid_ext):
            continue

        path = os.path.join(folder, file)

        try:
            img = Image.open(path)
            img.thumbnail((120, 80))

            photo = ImageTk.PhotoImage(img)
            preview_images.append(photo)

            btn = tk.Button(
                preview_frame,
                image=photo,
                command=lambda p=path: set_wallpaper(p)
            )

            row = image_index // 4
            col = image_index % 4

            btn.grid(row=row, column=col, padx=5, pady=5)

            image_index += 1

        except Exception as e:
            print("Preview load error:", e)



# ---------------- GUI ---------------- #

root = tk.Tk()

icon = tk.PhotoImage(file=ICON_PATH)
root.iconphoto(False, icon)

root.title("Wallpy")
root.geometry("562x930")


title = tk.Label(root, text="Wallpy", font=("Arial", 16))
title.pack(pady=10)


# ENGINE BUTTONS
start_button = tk.Button(root, text="Start Engine", command=start_engine_gui)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Engine", command=stop_engine_gui)
stop_button.pack(pady=5)


# FOLDER SELECTOR
folder_button = tk.Button(root, text="Select Wallpaper Folder", command=choose_folder)
folder_button.pack(pady=10)


# INTERVAL SETTING
interval_label = tk.Label(root, text="Interval (seconds)")
interval_label.pack()

interval_entry = tk.Entry(root)
interval_entry.pack()

interval_button = tk.Button(root, text="Set Interval", command=set_interval)
interval_button.pack(pady=5)


# MODE TOGGLE
mode_label = tk.Label(root, text="Wallpaper Mode")
mode_label.pack(pady=5)

mode_var = tk.StringVar()

config = load_config()
mode_var.set(config["mode"])

random_radio = tk.Radiobutton(
    root,
    text="Random",
    variable=mode_var,
    value="random",
    command=change_mode
)

sequential_radio = tk.Radiobutton(
    root,
    text="Sequential",
    variable=mode_var,
    value="sequential",
    command=change_mode
)

random_radio.pack()
sequential_radio.pack()


# ---------------- PREVIEW GALLERY ---------------- #

preview_label = tk.Label(root, text="Wallpaper Preview")
preview_label.pack(pady=10)

preview_container = tk.Frame(root)
preview_container.pack(fill="both", expand=True)

preview_canvas = tk.Canvas(preview_container)
preview_canvas.pack(side="left", fill="both", expand=True)

scrollbar_y = tk.Scrollbar(preview_container, orient="vertical", command=preview_canvas.yview)
scrollbar_y.pack(side="right", fill="y")

scrollbar_x = tk.Scrollbar(root, orient="horizontal", command=preview_canvas.xview)
scrollbar_x.pack(fill="x")

preview_canvas.configure(
    yscrollcommand=scrollbar_y.set,
    xscrollcommand=scrollbar_x.set
)

preview_frame = tk.Frame(preview_canvas)

preview_canvas.create_window((0, 0), window=preview_frame, anchor="nw")


def update_scroll_region(event=None):
    preview_canvas.configure(scrollregion=preview_canvas.bbox("all"))

preview_frame.bind("<Configure>", update_scroll_region)


def on_mousewheel(event):
    preview_canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")


def on_shift_mousewheel(event):
    preview_canvas.xview_scroll(-1 if event.delta > 0 else 1, "units")


preview_canvas.bind_all("<MouseWheel>", on_mousewheel)
preview_canvas.bind_all("<Shift-MouseWheel>", on_shift_mousewheel)


reload_button = tk.Button(root, text="Refresh Wallpapers", command=load_wallpaper_previews)
reload_button.pack(pady=5)


# INITIAL ENGINE STATUS
update_engine_buttons()
refresh_status()
load_wallpaper_previews()

root.mainloop()
