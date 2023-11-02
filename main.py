import cv2
from src.draw_page import draw_page
from datetime import datetime


if __name__ == '__main__':
    start_date = datetime.strptime("06/11/2023", "%d/%m/%Y")
    image = draw_page(start_date)
    cv2.imwrite('plannergit sdt.png', image)