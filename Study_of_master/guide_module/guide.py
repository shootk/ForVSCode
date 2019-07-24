import math
import cv2


class Point():
    def __init__(self, x=0, y=0):
        self.X = x
        self.Y = y

    def change_coordinate(self, x, y):
        self.X = x
        self.Y = y


class Circle():
    def __init__(self, center=Point(0, 0), radius=10):
        self.center = center
        self.radius = radius


class Line():
    def __init__(self, start=Point(0, 0), end=Point(0, 0)):
        self.start = start
        self.end = end
        self.length = math.sqrt(
            (self.end.X - self.start.X) ** 2 + (self.end.Y - self.start.Y))
        self.middle_point = Point(
            (self.end.X - self.start.X) / 2, (self.end.Y - self.start.Y) / 2)
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


class FigureGuide():
    def __init__(self, width=640, height=480):
        self.line = Line(Point(width * 0.25, height / 2),
                         Point(width * 0.75, height / 2))
        self.make_guide()

    def set_line(self, start, end):
        self.line = Line(start, end)
        self.make_guide()

    def make_guide(self):
        self.lines = []
        self.circles = []

        self.vertical_bisector = Line()
        self.vertical_bisector.make_from_radian(
            self.line.middle_point,
            self.line.angle_rad + math.radians(90),
            self.line.length * 3)

        self.lines.append(self.vertical_bisector)

        self.vertical_line_1 = Line()

        self.vertical_line_1.make_from_radian(
            self.line.start,
            self.line.angle_rad + math.radians(90),
            self.line.length * 3)
        self.lines.append(self.vertical_line_1)

        self.vertical_line_2 = Line()

        self.vertical_line_2.make_from_radian(
            self.line.end,
            self.line.angle_rad + math.radians(90),
            self.line.length * 3)
        self.lines.append(self.vertical_line_2)

        self.middle_circle = Circle(
            self.line.middle_point, self.line.length / 2)
        self.circles.append(self.middle_circle)

        self.left_circle = Circle(self.line.start, self.line.length)
        self.circles.append(self.left_circle)

        self.right_circle = Circle(self.line.end, self.line.length)
        self.circles.append(self.right_circle)

    def draw_guide(self, img):
        for line in self.lines:
            start = (line.start.X, line.start.Y)
            end = (line.end.X, line.end.Y)
            img = cv2.line(img, start, end, (255, 255, 255), 2)

        for circle in self.circles:
            center = (circle.center.X, circle.center.Y)
            radius = circle.radius
            img = cv2.circle(img, center, radius, (255, 255, 255), 2)
