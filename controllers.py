
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


# Winamp IPC Constants
WM_COMMAND = 0x0111
WM_USER = 0x0400

IPC_GETVERSION = 0 # Returns Winamp version
IPC_PLAY = 104 # Play
IPC_PAUSE = 105 # Pause
IPC_STOP = 106 # Stop
IPC_NEXT = 40044 # Next track
IPC_PREV = 40045 # Previous track
IPC_SETVOLUME = 114 # Set volume (0-255)
IPC_GETOUTPUTTIME = 107 # Get current track position/length
IPC_GETPLAYLISTTITLE = 212 # Get title of playlist item at index
IPC_GETPLAYLISTLENGTH = 211 # Get playlist length
IPC_ISPLAYING = 104 # Get playback status (0=stopped, 1=playing, 3=paused)
IPC_ENQUEUEFILE = 100 # Enqueue file (uses WM_COPYDATA)
IPC_DELETE = 101 # Clear playlist
IPC_GETLISTPOS = 124 # Get current playlist position
IPC_SETPLAYLISTPOS = 125 # Set current playlist position
IPC_GETSHUFFLE = 250 # Get shuffle status
IPC_GETREPEAT = 251 # Get repeat status

# WM_COMMAND messages for toggles
WINAMP_SHUFFLE_TOGGLE = 40023
WINAMP_REPEAT_TOGGLE = 40022

class WinampController:
    def __init__(self):
        self.winamp_hwnd = None

    def _find_winamp_window(self):
        if self.winamp_hwnd and win32gui.IsWindow(self.winamp_hwnd):
            return self.winamp_hwnd
        
        self.winamp_hwnd = win32gui.FindWindow("Winamp v1.x", None) # Main window
        if not self.winamp_hwnd:
            self.winamp_hwnd = win32gui.FindWindow("Winamp AVS", None)
        
        if not self.winamp_hwnd:
            print("Winamp window not found. Please ensure Winamp is running.")
        return self.winamp_hwnd

    def _send_winamp_command(self, command, param=0):
        hwnd = self._find_winamp_window()
        if hwnd:
            win32api.SendMessage(hwnd, WM_COMMAND, command, param)
            return True
        return False

    def _send_winamp_ipc(self, command, param=0):
        hwnd = self._find_winamp_window()
        if hwnd:
            result = win32api.SendMessage(hwnd, WM_USER, param, command)
            return result
        return False

    def play_pause(self):
        print("Winamp: Play/Pause")
        # WM_COMMAND with 40046 is the play/pause toggle
        return self._send_winamp_command(40046)

    def next_track(self):
        print("Winamp: Next Track")
        return self._send_winamp_command(IPC_NEXT)

    def prev_track(self):
        print("Winamp: Previous Track")
        return self._send_winamp_command(IPC_PREV)

    def set_volume(self, volume_percent):
        winamp_volume = int((volume_percent / 100) * 255)
        print(f"Winamp: Set Volume to {volume_percent}% ({winamp_volume}/255)")
        return self._send_winamp_ipc(IPC_SETVOLUME, winamp_volume)

    def get_current_track_title(self):
        hwnd = self._find_winamp_window()
        if hwnd:
            title = win32gui.GetWindowText(hwnd)
            if " - Winamp" in title:
                return title.replace(" - Winamp", "").strip()
            return title
        return "N/A"

    def get_playback_status(self):
        hwnd = self._find_winamp_window()
        if hwnd:
            status = self._send_winamp_ipc(IPC_ISPLAYING, 0)
            if status == 1:
                return "Playing"
            elif status == 3:
                return "Paused"
            elif status == 0:
                return "Stopped"
        return "Unknown"

    def get_playlist_length(self):
        hwnd = self._find_winamp_window()
        if hwnd:
            length = self._send_winamp_ipc(IPC_GETPLAYLISTLENGTH, 0)
            return length if length != -1 else 0
        return 0

    def get_playlist_position(self):
        hwnd = self._find_winamp_window()
        if hwnd:
            pos = self._send_winamp_ipc(IPC_GETLISTPOS, 0)
            return pos if pos != -1 else 0
        return 0

    def jump_to_track(self, index):
        print(f"Winamp: Jump to track {index}")
        return self._send_winamp_ipc(IPC_SETPLAYLISTPOS, index)

    def toggle_shuffle(self):
        print("Winamp: Toggle Shuffle")
        return self._send_winamp_command(WINAMP_SHUFFLE_TOGGLE)

    def toggle_repeat(self):
        print("Winamp: Toggle Repeat")
        return self._send_winamp_command(WINAMP_REPEAT_TOGGLE)

    def get_shuffle_status(self):
        hwnd = self._find_winamp_window()
        if hwnd:
            status = self._send_winamp_ipc(IPC_GETSHUFFLE, 0)
            return "On" if status == 1 else "Off"
        return "Unknown"

    def get_repeat_status(self):
        hwnd = self._find_winamp_window()
        if hwnd:
            status = self._send_winamp_ipc(IPC_GETREPEAT, 0)
            return "On" if status == 1 else "Off"
        return "Unknown"

    def get_playback_time(self):
        hwnd = self._find_winamp_window()
        if hwnd:
            current_ms = self._send_winamp_ipc(IPC_GETOUTPUTTIME, 0) # Current position in ms
            total_ms = self._send_winamp_ipc(IPC_GETOUTPUTTIME, 1) # Total length in seconds, need to convert to ms
            
            if current_ms != -1 and total_ms != -1:
                total_ms = total_ms * 1000 # Convert seconds to milliseconds
                return {'current_ms': current_ms, 'total_ms': total_ms}
        return {'current_ms': 0, 'total_ms': 0}

    def add_file_to_playlist(self, file_path):
        # IPC_ENQUEUEFILE uses WM_COPYDATA, which is complex to implement directly in pywin32.
        # It requires creating a COPYDATASTRUCT and passing a pointer to it.
        # For now, this remains a known limitation for direct IPC.
        print(f"Adding file {file_path} to Winamp playlist is complex via IPC_ENQUEUEFILE (WM_COPYDATA).")
        print("Consider using a command-line utility like clever.exe or WACommand.exe if available, or manual drag-and-drop.")
        return False

    def clear_playlist(self):
        print("Winamp: Clear Playlist")
        return self._send_winamp_ipc(IPC_DELETE)

