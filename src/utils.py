from src.config import DPI

def cm_to_px(cm):
    inch_to_cm = 2.54
    return int((cm / inch_to_cm) * DPI)