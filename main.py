import webview
import os
from src.config import WINDOW_TITLE, WINDOW_URL, WINDOW_WIDTH, WINDOW_HEIGHT


def run(window):
    os.system("streamlit run app.py --server.headless=true --browser.gatherUsageStats=false")
    window.destroy()

if __name__ == '__main__':
    # Create a pywebview window pointing to the local Streamlit server
    window = webview.create_window(
        title=WINDOW_TITLE, 
        url=WINDOW_URL, 
        width=WINDOW_WIDTH, 
        height=WINDOW_HEIGHT, 
        resizable=False, 
        fullscreen=False
    )
    webview.start(run, window)
