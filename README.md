# A.R.C. (Advanced Remote Control)

A Python-based web remote control application that allows you to control your computer from any device with a web browser. Features include mouse control (with a mousepad and a 'find mouse' glow effect), keyboard input (with Arabic support), media controls, application launching, and a basic file browser.

## Features:
- Mouse control (left/right click, movement, 'find mouse' glow)
- Keyboard input (supports Unicode/Arabic via clipboard)
- Media controls (play/pause, next/previous track, volume up/down, mute)
- Application Launcher (e.g., Calculator, Notepad)
- Basic File Browser
- WebSockets for real-time communication
- Clean, modular, and object-oriented codebase

## Setup:
1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd PythonRemote
    ```
2.  **Install dependencies:**
    ```bash
    pip install Flask Flask-SocketIO pyautogui pyperclip
    ```
3.  **Run the server:**
    ```bash
    python app.py
    ```
4.  **Access the remote:**
    Open a web browser on your phone or another device and navigate to `http://<your_computer_ip>:5000` (replace `<your_computer_ip>` with your computer's actual IP address).

## Contributing:
Feel free to fork the repository and contribute to A.R.C.!
