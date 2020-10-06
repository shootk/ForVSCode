# 図形描画のパーツ管理モジュール
# 点、円、線のクラスを保持
# 文字クラスとかも作る予定～

import math
import numpy as np
<<<<<<< HEAD
from define_property import define_property
=======
>>>>>>> e9847fcc13a85bcc0a2dff423fe1c169c245d5fe


class Point():
    def __init__(self, *args):
<<<<<<< HEAD
        if len(args) == 1:
            self.__x = int(args[0][0])
            self.__y = int(args[0][1])
        elif len(args) == 2:
            self.__x = int(args[0])
            self.__y = int(args[1])
        elif len(args) == 0:
            self.__x = 0
            self.__y = 0
        else:
            raise IndexError('Index out of range.', type(args[0]))

    def __add__(self, other):
        return Point(int(self.__x + other[0]),
                     int(self.__y + other[1]))

    def __iadd__(self, other):
        self.__x += int(other[0])
        self.__y += int(other[1])
        return self

    def __sub__(self, other):
        return Point(int(self.__x - other[0]),
                     int(self.__y - other[1]))

    def __isub__(self, other):
        self.__x -= int(other[0])
        self.__y -= int(other[1])
        return self

    def __getitem__(self, idx):
        if idx == 0:
            return self.__x
        elif idx == 1:
            return self.__y
        else:
            raise IndexError('Index out of range.')

    def __setitem__(self, idx, value):
        if idx == 0:
            self.__x = int(value)
        elif idx == 1:
            self.__y = int(value)
        else:
            raise IndexError('Index out of range.')

    def __str__(self):
        return "({0},{1})".format(self.__x, self.__y)

    def __repr__(self):
        return "{}".format(tuple(self.__x, self.__y))

    def __len__(self):
        return 2
=======
        if len(args) == 0:
            self.__coordinate = [0, 0]
        elif len(args) == 1:
            arg = args[0]
            if type(arg) == tuple:
                self.__coordinate = [arg[0], arg[1]]
            elif type(arg) == Point:
                self.__coordinate = [arg.X, arg.Y]
        elif type(args[0]) == int:
            self.__coordinate = [int(args[0]), int(args[1])]
        else:
            self.__coordinate = [0, 0]

    def __add__(self, other):
        if type(other) == tuple:
            return Point(self.__coordinate[0] + other[0],
                         self.__coordinate[1] + other[1])
        elif type(other) == type(self):
            return Point(self.__coordinate[0] + other.X,
                         self.__coordinate[1] + other.Y)

    def __iadd__(self, other):
        if type(other) == tuple:
            self.__coordinate[0] += other[0]
            self.__coordinate[1] += other[1]
        elif type(other) == type(self):
            self.__coordinate[0] += other.X
            self.__coordinate[1] += other.Y
        return self

    def __sub__(self, other):
        if type(other) == tuple:
            return Point(self.__coordinate[0] - other[0],
                         self.__coordinate[1] - other[1])
        elif type(other) == type(self):
            return Point(self.__coordinate[0] - other.X,
                         self.__coordinate[1] - other.Y)

    def __isub__(self, other):
        if type(other) == tuple:
            self.__coordinate[0] -= other[0]
            self.__coordinate[1] -= other[1]
        elif type(other) == type(self):
            self.__coordinate[0] -= other.X
            self.__coordinate[1] -= other.Y
        return self

    def __str__(self):
        return str(tuple(self.__coordinate))

    def __repr__(self):
        return str(tuple(self.__coordinate))
>>>>>>> e9847fcc13a85bcc0a2dff423fe1c169c245d5fe

    @property
    def coordinate(self):
        return self.__x, self.__y

    @coordinate.setter
    def coordinate(self, x, y):
<<<<<<< HEAD
        self.__x = int(x)
        self.__y = int(y)
=======
        self.__coordinate = [int(x), int(y)]
>>>>>>> e9847fcc13a85bcc0a2dff423fe1c169c245d5fe

    @property
    def X(self):
        return self.__x

    @X.setter
    def X(self, x):
        self.__x = int(x)

    @property
    def Y(self):
        return self.__y

    @Y.setter
    def Y(self, y):
        self.__y = int(y)


