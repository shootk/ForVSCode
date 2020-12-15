import pyocr
import os
from PIL import Image
import cv2
from datetime import datetime as dt
import numpy as np
from detector import LineDetector
import time
"""
TESSERACT_PATH = 'C:\\Program Files (x86)\\Tesseract-OCR'
TESSDATA_PATH = 'C:\\Program Files (x86)\\Tesseract-OCR\\tessdata'

os.environ["PATH"] += os.pathsep + TESSERACT_PATH
os.environ["TESSDATA_PREFIX"] = TESSDATA_PATH

tools = pyocr.get_available_tools()
ocr = tools[0]

image = cv2.imread('images/image.png', 0)
image = cv2.threshold(image, 30, 255, cv2.THRESH_OTSU)
cv2.imshow('', image)
cv2.imwrite('images/target.png', image)

image = Image.open('images/target.png')
texts = ocr.image_to_string(image, lang='jpn',
                            builder=pyocr.builders.LineBoxBuilder(tesseract_layout=6))
for text in texts:
    print(text.position, text.content)
"""

"""
detect_low_white = np.array([0, 0, 190])
detect_high_white = np.array([360, 60, 255])


def get_difference(src1_image, after_image):
    diff = cv2.absdiff(src1_image, after_image)
    return cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)


def get_difference_gray(src1_image, after_image):
    return cv2.absdiff(src1_image, after_image)


def get_white(src_image, low_white, high_white):
    src_image = cv2.cvtColor(src_image, cv2.COLOR_BGR2HSV_FULL)
    return cv2.inRange(src_image, low_white, high_white)


def get_same_part(src1_image, after_image):
    return cv2.bitwise_and(src1_image, after_image)


def get_edge(src_image):
    return cv2.Canny(src_image, 40, 150)


date = dt.now().strftime('%Y-%m-%d-%H-%M-%S')

back = cv2.imread('images/back_img.png')
# back = cv2.cvtColor(back, cv2.COLOR_RGB2HSV_FULL)
write_name = './images/H.png'
cv2.imwrite(write_name, back)

before = cv2.imread('images/before.png')
# before = cv2.cvtColor(before, cv2.COLOR_RGB2HSV_FULL)
write_name = './images/I1.png'
cv2.imwrite(write_name, before)

after = cv2.imread('images/after.png')
# after = cv2.cvtColor(after, cv2.COLOR_RGB2HSV_FULL)
write_name = './images/I2.png'
cv2.imwrite(write_name, after)

diff1 = get_difference(back, before)
write_name = './images/J1.png'
cv2.imwrite(write_name, diff1)

diff2 = get_difference(back, after)
write_name = './images/J2.png'
cv2.imwrite(write_name, diff2)

diff3 = get_difference_gray(diff1, diff2)
write_name = './images/K.png'
cv2.imwrite(write_name, diff3)

white = get_white(after, detect_low_white, detect_high_white)
write_name = './images/L.png'
cv2.imwrite(write_name, white)

same = get_same_part(diff3, white)
write_name = './images/X.png'
cv2.imwrite(write_name, same)

edge = get_edge(same)
write_name = './images/Z.png'
cv2.imwrite(write_name, edge)
"""


def main():
    detector = LineDetector()
    camera = cv2.VideoCapture(1)
    while():
        return_value, frame = camera.read()
        if return_value:
            back_image = frame
            break
    detector.back_image = back_image

    while():
        time.sleep(1)


if __name__ == "__main__":
    main()
