from flask import Flask, render_template
from flask_socketio import SocketIO
import pyautogui

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

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
    pyautogui.typewrite(data['key'])

@socketio.on('media')
def handle_media(data):
    pyautogui.press(data['key'])

@socketio.on('power')
def handle_power(data):
    if data['action'] == 'shutdown':
        # This will not work on all systems. It's a placeholder.
        # For a real shutdown, you would need to use os-specific commands.
        print("Simulating shutdown")
    elif data['action'] == 'restart':
        print("Simulating restart")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)