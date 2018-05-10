from math import sqrt


class Point:

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def __copy__(self):
        return Point(self.x, self.y)

    def __str__(self):
        return 'Point({}, {})'.format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.__x += other.x
        self.__y += other.y
        return self

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def convert_to_image_coordinates(self, image_size, shift):
        return Point((self.x + shift) * image_size, (self.y + shift) * image_size)

    def convert_to_cell_coordinates(self, image_size, shift):
        return Point(self.x // image_size - shift, self.y // image_size - shift)

    def get_distance(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def get_nearby_points(self):
        return (Point(self.x - 1, self.y),
                Point(self.x + 1, self.y),
                Point(self.x, self.y - 1),
                Point(self.x, self.y + 1))

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y
