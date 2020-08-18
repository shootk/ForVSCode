# 図形描画のパーツ管理モジュール
# 点、円、線のクラスを保持
# 文字クラスとかも作る予定～

import math


class Point():
    def __init__(self, x=0, y=0):
        self.__coordinate = (int(x), int(y))

    @property
    def coordinate(self):
        return self.__coordinate

    @coordinate.setter
    def coordinate(self, x, y):
        self.__coordinate = (int(x), int(y))

    @property
    def X(self):
        return self.__coordinate[0]

    @X.setter
    def X(self, x):
        self.__coordinate[0] = x

    @property
    def Y(self):
        return self.__coordinate[1]

    @Y.setter
    def Y(self, y):
        self.__coordinate[1] = y


class Circle():
    def __init__(self, center=Point(), radius=10):
        self.__center = center
        self.radius = int(radius)

    @property
    def center(self):
        return self.__center

    @center.setter
    def center(self, point):
        if type(point) == Point:
            self.__center = point
        else:
            raise TypeError('Point required. Get ', type(point))


class Line():
    def __init__(self, start=Point(), end=Point()):
        self.__start = start
        self.__end = end
        self.__length = math.sqrt(
            (self.__end.X - self.__start.X) ** 2 + (self.__end.Y - self.__start.Y) ** 2)
        self.__middle_point = Point(
            (self.__end.X + self.__start.X) / 2,
            (self.__end.Y + self.__start.Y) / 2)
        self.__angle_rad = math.atan2(
            self.__end.Y - self.__start.Y,
            self.__end.X - self.__start.X)
        self.__angle_deg = math.degrees(self.__angle_rad)

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, point):
        if type(point) == Point:
            self.__start = point
        else:
            raise TypeError('Point required. Get ', type(point))

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, point):
        if type(point) == Point:
            self.__end = point
        else:
            raise TypeError('Point required. Get ', type(point))

    @property
    def middle_point(self):
        return self.__middle_point

    @property
    def length(self):
        return self.__length

    @property
    def angle_rad(self):
        return self.__angle_rad

    @property
    def angle_deg(self):
        return self.__angle_deg

    def make_from_radian(self, middle_point, rad, length):
        self.__length = length
        self.__middle_point = middle_point
        self.__angle_rad = rad
        self.__angle_deg = math.degrees(self.__angle_rad)
        self.__start = Point(
            middle_point.X - math.cos(rad) * (length / 2),
            middle_point.Y - math.sin(rad) * (length / 2))
        self.__end = Point(
            middle_point.X + math.cos(rad) * (length / 2),
            middle_point.Y + math.sin(rad) * (length / 2))

    def change_coordinate_point(self, x, y, start_or_end):
        if start_or_end == 'start':
            self.__start.coordinate(x, y)
        elif start_or_end == 'end':
            self.__end.coordinate(x, y)

        self.__length = math.sqrt(
            (self.__end.X - self.__start.X) ** 2 + (self.__end.Y - self.__start.Y) ** 2)
        self.__middle_point = Point(
            (self.__end.X - self.__start.X) / 2,
            (self.__end.Y - self.__start.Y) / 2)
        self.__angle_rad = math.atan2(
            self.__end.Y - self.__start.Y,
            self.__end.X - self.__start.X)
        self.__angle_deg = math.degrees(self.__angle_rad)

    def get_start(self):
        return (self.__start.X, self.__start.Y)

    def get_end(self):
        return (self.__end.X, self.__end.Y)
