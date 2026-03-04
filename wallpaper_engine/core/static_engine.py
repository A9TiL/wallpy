import os
import time
import json
import subprocess
import random
from wallpaper_engine.utils.config_manager import load_config


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.json")

def get_images(folder):
	valid_ext = (".jpg",".jpeg",".png",".webp")
	return [
		os.path.join(folder,f)
		for f in os.listdir(folder)
		if f.lower().endswith(valid_ext)
	]
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

def run():
	config = load_config()
	folder = config["folder"]
	interval = config["interval"]
	mode = config["mode"]

	images = get_images(folder)

	if not images:
		print("NO IMAGES FOUND.")
		return
	while True:
		if mode == "random":
			image = random.choice(images)
			set_wallpaper(image)
			time.sleep(interval)
		else:
			for image in images:
				set_wallpaper(image)
				time.sleep(interval)

if __name__ == "__main__":
	run()
		
