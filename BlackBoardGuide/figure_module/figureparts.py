# 図形描画のパーツ管理モジュール
# 点、円、線のクラスを保持
# 文字クラスとかも作る予定～

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
    def __init__(self, start=Point(-1, -1), end=Point(-1, -1)):
        self.start = start
        self.end = end
        self.length = math.sqrt(
            (self.end.X - self.start.X) ** 2 + (self.end.Y - self.start.Y) ** 2)
        self.middle_point = Point(
            (self.end.X + self.start.X) / 2,
            (self.end.Y + self.start.Y) / 2)
        self.angle_rad = math.atan2(
            self.end.Y - self.start.Y,
            self.end.X - self.start.X)
        self.angle_deg = math.degrees(self.angle_rad)

    def make_from_radian(self, middle_point, rad, length):
        self.length = length
        self.middle_point = middle_point
        self.angle_rad = rad
        self.angle_deg = math.degrees(self.angle_rad)
        self.start = Point(
            middle_point.X - math.cos(rad) * (length / 2),
            middle_point.Y - math.sin(rad) * (length / 2))
        self.end = Point(
            middle_point.X + math.cos(rad) * (length / 2),
            middle_point.Y + math.sin(rad) * (length / 2))

    def change_coordinate_point(self, x, y, start_or_end):
        if start_or_end == 'start':
            self.start.change_coordinate(x, y)
        elif start_or_end == 'end':
            self.end.change_coordinate(x, y)

        self.length = math.sqrt(
            (self.end.X - self.start.X) ** 2 + (self.end.Y - self.start.Y) ** 2)
        self.middle_point = Point(
            (self.end.X - self.start.X) / 2,
            (self.end.Y - self.start.Y) / 2)
        self.angle_rad = math.atan2(
            self.end.Y - self.start.Y,
            self.end.X - self.start.X)
        self.angle_deg = math.degrees(self.angle_rad)

    def get_start(self):
        return (self.start.X, self.start.Y)

    def get_end(self):
        return (self.end.X, self.end.Y)
