from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from controllers import MouseController, KeyboardController, MediaController, PowerController, AppLauncher, FileBrowser

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize controllers
mouse_controller = MouseController()
keyboard_controller = KeyboardController()
media_controller = MediaController()
power_controller = PowerController()
app_launcher = AppLauncher()
file_browser = FileBrowser()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files')
def list_files():
    current_path = request.args.get('path')
    files = file_browser.list_files(current_path)
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
        mouse_controller.move(data['dx'], data['dy'])
    elif data['type'] == 'left_click':
        mouse_controller.left_click()
    elif data['type'] == 'right_click':
        mouse_controller.right_click()
    elif data['type'] == 'find':
        mouse_controller.find_mouse()

@socketio.on('keyboard')
def handle_keyboard(data):
    keyboard_controller.type_text(data['key'])

@socketio.on('media')
def handle_media(data):
    media_controller.press_key(data['key'])

@socketio.on('power')
def handle_power(data):
    if data['action'] == 'shutdown':
        power_controller.shutdown()
    elif data['action'] == 'restart':
        power_controller.restart()

@socketio.on('launch')
def handle_launch(data):
    app_launcher.launch_app(data['app'])

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)