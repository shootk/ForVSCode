"""
ガイド作成用
ガイドのパーツ設定、作成（座標等の情報をreturn）をするモジュールとして使用
"""

import math
from figureparts import Line, Circle


class GuideMaker():
    def set_parts(self, base_line):
        self.lines = {}
        self.circles = {}

        self.vertical_bisector = Line()
        self.vertical_bisector.make_from_radian(
            base_line.middle_point,
            base_line.angle_rad + math.radians(90),
            base_line.length * 3)
        self.lines['bisector'] = self.vertical_bisector

        self.vertical_line_1 = Line()
        self.vertical_line_1.make_from_radian(
            base_line.start,
            base_line.angle_rad + math.radians(90),
            base_line.length * 3)
        self.lines['vertical_L'] = self.vertical_line_1

        self.vertical_line_2 = Line()
        self.vertical_line_2.make_from_radian(
            base_line.end,
            base_line.angle_rad + math.radians(90),
            base_line.length * 3)
        self.lines['vertical_R'] = self.vertical_line_2

        self.middle_circle = Circle(
            base_line.middle_point, base_line.length / 2)
        self.circles['middle'] = self.middle_circle

        self.left_circle = Circle(base_line.start, base_line.length)
        self.circles['left'] = self.left_circle

        self.right_circle = Circle(base_line.end, base_line.length)
        self.circles['right'] = self.right_circle

    def get_parts(self, line, linear_parts, circlear_parts):
        self.set_parts(line)

        return_lines = []
        return_circles = []

        for key in linear_parts:
            return_lines.append(self.lines[key])

        for key in circlear_parts:
            return_circles.append(self.circles[key])
        return return_lines, return_circles


class FigureGuides():
    def __init__(self):
        self.guides_parts = {}
        self.line = Line()
        self.set_guides()
        self.maker = GuideMaker()

    def set_line(self, line):
        self.line = line

    def set_guides(self):
        self.guides_parts['no'] = ([], [])
        """
        ガイドを一括表示のみにするためコメントアウト
        必要になり次第コメント解除
        self.guides_parts['isosceles_triangle'] = (
            ['bisector'], ['left', 'right'])

        self.guides_parts['right_triangle'] = (
            ['vertical_L', 'vertical_R'], ['middle'])

        self.guides_parts['rectangle'] = (
            ['vertical_L', 'vertical_R'], [])

        self.guides_parts['circle'] = (
            [], ['left', 'right'])
        """
        self.guides_parts['all'] = (
            ['bisector', 'vertical_L', 'vertical_R'],
            ['left', 'right', 'middle'])

    def get_guide(self, guide_key):
        return self.maker.get_parts(
            self.line, self.guides_parts[guide_key][0], self.guides_parts[guide_key][1])
