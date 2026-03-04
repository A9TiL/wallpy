# Wallpy

Wallpy is a lightweight open-source wallpaper manager for Linux.

It allows users to automatically rotate wallpapers, preview images, and manage wallpaper behavior through a simple graphical interface.

## Features

• Wallpaper slideshow  
• Random or sequential wallpaper mode  
• Preview gallery with scrolling  
• Built-in default wallpapers  
• Engine start / stop control  
• Lightweight Tkinter GUI  

## Screenshots



## Installation

Clone the repository:

git clone https://github.com/A9TiL/wallpy.git

Enter the project folder:

cd wallpy

Install dependencies:

pip install -r requirements.txt

Run the application:

python3 -m wallpaper_engine.app


## Configuration

User configuration is stored in:

~/.config/wallpy/config.json


## Project Structure

wallpy/
 ├── wallpaper_engine/
 │   ├── app.py
 │   ├── controller.py
 │   ├── core/
 │   ├── utils/
 │   └── assets/
 ├── desktop/
 ├── scripts/
 └── requirements.txt


## Roadmap

Planned future features:

• Video wallpapers  
• Multi-monitor support  
• Wayland / Hyprland backend  
• AppImage distribution  
• System tray integration  


## License

MIT License
