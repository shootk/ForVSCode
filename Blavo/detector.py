import cv2
import os
import sys
from PIL import Image
import pyocr
import numpy as np
from datetime import datetime as dt
from figureparts import Line, TextBox
from define_property import define_property


class Detector():
    def __init__(self, width=640, height=480, color=(200, 200, 200)):
        no_image = np.zeros(
            (width, height), dtype=np.uint8)
        define_property(self=self, name='before_draw_image', value=no_image)
        define_property(self=self, name='after_draw_image', value=no_image)
        define_property(self=self, name='back_image', value=no_image)
        self.__detect_low_white = np.array([160, 160, 140])
        self.__detect_high_white = np.array([190, 220, 190])

    @property
    def detect_low_white(self):
        return self.__detect_low_white

    @detect_low_white.setter
    def detect_low_white(self, color, s_length=60, v_length=60):
        self.__detect_low_white = np.array([
            0, max(0, color[1] - s_length / 2), max(0, color[2] - v_length / 2)])

    @property
    def detect_high_white(self):
        return self.__detect_high_white

    @detect_high_white.setter
    def detect_high_white(self, color, s_length=60, v_length=60):
        self.__detect_high_white = np.array([
            360, min(color[1] + s_length / 2, 360), min(color[2] + v_length / 2, 360)])

    def set_color(self, color, s_length=60, v_length=60):
        self.__detect_low_white = np.array([
            0, max(0, color[1] - s_length / 2), max(0, color[2] - v_length / 2)])
        self.__detect_high_white = np.array([
            360, min(color[1] + s_length / 2, 360), min(color[2] + v_length / 2, 360)])

    def queue(self, img):
        self.before_draw_image = self.after_draw_image
        self.after_draw_image = img

    def set_back(self, img):
        self.back_image = img

    def get_difference(self, src_image1, src_image2):
        return cv2.absdiff(src_image1, src_image2)

    def get_white(self, src_image, low_white, high_white):
        return cv2.inRange(src_image, low_white, high_white)

    def get_same_part(self, src_image1, src_image2):
        return cv2.bitwise_and(src_image1, src_image2)

    def get_edge(self, src_image):
        return cv2.Canny(src_image, 40, 150)

    def save_picture(self, pic_list, word=''):
        date = dt.now().strftime('%Y-%m-%d-%H-%M-%S')
        for i, picture in enumerate(pic_list):
            write_name = './images/' + str(date) + word + str(i) + '.png'
            cv2.imwrite(write_name, picture)

    def detect(self, back_image, src_image1, src_image2):
        if not back_image:
            back_image = self.back_image
        if not src_image1:
            src_image1 = self.before_draw_image
        if not src_image2:
            src_image2 = self.after_draw_image
        diff_back1 = self.get_difference(back_image, src_image1)
        diff_back2 = self.get_difference(back_image, src_image2)
        diff_frame = self.get_difference(diff_back1, diff_back2)
        diff_frame = cv2.cvtColor(diff_frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("1", diff_back1)
        cv2.imshow("2", diff_back2)
        cv2.imshow("1-2", diff_frame)
        src_image3 = cv2.cvtColor(src_image2, cv2.COLOR_BGR2HSV_FULL)
        white = self.get_white(
            src_image3, self.detect_low_white, self.detect_high_white)
        cv2.imshow("white", white)
        same = self.get_same_part(diff_frame, white)
        return same


class LineDetector(Detector):
    def __init__(self, width=640, height=480, color=(200, 200, 200)):
        super(LineDetector, self).__init__(
            width=width, height=height, color=color)
        define_property(self=self, name='detected_line', value=Line())

    def get_lines(self, src_image):
        lines = cv2.HoughLinesP(src_image, rho=1,
                                theta=np.pi / 360, threshold=50, minLineLength=40, maxLineGap=50)
        detedted_lines = []
        if lines is not None:
            dst = src_image
            for x1, y1, x2, y2 in lines[0]:
                # print('line coordinate : ({0},{1})({2},{3})'.format(x1, y1, x2, y2))
                dst = cv2.line(dst, (x1, y1), (x2, y2), (255, 255, 255), 2)
                line = Line((x1, y1), (x2, y2))
                detedted_lines.append(line)
            cv2.imwrite('./images/lines.png', dst)
        else:
            print('no lines')
        return detedted_lines

    def get_longest_line(self, lines):
        max_line = self.detected_line
        for line in lines:
            if max_line.length < line.length:
                max_line = line
        return max_line

    def detect_line(self, back_image=None, before_image=None, after_image=None):
        same = self.detect(back_image, before_image, after_image)
        edge = self.get_edge(same)
        if edge is not None:
            lines = self.get_lines(edge)
            line = self.get_longest_line(lines)
            src_image = np.zeros(same.shape)
            src_image = cv2.line(
                src_image, tuple(line.start.coordinate), tuple(line.end.coordinate), (255, 255, 255), 2)
            cv2.imwrite('./images/line.png', src_image)
            return line
        else:
            print('No lines.')


class TextDetector(Detector):
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
        define_property(self=self, name='detect_text_box',
                        value=TextBox((0, 0), (0, 0), text=''))

    def detect_text(self, back_image=None, before_image=None, after_image=None, language='jpn'):
        same = self.detect(back_image, before_image, after_image)
        _, threshould = cv2.threshold(same, 0, 255, cv2.THRESH_OTSU)
        inverse = cv2.bitwise_not(threshould)
        cv2.imwrite('./images/target.png', inverse)
        target_image = Image.open('./images/target.png')
        target_image = Image.fromarray(inverse)
        builder = pyocr.builders.LineBoxBuilder(tesseract_layout=6)
        detect_texts = self.ocr_tool.image_to_string(
            image=target_image,
            lang=language,
            builder=builder)
        text_boxs = self.arrange_coordinate(
            detect_texts=detect_texts, height=target_image.height)
        text_box = self.get_corner_box(
            text_boxs, 0, 0)
        return text_box

    def arrange_coordinate(self, detect_texts=None, *, height):
        text_box_list = []
        for box in detect_texts:
            x, y = box.position[0]
            width, height = box.position[1]
            text_box_list.append(
                TextBox((x, y), width, height, text=box.content))
        return text_box_list

    def get_corner_box(self, text_boxs, x, y):
        if len(text_boxs) > 0:
            corner_box = text_boxs[0]
            target_pt = (x, y)
            min_length = Line(target_pt, corner_box.center).length
        else:
            return self.detect_text_box
        for text_box in text_boxs:
            length = Line(target_pt, text_box.center).length
            if length < min_length:
                min_length = length
                corner_box = text_box
            elif length == min_length:
                if text_box.center.Y < corner_box.center.Y:
                    min_length = length
                    corner_box = text_box
        return corner_box
