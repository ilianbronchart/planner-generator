import cv2
import numpy as np
from src.utils import cm_to_px
from src.config import START_HOUR, END_HOUR, FONT, FONT_SCALE, FONT_THICKNESS, LINE_COLOR, LINE_THICKNESS, DPI, WIDTH, HEIGHT
from datetime import datetime, timedelta


# Parameters
section_width = cm_to_px(4)
leftmost_section_width = WIDTH - 7 * section_width

top_section_height = cm_to_px(1)
top_gap_height = cm_to_px(0.5)

hour_height = cm_to_px(1)
guide_mark_width = cm_to_px(0.1)


def draw_vertical_lines(image):
    # Draw vertical lines to delineate the sections
    for i in range(0, 7):
        x = leftmost_section_width + (i * section_width)
        cv2.line(image, (x, 0), (x, HEIGHT), LINE_COLOR, LINE_THICKNESS)


def draw_horizontal_lines(image):
    # Draw top section
    y = top_section_height
    cv2.line(image, (0, y), (WIDTH, y), LINE_COLOR, LINE_THICKNESS)

    # Draw top gap starting from first vertical line
    y = top_section_height + top_gap_height
    x = leftmost_section_width
    cv2.line(image, (x, y), (WIDTH, y), LINE_COLOR, LINE_THICKNESS)

    # Draw leftmost horizontal hour guide marks
    num_hours = END_HOUR - START_HOUR
    for i in range(0, num_hours + 1):
        y = top_section_height + top_gap_height + (i * hour_height)
        x1 = leftmost_section_width - guide_mark_width / 2
        x2 = leftmost_section_width
        cv2.line(image, (int(x1), y), (int(x2), y), LINE_COLOR, LINE_THICKNESS)

    # Draw horizontal hour guide marks for each section for each hour
    for i in range(0, 7):
        for j in range(0, num_hours + 1):
            y = top_section_height + top_gap_height + (j * hour_height)
            x1 = leftmost_section_width + (i * section_width) - guide_mark_width / 2
            x2 = leftmost_section_width + (i * section_width) + guide_mark_width / 2
            cv2.line(image, (int(x1), y), (int(x2), y), LINE_COLOR, LINE_THICKNESS)

    # Draw bottom line
    y = top_section_height + top_gap_height + (num_hours * hour_height)
    x = leftmost_section_width
    cv2.line(image, (x, y), (WIDTH, y), LINE_COLOR, LINE_THICKNESS)


def draw_hours(image):
    # Calculate text HEIGHT and WIDTH to center text
    (text_width, text_height), baseline = cv2.getTextSize("00:00", FONT, FONT_SCALE, FONT_THICKNESS)
    
    for i in range(START_HOUR, END_HOUR + 1):
        # Convert hour to h:mm format
        hour_str = f"{str(i).zfill(2)}:00"
        
        # Calculate position
        y = top_section_height + top_gap_height + (i - START_HOUR) * hour_height + text_height // 2
        x = (leftmost_section_width - text_width) // 2
        
        # Draw text
        cv2.putText(image, hour_str, (x, y), FONT, FONT_SCALE, LINE_COLOR, FONT_THICKNESS)


def draw_days(image, start_date):
    left_padding = cm_to_px(0.2)
    right_padding = cm_to_px(0.2)
    
    current_date = start_date
    section_index = 0
    
    # Ensure start_date is a Monday
    if start_date.weekday() != 0:
        raise ValueError("The start date must be a Monday.")
    
    # Calculate end_date as 6 days after start_date
    end_date = start_date + timedelta(days=6)
    
    current_date = start_date
    section_index = 0
    
    while current_date <= end_date and section_index < 7:
        # Format day of the week and date
        day_str = current_date.strftime("%a")
        date_str = current_date.strftime("%d/%m")
        
        # Calculate text size
        (day_text_width, day_text_height), baseline = cv2.getTextSize(day_str, FONT, FONT_SCALE, FONT_THICKNESS)
        (date_text_width, date_text_height), baseline = cv2.getTextSize(date_str, FONT, FONT_SCALE, FONT_THICKNESS)
        
        # Calculate position
        y = (top_section_height + day_text_height) // 2
        x_day = leftmost_section_width + (section_index * section_width) + left_padding
        x_date = leftmost_section_width + ((section_index + 1) * section_width) - right_padding - date_text_width
        
        # Draw text
        cv2.putText(image, day_str, (int(x_day), y), FONT, FONT_SCALE, LINE_COLOR, FONT_THICKNESS)
        cv2.putText(image, date_str, (int(x_date), y), FONT, FONT_SCALE, LINE_COLOR, FONT_THICKNESS)
        
        # Move to next day and section
        current_date += timedelta(days=1)
        section_index += 1


def draw_year(image, start_date):
    current_year = str(start_date.year)
    
    (text_width, text_height), baseline = cv2.getTextSize(current_year, FONT, FONT_SCALE, FONT_THICKNESS)
    x = (leftmost_section_width - text_width) // 2
    y = (top_section_height + text_height) // 2
    
    cv2.putText(image, current_year, (x, y), FONT, FONT_SCALE, LINE_COLOR, FONT_THICKNESS)


def draw_page(start_date):
    image = np.ones((HEIGHT, WIDTH, 3), np.uint8) * 255

    draw_vertical_lines(image)
    draw_horizontal_lines(image)
    draw_hours(image)
    draw_days(image, start_date)
    draw_year(image, start_date)

    return image
