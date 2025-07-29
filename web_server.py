
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import pyautogui
import pyperclip
import os

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

@socketio.on('mouse')
def handle_mouse(data):
    if data['type'] == 'move':
        pyautogui.move(data['dx'], data['dy'])
    elif data['type'] == 'left_click':
        pyautogui.click()
    elif data['type'] == 'right_click':
        pyautogui.click(button='right')

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
