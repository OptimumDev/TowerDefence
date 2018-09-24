from PyQt5.QtGui import QPixmap
from Units.Unit import Unit


class Land(Unit):
    def __init__(self, is_road, coordinates):
        self.__is_road = is_road
        image = QPixmap('images/road.png') if is_road else QPixmap('images/grass.png')
        super().__init__(coordinates, image)

    @property
    def is_road(self):
        return self.__is_road