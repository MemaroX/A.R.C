
import pyautogui
import pyperclip
import os
import tkinter as tk
import threading
import time

class MouseController:
    def left_click(self):
        pyautogui.click()

    def right_click(self):
        pyautogui.click(button='right')

    def move(self, dx, dy):
        pyautogui.move(dx, dy)

    def find_mouse(self):
        find_mouse_thread = threading.Thread(target=self._glow_effect)
        find_mouse_thread.start()

    def _glow_effect(self):
        root = tk.Tk()
        root.overrideredirect(True) # Remove window decorations
        root.attributes('-topmost', True) # Keep window on top
        root.wm_attributes('-transparentcolor', 'white') # Make white background transparent

        canvas = tk.Canvas(root, width=10, height=10, bg='white', highlightthickness=0)
        canvas.pack()

        size = 10
        for _ in range(10): # Fewer, faster iterations
            x, y = pyautogui.position() # Get current mouse position
            
            # Calculate window position to center the circle on the mouse
            win_x = x - size // 2
            win_y = y - size // 2
            root.geometry(f'{size}x{size}+{win_x}+{win_y}')
            
            canvas.delete("all")
            canvas.create_oval(0, 0, size, size, fill='red', outline='red')
            
            root.update_idletasks()
            root.update()
            
            size += 40 # Increase size more aggressively
            
            time.sleep(0.01) # Shorter sleep time for faster updates
        
        root.destroy()

class KeyboardController:
    def type_text(self, text):
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')

class MediaController:
    def press_key(self, key):
        pyautogui.press(key)

class PowerController:
    def shutdown(self):
        print("Simulating shutdown")
        # os.system('shutdown /s /t 1') # For Windows

    def restart(self):
        print("Simulating restart")
        # os.system('shutdown /r /t 1') # For Windows

class AppLauncher:
    def launch_app(self, app_name):
        if os.name == 'nt': # For Windows
            if app_name == 'calc':
                os.system('calc')
            elif app_name == 'notepad':
                os.system('notepad')

import comtypes
from pycaw.pycaw import AudioUtilities
import pythoncom
from pycaw.constants import EDataFlow, ERole, DEVICE_STATE, CLSID_MMDeviceEnumerator
from pycaw.pycaw import AudioUtilities, IMMDeviceEnumerator
import json
import win32api, win32con, win32gui, win32com.client

# Define the IPolicyConfig interface and its CLSID/IID
class IPolicyConfig(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{F8679F50-850A-41CF-9C72-430F290290C8}") # IID_IPolicyConfig
    _methods_ = [
        comtypes.STDMETHOD(None, "SetDefaultEndpoint", [comtypes.c_wchar_p, comtypes.c_int]),
    ]

# CLSID for PolicyConfigClient
CLSID_PolicyConfigClient = comtypes.GUID('{870AF99C-171D-4F9E-AF0D-E63DF40C2BC9}')

class FileBrowser:
    def list_files(self, path=None):
        if path is None:
            path = os.path.expanduser("~") # Start in the user's home directory
        
        files_list = []
        try:
            for f in os.listdir(path):
                full_path = os.path.join(path, f)
                files_list.append({'name': f, 'is_dir': os.path.isdir(full_path), 'path': full_path})
        except Exception as e:
            print(f"Error listing files: {e}")
            # You might want to return an error message to the client here
        return files_list

class AudioController:
    def list_audio_devices(self):
        pythoncom.CoInitialize()
        try:
            devices = []
            device_enumerator = comtypes.CoCreateInstance(
                CLSID_MMDeviceEnumerator,
                IMMDeviceEnumerator,
                comtypes.CLSCTX_INPROC_SERVER
            )
            
            collection = device_enumerator.EnumAudioEndpoints(EDataFlow.eRender.value, DEVICE_STATE.ACTIVE.value)
            
            count = collection.GetCount()
            for i in range(count):
                dev = collection.Item(i)
                if dev is not None:
                    audio_device = AudioUtilities.CreateDevice(dev)
                    if audio_device:
                        is_default = False
                        try:
                            default_device_raw = AudioUtilities.GetSpeakers()
                            default_device = AudioUtilities.CreateDevice(default_device_raw)
                            if default_device and audio_device.id == default_device.id:
                                is_default = True
                        except Exception as e:
                            print(f"Error checking default device status for {audio_device.FriendlyName}: {e}")
                        devices.append({'FriendlyName': audio_device.FriendlyName, 'id': audio_device.id, 'IsDefault': is_default})
            return devices
        finally:
            pythoncom.CoUninitialize()

    

    def switch_global_audio_output(self, device_name):
        """
        Attempts to switch the global audio output device by simulating UI interaction (keyboard only).
        This method is highly dependent on Windows UI layout and the order of devices.
        """
        print(f"Attempting to switch global audio output to: {device_name} via keyboard automation.")
        
        # Press Ctrl+Win+V to open the "App volume and device preferences"
        pyautogui.hotkey('ctrl', 'win', 'v')
        time.sleep(1) # Give time for the window to open and focus

        if device_name == 'Headphones':
            pyautogui.press('down') # Press down once for the second option
            time.sleep(0.2) # Small delay for UI to register
        # For Speakers, no 'down' press is needed as it's the first option
        
        # After navigating to the desired device, press Enter to select it
        pyautogui.press('enter')
        time.sleep(0.5) # Give time for the selection to apply

        print("Keyboard automation for audio device switching initiated.")
        
        # Close the window (e.g., by pressing Escape)
        pyautogui.press('esc')
        print("Please verify the audio output has switched.")
