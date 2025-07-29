
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
