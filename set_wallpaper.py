import os
import platform
import subprocess
import ctypes
from pathlib import Path

def set_wallpaper(image_path):
    """Change the desktop wallpaper based on the operating system."""
    system_name = platform.system()
    image_path = Path(image_path).resolve()

    if not image_path.is_file():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    if system_name == "Windows":
        # Convert the image path to a proper Windows string
        ctypes.windll.user32.SystemParametersInfoW(20, 0, str(image_path), 3)
        print(f"Wallpaper changed successfully on Windows.")
    elif system_name == "Darwin":  # macOS
        # Use AppleScript to change the wallpaper
        script = f"""
        tell application "System Events"
            tell every desktop
                set picture to "{image_path}"
            end tell
        end tell
        """
        subprocess.run(["osascript", "-e", script], check=True)
        print(f"Wallpaper changed successfully on macOS.")
    elif system_name == "Linux":
        # Assume GNOME desktop for simplicity
        try:
            subprocess.run(
                ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{image_path}"],
                check=True
            )
            print(f"Wallpaper changed successfully on GNOME-based Linux.")
        except FileNotFoundError:
            print("Failed to set wallpaper. Make sure `gsettings` is installed or use another desktop environment.")
    else:
        print(f"Unsupported operating system: {system_name}")

if __name__ == "__main__":
    # Provide the path to your image file here
    image_file = input("Enter the path to the image file: ").strip()
    try:
        set_wallpaper(image_file)
    except Exception as e:
        print(f"Error: {e}")
