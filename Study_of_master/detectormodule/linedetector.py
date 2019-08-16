import cv2
import numpy as np
from guidemodule import guide


class LineDitector():
    def __init__(self, width=640, height=480, color=(200, 200, 200)):

        self.before_drawline_image = np.zeros((width, height), dtype=np.uint8)
        self.after_drawline_image = np.zeros((width, height), dtype=np.uint8)
        self.detected_line = guide.Line()
        self.ditect_low_white = color - (30, 30, 30)
        self.ditect_high_white = color + (30, 30, 30)

    def SetSrcImage(self, img):
        self.before_drawline_image = img

    def SetDstImage(self, img):
        self.after_drawline_image = img

    def Queue(self, img):
        self.before_drawline_image = self.after_drawline_image
        self.after_drawline_image = img

    def GetDifference(self, src1_image, src2_image):
        diff = cv2.absdiff(src1_image, src2_image)
        return cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    def GetWhite(self, src_image):
        return cv2.inRange(src_image, self.ditect_low_white, self.ditect_high_white)

    def GetSamePart(self, src1_image, src2_image):
        return cv2.bitwise_and(src1_image, src2_image)

    def DetectEdge(self, src_image):
        return cv2.Canny(src_image, 70, 100, 30)

    def DetectLine(self, src_image):
        lines = cv2.HoughLinesP(src_image, 1, np.pi / 180, 40, 10, 100)
        detedted_lines = []
        for x1, y1, x2, y2 in lines[0]:
            line = guide.Line(guide.Point(x1, y1), guide.Point(x2, y2))
            detedted_lines.append(line)
        return detedted_lines

    def GetLongestLine(self, lines):
        max_line = self.detected_line
        for line in lines:
            if max_line.length < line.length:
                max_line = line
        return max_line

    def SetColor(self, color):
        self.ditect_low_white = color - (30, 30, 30)
        self.ditect_high_white = color + (30, 30, 30)