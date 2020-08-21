import cv2
import numpy as np
from datetime import datetime as dt
from figure_module.figureparts import Point, Line


class LineDitector():
    def __init__(self, width=640, height=480, color=(200, 200, 200)):
        self.__before_drawline_image = np.zeros(
            (width, height), dtype=np.uint8)
        self.__after_drawline_image = np.zeros(
            (width, height), dtype=np.uint8)
        self.detected_line = Line()
        self.__ditect_low_white = np.array([160, 160, 140])
        self.__ditect_high_white = np.array([190, 220, 190])

    @property
    def before_drawline_image(self):
        return self.__before_drawline_image

    @before_drawline_image.setter
    def before_drawline_image(self, img):
        self.__before_drawline_image = img

    @property
    def after_drawline_image(self):
        return self.__after_drawline_image

    @after_drawline_image.setter
    def after_drawline_image(self, img):
        self.__after_drawline_image = img

    @property
    def ditect_low_white(self):
        return self.__ditect_low_white

    @ditect_low_white.setter
    def ditect_low_white(self, color):
        self.ditect_low_white = np.array([
            # color[0] - (color[0] % 30
            0, color[1] - 30, color[2] - 30])

    @property
    def ditect_high_white(self):
        return self.__ditect_high_white

    @ditect_high_white.setter
    def ditect_high_white(self, color):
        self.ditect_high_white = np.array([
            # color[0] - (color[0] % 30) + 30
            360, color[1] + 30, color[2] + 30])

    def set_color(self, color):
        self.ditect_low_white(color)
        self.ditect_high_white(color)

    def queue(self, img):
        self.__before_drawline_image = self.__after_drawline_image
        self.__after_drawline_image = img

    def get_difference(self, src1_image, src2_image):
        diff = cv2.absdiff(src1_image, src2_image)
        return cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    def get_white(self, src_image):
        src_image = cv2.cvtColor(src_image, cv2.COLOR_BGR2HSV_FULL)
        return cv2.inRange(src_image, self.__ditect_low_white, self.__ditect_high_white)

    def get_same_part(self, src1_image, src2_image):
        return cv2.bitwise_and(src1_image, src2_image)

    def detect_edge(self, src_image):
        return cv2.Canny(src_image, 70, 100, 30)

    def detect_line(self, src_image):
        lines = cv2.HoughLinesP(src_image, rho=1,
                                theta=np.pi / 360, threshold=40, minLineLength=40, maxLineGap=100)
        detedted_lines = []
        if lines:
            for x1, y1, x2, y2 in lines[0]:
                line = Line(Point(x1, y1), Point(x2, y2))
                detedted_lines.append(line)
        return detedted_lines

    def get_longest_line(self, lines):
        max_line = self.detected_line
        for line in lines:
            if max_line.length < line.length:
                max_line = line
        return max_line

    def do_detecting(self):
        diff = self.get_difference(
            self.__before_drawline_image, self.__after_drawline_image)
        white = self.get_white(self.__after_drawline_image)
        same = self.get_same_part(diff, white)
        edge = self.detect_edge(same)
        """
        self.save_picture(
            [self.__before_drawline_image,
             self.__after_drawline_image,
             diff, white, same, edge])
        """
        if edge is not None:
            lines = self.detect_line(edge)
            line = self.get_longest_line(lines)
            return line
        else:
            print('No lines')

    def save_picture(self, pic_list):
        date = dt.now().strftime('%Y-%m-%d-%H-%M-%S')
        for i, picture in enumerate(pic_list):
            cv2.imwrite('images/' + str(date) + '-' + str(i), picture)
