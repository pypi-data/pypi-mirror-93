import numpy as np
import math
from numpy.linalg import norm
from math import cos, sin

from .dbnamedtuple import DbNamedTuple


class Point(DbNamedTuple):
    x: float
    y: float

    def distance(self, b: 'Point'):
        """

            :param self:
            :param b:
            :return: distance between points a and b
            """
        return norm(np.array(b)-np.array(self))

    def rotate(self, reference_point: 'Point', angle: float) -> 'Point':
        """
            rotates self object around the reference (counterclockwise)
            :param reference_point: reference point
            :param angle: angle in radians
            :return: rotated point
        """
        c = np.array(self) - np.array(reference_point)
        x2 = cos(angle) * c[0] - sin(angle) * c[1]
        y2 = sin(angle) * c[0] + cos(angle) * c[1]
        return Point(x2+reference_point.x, y2+reference_point.y)

    def move(self, movement_vector: 'Point') -> 'Point':
        """

        :param movement_vector:
        :return: Point
        """
        return Point(*(np.array(self) + np.array(movement_vector)))

    def move_x(self, x: float):
        """
            adds given value to x direction and returns moved point.
        @param x:
        @return:
        """
        return Point(self.x + x, self.y)

    def move_y(self, y: float):
        """
            adds given value to y direction and returns moved point.
        @param y:
        @return:
        """
        return Point(self.x, self.y + y)

    def angle(self, b: 'Point') -> float:
        """
        returns the angle between point b and the x axis of self
        :param b:
        :return: angle in radians
        """
        v = np.array(b) - np.array(self)
        return math.atan2(v[1], v[0])

    def x_mirror(self, reference_point: 'Point') -> 'Point':
        """
        :param reference_point:
        :return:
        """
        return Point(2 * reference_point.x - self.x, self.y)

    def y_mirror(self, reference_point: 'Point') -> 'Point':
        """
        :param reference_point:
        :return:
        """
        return Point(self.x, 2*reference_point.y - self.y)

    def x_y_mirror(self, reference_point: 'Point') -> 'Point':
        """
        :param reference_point:
        :return:
        """
        return Point(2 * reference_point.x - self.x, 2 * reference_point.y - self.y)

    # TODO think about dropping support
    def get_p(self) -> tuple:
        """
            function returns a list with all points of the object
            :return:
        """
        return tuple([Point(*self)])

