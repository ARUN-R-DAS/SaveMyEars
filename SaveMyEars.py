# for lib check
import subprocess
import sys
# --------------------- lib check --------------------------
required_libraries = ["pycaw", "comtypes", "winotify"]

for lib in required_libraries:
    try:
        __import__(lib)
    except ImportError:
        print(f"Library '{lib}' not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
        print(f"'{lib}' installed successfully!")
# --------------------- Actual Program --------------------------
# now safe to import
from pycaw.pycaw import AudioUtilities
from winotify import Notification
import time

prev_device = AudioUtilities.GetSpeakers().FriendlyName

def show_notification(message):
    toast = Notification(
        app_id="SaveMyEars",
        title="SaveMyEars",
        msg=message,
        duration="short"  # "short" ~7s, "long" ~25s
    )
    toast.show()

def set_volume(level_percent):
    global prev_device
    """
    Set system master volume (0–100).
    """
    if not 0 <= level_percent <= 100:
        raise ValueError("Volume must be between 0 and 100")

    device = AudioUtilities.GetSpeakers()
    
    current_device = device.FriendlyName
    if prev_device != current_device:
        print(f"Device changed: {current_device}")
        # show_notification(f"Device changed: {current_device}")
        prev_device = current_device
        if current_device == 'Headphones (Noise Buds VS102 NEO)':
            print("Correct Device Detected - Volume set to 20%")
            show_notification("Headphones connected - Volume set to 20%")
            volume = device.EndpointVolume  # Correct way in newer pycaw
            volume.SetMasterVolumeLevelScalar(level_percent / 100.0, None)

if __name__ == "__main__":
    desired_volume = 20  # change this value
    while True:
        set_volume(desired_volume)
        time.sleep(2)
    # print(f"Volume set to {desired_volume}%")