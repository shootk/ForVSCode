import cv2
import os
import sys
from PIL import Image
import pyocr
import numpy as np
from datetime import datetime as dt
from figureparts import Point, Line
from define_property import define_property


class Detector():
    def __init__(self, width=640, height=480, color=(200, 200, 200)):
        no_image = np.zeros(
            (width, height), dtype=np.uint8)
        self.__before_draw_image = no_image
        self.__after_draw_image = no_image
        self.__detect_low_white = np.array([160, 160, 140])
        self.__detect_high_white = np.array([190, 220, 190])

    @property
    def before_draw_image(self):
        return self.__before_draw_image

    @before_draw_image.setter
    def before_draw_image(self, image):
        self.__before_draw_image = image

    @property
    def after_draw_image(self):
        return self.__after_draw_image

    @after_draw_image.setter
    def after_draw_image(self, image):
        self.__after_draw_image = image

    @property
    def detect_low_white(self):
        return self.__detect_low_white

    @detect_low_white.setter
    def detect_low_white(self, color):
        self.__detect_low_white = np.array([
            # color[0] - (color[0] % 30
            0, color[1] - 30, color[2] - 30])

    @property
    def detect_high_white(self):
        return self.__detect_high_white

    @detect_high_white.setter
    def detect_high_white(self, color):
        self.__detect_high_white = np.array([
            # color[0] - (color[0] % 30) + 30
            360, color[1] + 30, color[2] + 30])

    def set_color(self, color):
        self.__detect_low_white = np.array([
            # color[0] - (color[0] % 30
            0, color[1] - 30, color[2] - 30])
        self.__detect_high_white = np.array([
            # color[0] - (color[0] % 30) + 30
            360, color[1] + 30, color[2] + 30])

    def queue(self, img):
        self.__before_draw_image = self.__after_draw_image
        self.__after_draw_image = img

    def get_difference(self, src1_image, src2_image):
        diff = cv2.absdiff(src1_image, src2_image)
        return cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    def get_white(self, src_image, low_white, high_white):
        src_image = cv2.cvtColor(src_image, cv2.COLOR_BGR2HSV_FULL)
        return cv2.inRange(src_image, low_white, high_white)

    def get_same_part(self, src1_image, src2_image):
        return cv2.bitwise_and(src1_image, src2_image)

    def get_edge(self, src_image):
        return cv2.Canny(src_image, 70, 100, 30)

    def save_picture(self, pic_list):
        date = dt.now().strftime('%Y-%m-%d/%H-%M-%S')
        for i, picture in enumerate(pic_list):
            cv2.imwrite(
                'images/{0}-{1}.png'.format(str(date), str(i)), picture)


class LineDetector(Detector):
    def __init__(self, width=640, height=480, color=(200, 200, 200)):
        super(LineDetector, self).__init__(
            width=width, height=height, color=color)
        define_property(self=self, name='detected_line', value=Line())

    def get_lines(self, src_image):
        lines = cv2.HoughLinesP(src_image, rho=1,
                                theta=np.pi / 360, threshold=40, minLineLength=40, maxLineGap=100)
        detedted_lines = []
        if lines is not None:
            for x1, y1, x2, y2 in lines[0]:
                line = Line(Point(x1, y1), Point(x2, y2))
                detedted_lines.append(line)
        return detedted_lines

    def get_longest_line(self, lines):
        max_line = self.__detected_line
        for line in lines:
            if max_line.length < line.length:
                max_line = line
        return max_line

    def detect(self, before_image=None, after_image=None):
        if (before_image is None) or (after_image is None):
            before_image = self.before_draw_image
            after_image = self.after_draw_image
        diff = self.get_difference(
            before_image,
            after_image)
        white = self.get_white(
            after_image,
            self.detect_low_white,
            self.detect_high_white)
        same = self.get_same_part(diff, white)
        edge = self.get_edge(same)
        self.save_picture(
            [before_image, after_image,
             diff, white, same, edge])
        if edge is not None:
            lines = self.get_lines(edge)
            line = self.get_longest_line(lines)
            return line
        else:
            print('No lines')


class CharacterDetector(Detector):
    def __init__(self, width=640, height=480, color=(200, 200, 200)):
        super().__init__()
        TESSERACT_PATH = 'C:\\Program Files (x86)\\Tesseract-OCR'
        TESSDATA_PATH = 'C:\\Program Files (x86)\\Tesseract-OCR\\tessdata'

        os.environ["PATH"] += os.pathsep + TESSERACT_PATH
        os.environ["TESSDATA_PREFIX"] = TESSDATA_PATH

        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print("No OCR tool found")
            sys.exit("No OCR tool found")
        define_property(self, name='ocr_tool',
                        value=tools[0], writable=False)

    def detect(self, before_image=None, after_image=None, language='jpn'):
        if (before_image is None) or (after_image is None):
            before_image = self.before_draw_image
            after_image = self.after_draw_image
        diff = self.get_difference(
            before_image,
            after_image)
        white = self.get_white(
            after_image,
            self.detect_low_white,
            self.detect_high_white)
        same = self.get_same_part(diff, white)
        inverse = cv2.bitwise_not(same)
        target_image = Image.fromarray(inverse)
        detect_text = self.ocr_tool.image_to_string(
            image=target_image,
            lang=language,
            builder=pyocr.builders.TextBuilder(tesseract_layout=6))
        self.save_picture(
            [before_image, after_image,
             diff, white, same, inverse])
        return detect_text
