import math


class Point():
    def __init__(self, x=0, y=0):
        self.X = int(x)
        self.Y = int(y)

    def change_coordinate(self, x, y):
        self.X = int(x)
        self.Y = int(y)


class Circle():
    def __init__(self, center=Point(0, 0), radius=10):
        self.center = center
        self.radius = int(radius)

    def get_center(self):
        return (self.center.X, self.center.Y)


class Line():
    def __init__(self, start=Point(-2, -2), end=Point(-1, -1)):
        self.start = start
        self.end = end
        self.length = math.sqrt(
            (self.end.X - self.start.X) ** 2 + (self.end.Y - self.start.Y) ** 2)
        self.middle_point = Point(
            (self.end.X + self.start.X) / 2, (self.end.Y + self.start.Y) / 2)
        self.angle_rad = math.atan2(
            self.end.Y - self.start.Y, self.end.X - self.start.X)
        self.angle_deg = math.degrees(self.angle_rad)

    def make_from_radian(self, middle_point, rad, length):
        self.length = length
        self.middle_point = middle_point
        self.angle_rad = rad
        self.angle_deg = math.degrees(self.angle_rad)
        self.start = Point(middle_point.X - math.cos(rad) * (length / 2),
                           middle_point.Y - math.sin(rad) * (length / 2))
        self.end = Point(middle_point.X + math.cos(rad) * (length / 2),
                         middle_point.Y + math.sin(rad) * (length / 2))

    def change_coordinate_point(self, x, y, start_or_end):
        if start_or_end == 'start':
            self.start.change_coordinate(x, y)
        elif start_or_end == 'end':
            self.end.change_coordinate(x, y)

        self.length = math.sqrt(
            (self.end.X - self.start.X) ** 2 + (self.end.Y - self.start.Y) ** 2)
        self.middle_point = Point(
            (self.end.X - self.start.X) / 2, (self.end.Y - self.start.Y) / 2)
        self.angle_rad = math.atan2(
            self.end.Y - self.start.Y, self.end.X - self.start.X)
        self.angle_deg = math.degrees(self.angle_rad)

    def get_start(self):
        return (self.start.X, self.start.Y)

    def get_end(self):
        return (self.end.X, self.end.Y)


class GuideMaker():
    def set_parts(self, line):
        self.lines = {}
        self.circles = {}

        self.vertical_bisector = Line()
        self.vertical_bisector.make_from_radian(
            line.middle_point,
            line.angle_rad + math.radians(90),
            line.length * 3)
        self.lines['bisector'] = self.vertical_bisector

        self.vertical_line_1 = Line()
        self.vertical_line_1.make_from_radian(
            line.start,
            line.angle_rad + math.radians(90),
            line.length * 3)
        self.lines['vertical_L'] = self.vertical_line_1

        self.vertical_line_2 = Line()
        self.vertical_line_2.make_from_radian(
            line.end,
            line.angle_rad + math.radians(90),
            line.length * 3)
        self.lines['vertical_R'] = self.vertical_line_2

        self.middle_circle = Circle(
            line.middle_point, line.length / 2)
        self.circles['middle'] = self.middle_circle

        self.left_circle = Circle(line.start, line.length)
        self.circles['left'] = self.left_circle

        self.right_circle = Circle(line.end, line.length)
        self.circles['right'] = self.right_circle

    def make_guide(self, line, linear_parts, circlear_parts):
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
        self.line = Line(Point(0, 0), Point(0, 0))
        self.set_guides()
        self.maker = GuideMaker()

    def set_line(self, line):
        self.line = line

    def set_guides(self):
        self.guides_parts['no'] = ([], [])
        # self.guides_parts['isosceles_triangle'] = (
#            ['bisector'], ['left', 'right'])

 #       self.guides_parts['right_triangle'] = (
  #          ['vertical_L', 'vertical_R'], ['middle'])

   #     self.guides_parts['rectangle'] = (
    #        ['vertical_L', 'vertical_R'], [])

     #   self.guides_parts['circle'] = (
      #      [], ['left', 'right'])

        self.guides_parts['all'] = (
            ['bisector', 'vertical_L', 'vertical_R'],
            ['left', 'right', 'middle'])

    def get_guide(self, guide_key):
        return self.maker.make_guide(
            self.line, self.guides_parts[guide_key][0], self.guides_parts[guide_key][1])
