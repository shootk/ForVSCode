import pyocr
import os
from PIL import Image
import cv2
from datetime import datetime as dt
import numpy as np
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


detect_low_white = np.array([0, 0, 190])
detect_high_white = np.array([360, 60, 255])


def get_difference(src1_image, src2_image):
    diff = cv2.absdiff(src1_image, src2_image)
    return diff


def get_white(src_image, low_white, high_white):
    src_image = cv2.cvtColor(src_image, cv2.COLOR_BGR2HSV_FULL)
    return cv2.inRange(src_image, low_white, high_white)


date = dt.now().strftime('%Y-%m-%d-%H-%M-%S')
src1 = cv2.imread('images/2020-09-28-15-00-54img0.png')
src1 = get_white(src1, detect_low_white, detect_high_white)
write_name = './images/' + str(date) + 'white1.png'
cv2.imwrite(write_name, src1)

src2 = cv2.imread('images/2020-09-28-15-54-07img1.png')
src2 = get_white(src2, detect_low_white, detect_high_white)
write_name = './images/' + str(date) + 'white2.png'
cv2.imwrite(write_name, src2)

src3 = cv2.imread('images/2020-09-28-15-54-07img0.png')
src3 = get_white(src3, detect_low_white, detect_high_white)
write_name = './images/' + str(date) + 'white3.png'
cv2.imwrite(write_name, src3)

diff1 = get_difference(src1, src2)
diff2 = get_difference(src1, src3)
diff3 = get_difference(src2, src3)
write_name = './images/' + str(date) + 'diff1.png'
cv2.imwrite(write_name, diff1)
write_name = './images/' + str(date) + 'diff2.png'
cv2.imwrite(write_name, diff2)
write_name = './images/' + str(date) + 'diff3.png'
cv2.imwrite(write_name, diff3)
