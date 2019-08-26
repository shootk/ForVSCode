import cv2
import numpy as np
from guidemodule import guide


class LineDitector():
    def __init__(self, width=640, height=480, color=(200, 200, 200)):

        self.before_drawline_image = np.zeros((width, height), dtype=np.uint8)
        self.after_drawline_image = np.zeros((width, height), dtype=np.uint8)
        self.detected_line = guide.Line()
        self.ditect_low_white = np.array([
            160, 160, 140])
        self.ditect_high_white = np.array([
            190, 220, 190])

    def SetSrcImage(self, img):
        self.before_drawline_image = img

    def SetDstImage(self, img):
        self.after_drawline_image = img

    def SetColor(self, color):
        self.ditect_low_white = np.array([
            color[0] - (color[0] % 30), color[1] - 30, color[2] - 30])
        self.ditect_high_white = np.array([
            color[0] - (color[0] % 30) + 30, color[1] + 30, color[2] + 30])

    def Queue(self, img):
        self.before_drawline_image = self.after_drawline_image
        self.after_drawline_image = img

    def GetDifference(self, src1_image, src2_image):
        diff = cv2.absdiff(src1_image, src2_image)
        return cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    def GetWhite(self, src_image):
        src_image = cv2.cvtColor(src_image, cv2.COLOR_BGR2HSV_FULL)
        return cv2.inRange(src_image, self.ditect_low_white, self.ditect_high_white)

    def GetSamePart(self, src1_image, src2_image):
        return cv2.bitwise_and(src1_image, src2_image)

    def DetectEdge(self, src_image):
        return cv2.Canny(src_image, 70, 100, 30)

    def DetectLine(self, src_image):
        lines = cv2.HoughLinesP(src_image, rho=1,
                                theta=np.pi / 360, threshold=40, minLineLength=40, maxLineGap=100)
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

    def DoDetecting(self):
        diff = self.GetDifference(
            self.before_drawline_image, self.after_drawline_image)
        white = self.GetWhite(self.after_drawline_image)
        same = self.GetSamePart(diff, white)
        edge = self.DetectEdge(same)
        cv2.imshow('edge', edge)
        if edge is not None:
            lines = self.DetectLine(edge)
            line = self.GetLongestLine(lines)
            return line

        else:
            print('No lines')
