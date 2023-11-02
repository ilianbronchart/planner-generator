import cv2

# Create a blank A4 image in landscape orientation
WIDTH = int(3508)
HEIGHT = int(2480)

# Set line color (B, G, R) and thickness
LINE_COLOR = (0, 0, 0)  # Black
LINE_THICKNESS = 3

DPI = 300
START_HOUR = 8
END_HOUR = 24
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 1.7
FONT_THICKNESS = 3