class Circle():
<<<<<<< HEAD
    def __init__(self, center=(0, 0), radius=10):
        self.__center = Point(center)
        self.__radius = int(radius)

    def __repr__(self):
        return '\n O:' + str(self.__center.coordinate) + ' rad:' + str(self.__radius)
=======
    def __init__(self, center=Point(), radius=10):
        self.__center = Point(center)
        self.__radius = int(radius)
>>>>>>> e9847fcc13a85bcc0a2dff423fe1c169c245d5fe

    @property
    def center(self):
        return self.__center

    @center.setter
    def center(self, point):
<<<<<<< HEAD
        self.__center = Point(point)
=======
        try:
            self.__center = Point(point)
        except TypeError:
            raise TypeError('Require Point or Tuple')
>>>>>>> e9847fcc13a85bcc0a2dff423fe1c169c245d5fe

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, length):
        if type(length) == int or type(length) == float:
            self.__radius = int(length)
        else:
            raise TypeError('Int or Float required. Get ', type(length))


class Line():
    def __init__(self, start=Point(), end=Point()):
<<<<<<< HEAD
        define_property(self, name='start', value=Point(start))
        define_property(self, name='end', value=Point(end))
=======
        self.__start = Point(start)
        self.__end = Point(end)
        self.__length = math.sqrt(
            (self.__end.X - self.__start.X) ** 2 + (self.__end.Y - self.__start.Y) ** 2)
        self.__middle_point = Point(
            (self.__end.X + self.__start.X) / 2,
            (self.__end.Y + self.__start.Y) / 2)
        self.__angle_rad = math.atan2(
            self.__end.Y - self.__start.Y,
            self.__end.X - self.__start.X)
        self.__angle_deg = math.degrees(self.__angle_rad)

    def __repr__(self):
        return '\n' + str(self.__start.coordinate) + ' to ' + str(self.__end.coordinate)

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
>>>>>>> e9847fcc13a85bcc0a2dff423fe1c169c245d5fe

    def __repr__(self):
        return '\n' + str(self.start.coordinate) + ' to ' + str(self.end.coordinate)

    @property
    def middle_point(self):
        return Point(
            (self.end.X + self.start.X) / 2,
            (self.end.Y + self.start.Y) / 2)

    @property
    def length(self):
        return math.sqrt(
            (self.end.X - self.start.X) ** 2 + (self.end.Y - self.start.Y) ** 2)

    @property
    def angle_rad(self):
        x, y = (self.end - self.start).coordinate
        return math.atan2(y, x)

    @property
    def angle_deg(self):
        return math.degrees(self.angle_rad)

    def make_from_radian(self, middle_point, rad, length):
        self.start = Point(
            middle_point.X - math.cos(rad) * (length / 2),
            middle_point.Y - math.sin(rad) * (length / 2))
        self.end = Point(
            middle_point.X + math.cos(rad) * (length / 2),
            middle_point.Y + math.sin(rad) * (length / 2))

<<<<<<< HEAD
=======
    def change_coordinate_point(self, x, y, start_or_end):
        if start_or_end == 'start':
            self.__start.coordinate = (x, y)
        elif start_or_end == 'end':
            self.__end.coordinate = (x, y)

        self.__length = math.sqrt(
            (self.__end.X - self.__start.X) ** 2 + (self.__end.Y - self.__start.Y) ** 2)
        self.__middle_point = Point(
            (self.__end.X + self.__start.X) / 2,
            (self.__end.Y + self.__start.Y) / 2)
        self.__angle_rad = math.atan2(
            self.__end.Y - self.__start.Y,
            self.__end.X - self.__start.X)
        self.__angle_deg = math.degrees(self.__angle_rad)

>>>>>>> e9847fcc13a85bcc0a2dff423fe1c169c245d5fe
    def get_start(self):
        return self.start.coordinate

    def get_end(self):
        return self.end.coordinate


class Box():
    def __init__(self, *args):
        self.__corner = []
        self.__lines = []
        if len(args) == 2:
<<<<<<< HEAD
            self.make_from_two_points(args[0], args[1])
        elif len(args) == 3:
            self.make_from_two_points(args[0], (args[1], args[2]))
        elif len(args) == 4:
            self.make_from_points(args[0], args[1], args[2], args[3])
=======
            self.make_from_two_points(args)
        elif len(args) == 3:
            self.make_from_two_points(args[0], (args[1], args[2]))
        elif len(args) == 4:
            self.make_from_points(args)
