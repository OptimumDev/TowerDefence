from PyQt5.QtGui import QPixmap
from Units.Unit import Unit


class Castle(Unit):
    def __init__(self, coordinates, health):
        super().__init__(coordinates, QPixmap('images/castle.png'))
        self.__health = health

    def get_damage(self, damage):
        self.__health -= damage

    @property
    def health(self):
        return self.__health

    @property
    def is_alive(self):
        return self.__health > 0