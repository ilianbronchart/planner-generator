import streamlit as st
import cv2
import os
from datetime import datetime, timedelta
from src.draw_page import draw_page
from src.config import WINDOW_TITLE, START_HOUR, END_HOUR
import tkinter as tk
from tkinter import filedialog
from PIL import Image


def save_planner_images(start_hour, end_hour, start_date, weeks, pdf_path):
    images = []
    current_date = start_date
    
    for week in range(weeks):
        image = draw_page(start_hour, end_hour, current_date)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image)
        images.append(pil_image)
        current_date += timedelta(weeks=1)

    images[0].save(pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:])


def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    root.destroy()
    return folder_path

def toggle_preview():
    st.session_state['show_preview'] = not st.session_state['show_preview']


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.title(WINDOW_TITLE)

    if 'show_preview' not in st.session_state:
        st.session_state['show_preview'] = False
        st.session_state['folder_path'] = None

    start_hour = st.number_input("Enter start hour:", min_value=0, max_value=23, value=START_HOUR)
    end_hour = st.number_input("Enter end hour:", min_value=0, max_value=24, value=END_HOUR)

    # Calculate the date of the most recent Monday
    today = datetime.today()
    days_since_monday = today.weekday()
    monday_of_this_week = today - timedelta(days=days_since_monday)
    start_date = st.date_input("Enter start date (must be a Monday):", value=monday_of_this_week)

    weeks = st.number_input("Enter number of weeks:", min_value=1, value=1)
    file_name = st.text_input("Enter file name:", value="planner")

    if st.button("Select Destination Folder"):
        st.session_state['folder_path'] = select_folder()
        st.text_input("Selected folder path:", st.session_state['folder_path'], disabled=True)

    if st.session_state['show_preview']:
        st.button("Hide Preview", on_click=toggle_preview)
    else:
        st.button("Show Preview", on_click=toggle_preview)

    if st.session_state['show_preview']:
        if start_date.weekday() == 0:
            image = draw_page(start_hour, end_hour, start_date)
            st.image(image, channels="BGR")
        else:
            st.error("Start date must be a Monday.")

    if st.button("Generate Planner Pages"):
        folder_path = st.session_state.get('folder_path', '')

        if start_date.weekday() == 0:
            if folder_path and os.path.isdir(folder_path):
                pdf_path = os.path.join(folder_path, f'{file_name}.pdf')
                if os.path.exists(pdf_path):
                    st.error("The PDF file already exists. Please choose a different file name or folder.")
                else:
                    save_planner_images(start_hour, end_hour, start_date, weeks, pdf_path)
                    st.success(f"Planner PDF generated at {pdf_path}!")
            elif not folder_path:
                st.error("No folder path was selected.")
            else:
                st.error("The specified folder path does not exist.")
        else:
            st.error("Start date must be a Monday.")