>>>>>>> e9847fcc13a85bcc0a2dff423fe1c169c245d5fe
        else:
            raise TypeError('No required item.')
        self.__set_line(self.__corner)

    def __str__(self):
        return 'corner:' + str(self.__corner) + '\ncenter:' + str(self.center)

    @property
    def corner(self):
        return self.__corner

    @corner.setter
    def corner(self, *args):
<<<<<<< HEAD
        if len(args[0]) == 4 and len(args[0][3]) == 2:
            for i, arg in enumerate(args[0]):
                self.__corner[i] = Point(arg)
=======
        print(len(args[0]), args[0], args[0][-1])
        if len(args[0]) == 4 and len(args[0][3]) == 2:
            for i, arg in enumerate(args[0]):
                self.__corner[i] = Point(arg[0], arg[1])
>>>>>>> e9847fcc13a85bcc0a2dff423fe1c169c245d5fe
        elif len(args[0]) > 0:
            for i, corner_num in enumerate(args[0][-1]):
                self.__corner[corner_num] = Point(args[0][i])
        else:
            raise TypeError('None')
        self.__set_line(self.__corner)

    def __getitem__(self, idx):
        return self.__corner[idx]

    def __setitem__(self, idx, value):
        self.__corner[idx] = Point(value)
        self.__set_line(self.__corner)

    @property
    def asarray(self):
        return np.array([Point(point).coordinate for point in self.__corner])

    @property
<<<<<<< HEAD
    def asrearray(self):
        return np.array([Point(self.__corner[0]).coordinate, Point(self.__corner[3]).coordinate,
                         Point(self.__corner[2]).coordinate, Point(self.__corner[1]).coordinate])

    @property
=======
>>>>>>> e9847fcc13a85bcc0a2dff423fe1c169c245d5fe
    def lines(self):
        return self.__lines

    @property
<<<<<<< HEAD
    def top(self):
        return self.__lines[0]

    @property
    def right(self):
        return self.__lines[1]

    @property
    def bottom(self):
        return self.__lines[2]

    @property
    def left(self):
        return self.__lines[3]

    @property
=======
>>>>>>> e9847fcc13a85bcc0a2dff423fe1c169c245d5fe
    def width(self):
        x1 = self.__corner[1].X - self.__corner[0].X
        x2 = self.__corner[2].X - self.__corner[3].X
        if x1 == x2:
            return x1
        return None

    @property
    def height(self):
        y1 = self.__corner[3].Y - self.__corner[0].Y
        y2 = self.__corner[2].Y - self.__corner[1].Y
        if y1 == y2:
            return y1
        return None

    @property
    def center(self):
        x_sum, y_sum = 0, 0
        for point in self.__corner:
            x_sum += point.X
            y_sum += point.Y
        return Point(int(x_sum / 4), int(y_sum / 4))

<<<<<<< HEAD
    @property
    def angle_rad(self):
        if self.height is not None:
            return math.atan2(
                self.__corner[0].Y - self.__corner[1].Y,
                self.__corner[0].X - self.__corner[1].X)
        return None

    def make_from_two_points(self, *args):
        top_left_pt = Point(args[0])
        bottom_right_pt = Point(args[1])
=======
    def make_from_two_points(self, *args):
        top_left_pt = Point(args[0][0])
        bottom_right_pt = Point(args[0][1])
>>>>>>> e9847fcc13a85bcc0a2dff423fe1c169c245d5fe
        top_right_pt = Point(bottom_right_pt.X, top_left_pt.Y)
        bottom_left_pt = Point(top_left_pt.X, bottom_right_pt.Y)
        self.__corner = [top_left_pt, top_right_pt,
                         bottom_right_pt, bottom_left_pt]

    def make_from_points(self, *args):
        self.__corner = [Point(point) for point in args[0]]
        self.__set_line()

    def __set_line(self, corner):
        for i in range(4):
            self.__lines = [
                Line(corner[i], corner[(i + 1) % 4]) for i in range(4)]
<<<<<<< HEAD


class TextBox(Box):
    def __init__(self, *args, text):
        super().__init__(*args)
        define_property(self, name='text', value=text)
=======
>>>>>>> e9847fcc13a85bcc0a2dff423fe1c169c245d5fe
