from PyQt5.QtGui import QPixmap, QTransform
from Units.Unit import Unit
from Point import Point
import math


class Projectile(Unit):
    def __init__(self, coordinates, enemy, damage, image):
        super().__init__(coordinates, image)
        self.initial_image = self.image
        self.enemy = enemy
        self.damage = damage
        self.dealt_damage = False
        self.rotate()

    ENEMY_RADIUS = Point(0, 0)

    @property
    def enemy_coordinates(self):
        return self.enemy.coordinates + self.ENEMY_RADIUS

    @property
    def got_to_enemy(self):
        return self.coordinates == self.enemy_coordinates

    def rotate(self):
        angle = math.atan2(self.coordinates.y - self.enemy_coordinates.y,
                           self.coordinates.x - self.enemy_coordinates.x)
        transform = QTransform().rotate(-90 + angle * 180 / math.pi)
        self._image = self.initial_image.transformed(transform)

    def move(self):
        self.rotate()
        dif = self.enemy_coordinates - self.coordinates
        self._coordinates = self.coordinates + dif.normalize() / 20
        if not self.dealt_damage and self.got_to_enemy:
            self.enemy.get_damage(self.damage)
            self.dealt_damage = True


class Arrow(Projectile):

    DAMAGE = 5

    def __init__(self, coordinates, enemy):
        super().__init__(coordinates, enemy, self.DAMAGE, QPixmap('images/arrow.png'))