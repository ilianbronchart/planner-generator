import webview
import os
from src.config import WINDOW_TITLE, WINDOW_URL, WINDOW_WIDTH, WINDOW_HEIGHT
from streamlit.web import cli
import multiprocessing
import keyboard
import time

def run_server():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'app.py')
    args = ["--server.headless=true", "--browser.gatherUsageStats=false"]
    cli._main_run_clexplicit(filename, 'streamlit run', args)

def run(window):
    global server_process
    global running
    running = True
    server_process = multiprocessing.Process(target=run_server)
    server_process.start()

    while running:
        time.sleep(0.2)  # Prevent high CPU usage
        if keyboard.is_pressed('esc'):
            window.destroy()
            server_process.terminate()
            break

def on_closing():
    global server_process
    global running
    server_process.terminate()
    running = False

if __name__ == '__main__':
    multiprocessing.freeze_support()
    # Create a pywebview window pointing to the local Streamlit server
    window = webview.create_window(
        title=WINDOW_TITLE, 
        url=WINDOW_URL, 
        width=WINDOW_WIDTH, 
        height=WINDOW_HEIGHT, 
        resizable=False, 
        fullscreen=False
    )
    window.events.closing += on_closing

    webview.start(run, window)
