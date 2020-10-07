"""
ガイド作成用
ガイドのパーツ設定、作成（座標等の情報をreturn）をするモジュールとして使用
"""

import math
from figureparts import Line, Circle, TextBox
from define_property import define_property


class FigureGuideMaker():
    def set_parts(self, base_line):
        self.__lines = {}
        self.__circles = {}

        perpendicular_bisector = Line()
        perpendicular_bisector.make_from_radian(
            base_line.middle_point,
            base_line.angle_rad + math.radians(90),
            base_line.length * 3)
        self.__lines['bisector'] = perpendicular_bisector

        perpendicular_line_L = Line()
        perpendicular_line_L.make_from_radian(
            base_line.start,
            base_line.angle_rad + math.radians(90),
            base_line.length * 3)
        self.__lines['perpendicular_L'] = perpendicular_line_L

        perpendicular_line_R = Line()
        perpendicular_line_R.make_from_radian(
            base_line.end,
            base_line.angle_rad + math.radians(90),
            base_line.length * 3)
        self.__lines['perpendicular_R'] = perpendicular_line_R

        middle_circle = Circle(
            base_line.middle_point, base_line.length / 2)
        self.__circles['middle'] = middle_circle

        left_circle = Circle(base_line.start, base_line.length)
        self.__circles['left'] = left_circle

        right_circle = Circle(base_line.end, base_line.length)
        self.__circles['right'] = right_circle

    def get_parts(self, line, linear_parts, circlear_parts):
        self.set_parts(line)

        return_lines = []
        return_circles = []

        for key in linear_parts:
            return_lines.append(self.__lines[key])

        for key in circlear_parts:
            return_circles.append(self.__circles[key])
        return return_lines, return_circles


class FigureGuide():
    def __init__(self):
        self.__guide_mode = {}
        define_property(self, name='line', value=Line())
        self._set_guide_mode()
        self.__maker = FigureGuideMaker()

    @property
    def guide_mode(self):
        return self.__guide_mode

    def _set_guide_mode(self):
        self.__guide_mode['no'] = ([], [])
        """
        ガイドを一括表示のみにするためコメントアウト
        必要になり次第コメント解除
        self.__guide_mode['isosceles_triangle'] = (
            ['bisector'], ['left', 'right'])

        self.__guide_mode['right_triangle'] = (
            ['perpendicular_L', 'perpendicular_R'], ['middle'])

        self.__guide_mode['rectangle'] = (
            ['perpendicular_L', 'perpendicular_R'], [])

        self.__guide_mode['circle'] = (
            [], ['left', 'right'])
        """
        self.__guide_mode['all'] = (
            ['bisector', 'perpendicular_L', 'perpendicular_R'],
            ['left', 'right', 'middle'])

    def get_guide(self, guide_key):
        return self.__maker.get_parts(
            self.line, self.__guide_mode[guide_key][0], self.__guide_mode[guide_key][1])


class TextGuideMaker():
    def set_parts(self, base_text_box):
        self.__lines = {}

        left_vertical_line = Line()
        left_vertical_line.make_from_radian(
            base_text_box.bottom.start,
            base_text_box.angle_rad + math.radians(90),
            base_text_box.width * 2)
        self.__lines['left_vertical_line'] = left_vertical_line

        center_vertical_line = Line()
        center_vertical_line.make_from_radian(
            base_text_box.bottom.middle_point,
            base_text_box.angle_rad + math.radians(90),
            base_text_box.width * 2)
        self.__lines['center_vertical_line'] = center_vertical_line

        right_vertical_line = Line()
        right_vertical_line.make_from_radian(
            base_text_box.bottom.end,
            base_text_box.angle_rad + math.radians(90),
            base_text_box.width * 2)
        self.__lines['right_vertical_line'] = right_vertical_line

        top_horizontal_line = Line()
        top_horizontal_line.make_from_radian(
            base_text_box.right.start,
            base_text_box.angle_rad,
            base_text_box.width * 2)
        self.__lines['top_horizontal_line'] = top_horizontal_line

        center_horizontal_line = Line()
        center_horizontal_line.make_from_radian(
            base_text_box.right.middle_point,
            base_text_box.angle_rad,
            base_text_box.width * 2)
        self.__lines['center_horizontal_line'] = center_horizontal_line

        bottom_horizontal_line = Line()
        bottom_horizontal_line.make_from_radian(
            base_text_box.right.end,
            base_text_box.angle_rad,
            base_text_box.width * 2)
        self.__lines['bottom_horizontal_line'] = bottom_horizontal_line

    def get_parts(self, box, linear_parts):
        self.set_parts(box)

        return_lines = []

        for key in linear_parts:
            return_lines.append(self.__lines[key])

        return return_lines


class TextGuide():
    def __init__(self):
        define_property(self, name='text_box',
                        value=TextBox((0, 0), (0, 0), text=''))
        self.__guide_mode = {}
        self._set_guide_mode()
        self.__maker = TextGuideMaker()

    @property
    def guide_mode(self):
        return self.__guide_mode

    def _set_guide_mode(self):
        self.__guide_mode['no'] = ([],)
        """
        self.__guide_mode['vertical_all'] = (
            ['left_vertical_line', 'center_vertical_line', 'right_vertical_line'],)
        self.__guide_mode['horizontal_all'] = (
            ['top_horizontal_line', 'center_horizontal_line', 'bottom_horizontal_line'],)
        self.__guide_mode['vertical_simple'] = (
            ['center_vertical_line'],)
        self.__guide_mode['horizontal_simple'] = (
            ['center_horizontal_line'],)
        """
        self.__guide_mode['all'] = (
            ['left_vertical_line', 'center_vertical_line', 'right_vertical_line',
             'top_horizontal_line', 'center_horizontal_line', 'bottom_horizontal_line'],)

    def get_guide(self, guide_key):
        return self.__maker.get_parts(
            self.text_box, self.__guide_mode[guide_key][0])
