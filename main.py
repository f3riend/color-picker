from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from pynput import keyboard, mouse
from threading import Thread
from PIL import ImageGrab
import pyautogui
import webview
import sys

app = Flask(__name__, static_folder='static', static_url_path='/static')
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

colors = []

width = 400
height = 225

locX = 0
locY = pyautogui.size().height - height

def rgb_to_hex(rgb):
    r, g, b = rgb
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    hex_code = "#{:02x}{:02x}{:02x}".format(r, g, b)
    return hex_code

@app.route("/")
def main():
    return render_template("index.html", colors=colors)

def on_click(x, y, button, pressed):
    if button == mouse.Button.right and pressed:
        rgb = ImageGrab.grab().getpixel((x, y))
        hexcode = rgb_to_hex(rgb)
        colors.append([rgb, hexcode])
        socketio.emit("update", {'colors': colors})

def on_press(key):
    if key == keyboard.Key.esc:
        print("Escape key pressed. Exiting...")
        socketio.stop()  # Stop Flask-SocketIO server
        sys.exit(0)  # Exit the application

def start_mouse_listener():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

def start_keyboard_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def start_flask():
    socketio.run(app, debug=False, use_reloader=False)  # Disable debug and reloader

if __name__ == "__main__":
    listener_thread = Thread(target=start_mouse_listener)
    listener_thread.start()

    keyboard_listener_thread = Thread(target=start_keyboard_listener)
    keyboard_listener_thread.start()

    # Run Flask in a separate thread
    flask_thread = Thread(target=start_flask)
    flask_thread.start()

    # Start the WebView window
    window = webview.create_window("My App", "http://localhost:5000", x=locX, y=locY, width=width, height=height, frameless=True, on_top=True, draggable=False)
    webview.start()
