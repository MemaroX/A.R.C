
from flask import Flask, render_template
import pyautogui

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/left_click')
def left_click():
    pyautogui.click()
    return "OK"

@app.route('/right_click')
def right_click():
    pyautogui.click(button='right')
    return "OK"

@app.route('/move/<int:x>/<int:y>')
def move(x, y):
    pyautogui.move(x, y)
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
