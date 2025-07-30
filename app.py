from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from controllers import MouseController, KeyboardController, MediaController, PowerController, AppLauncher, FileBrowser, AudioController, WinampController

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize controllers
mouse_controller = MouseController()
keyboard_controller = KeyboardController()
media_controller = MediaController()
power_controller = PowerController()
app_launcher = AppLauncher()
file_browser = FileBrowser()
audio_controller = AudioController()
winamp_controller = WinampController()

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

@socketio.on('list_audio_devices')
def handle_list_audio_devices():
    devices = audio_controller.list_audio_devices()
    socketio.emit('audio_devices_list', devices)



@socketio.on('switch_global_audio')
def handle_switch_global_audio(data):
    device_name = data['device_name']
    audio_controller.switch_global_audio_output(device_name)
    socketio.emit('global_audio_switch_status', {'device_name': device_name, 'status': 'attempted'})

@socketio.on('winamp_control')
def handle_winamp_control(data):
    action = data['action']
    if action == 'play_pause':
        winamp_controller.play_pause()
    elif action == 'next_track':
        winamp_controller.next_track()
    elif action == 'prev_track':
        winamp_controller.prev_track()
    elif action == 'set_volume':
        volume = data['volume']
        winamp_controller.set_volume(volume)
    socketio.emit('winamp_status', {'action': action, 'status': 'attempted'})

@socketio.on('winamp_get_track_info')
def handle_winamp_get_track_info():
    title = winamp_controller.get_current_track_title()
    status = winamp_controller.get_playback_status()
    socketio.emit('winamp_track_info', {'title': title, 'status': status})

@socketio.on('winamp_get_playlist_info')
def handle_winamp_get_playlist_info():
    length = winamp_controller.get_playlist_length()
    position = winamp_controller.get_playlist_position()
    socketio.emit('winamp_playlist_info', {'length': length, 'position': position})

@socketio.on('winamp_jump_to_track')
def handle_winamp_jump_to_track(data):
    index = data['index']
    success = winamp_controller.jump_to_track(index)
    socketio.emit('winamp_jump_status', {'index': index, 'success': success})

@socketio.on('winamp_toggle_shuffle')
def handle_winamp_toggle_shuffle():
    success = winamp_controller.toggle_shuffle()
    socketio.emit('winamp_toggle_shuffle_status', {'success': success})

@socketio.on('winamp_toggle_repeat')
def handle_winamp_toggle_repeat():
    success = winamp_controller.toggle_repeat()
    socketio.emit('winamp_toggle_repeat_status', {'success': success})

@socketio.on('winamp_get_shuffle_status')
def handle_winamp_get_shuffle_status():
    status = winamp_controller.get_shuffle_status()
    socketio.emit('winamp_shuffle_status', {'status': status})

@socketio.on('winamp_get_repeat_status')
def handle_winamp_get_repeat_status():
    status = winamp_controller.get_repeat_status()
    socketio.emit('winamp_repeat_status', {'status': status})

@socketio.on('winamp_get_playback_time')
def handle_winamp_get_playback_time():
    time_info = winamp_controller.get_playback_time()
    socketio.emit('winamp_playback_time', time_info)

@socketio.on('winamp_add_file')
def handle_winamp_add_file(data):
    file_path = data['file_path']
    success = winamp_controller.add_file_to_playlist(file_path)
    socketio.emit('winamp_add_file_status', {'file_path': file_path, 'success': success})

@socketio.on('winamp_clear_playlist')
def handle_winamp_clear_playlist():
    success = winamp_controller.clear_playlist()
    socketio.emit('winamp_clear_playlist_status', {'success': success})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)