
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import pyautogui
import pyperclip
import os
import tkinter as tk
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files')
def list_files():
    path = os.path.expanduser("~") # Start in the user's home directory
    files = []
    for f in os.listdir(path):
        files.append({'name': f, 'is_dir': os.path.isdir(os.path.join(path, f))})
    return jsonify(files)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def glow_effect():
    root = tk.Tk()
    root.overrideredirect(True) # Remove window decorations
    root.attributes('-topmost', True) # Keep window on top
    root.wm_attributes('-transparentcolor', 'white') # Make white background transparent

    canvas = tk.Canvas(root, width=10, height=10, bg='white', highlightthickness=0)
    canvas.pack()

    x, y = pyautogui.position()
    
    # Initial position and size
    size = 10
    alpha = 1.0
    
    for _ in range(20): # Expand and fade for a few iterations
        x, y = pyautogui.position() # Get current mouse position
        
        # Calculate window position to center the circle on the mouse
        win_x = x - size // 2
        win_y = y - size // 2
        root.geometry(f'{size}x{size}+{win_x}+{win_y}')
        
        canvas.delete("all")
        canvas.create_oval(0, 0, size, size, fill='red', outline='red')
        
        # Update transparency (requires a bit of a hack for Tkinter)
        # This is a simplified approach, actual fading is more complex with Tkinter
        # For a true fade, you'd need to draw semi-transparent shapes or use a different library
        
        root.update_idletasks()
        root.update()
        
        size += 15 # Increase size
        alpha -= 0.05 # Decrease alpha (for conceptual fading)
        if alpha < 0:
            alpha = 0
        
        time.sleep(0.05)
    
    root.destroy()



@socketio.on('mouse')
def handle_mouse(data):
    if data['type'] == 'move':
        pyautogui.move(data['dx'], data['dy'])
    elif data['type'] == 'left_click':
        pyautogui.click()
    elif data['type'] == 'right_click':
        pyautogui.click(button='right')
    elif data['type'] == 'find':
        find_mouse_thread = threading.Thread(target=glow_effect)
        find_mouse_thread.start()

@socketio.on('keyboard')
def handle_keyboard(data):
    pyperclip.copy(data['key'])
    pyautogui.hotkey('ctrl', 'v')

@socketio.on('media')
def handle_media(data):
    pyautogui.press(data['key'])

@socketio.on('power')
def handle_power(data):
    if data['action'] == 'shutdown':
        print("Simulating shutdown")
    elif data['action'] == 'restart':
        print("Simulating restart")

@socketio.on('launch')
def handle_launch(data):
    if os.name == 'nt': # For Windows
        if data['app'] == 'calc':
            os.system('calc')
        elif data['app'] == 'notepad':
            os.system('notepad')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
