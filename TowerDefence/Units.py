from PyQt5.QtGui import QPixmap, QTransform
from Point import Point
import math


class Unit:

    def __init__(self, coordinates, image):
        self._coordinates = coordinates
        self._image = image

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def image(self):
        return self._image


class Land(Unit):
    def __init__(self, is_road, coordinates):
        self.__is_road = is_road
        image = QPixmap('images/road.png') if is_road else QPixmap('images/grass.png')
        super().__init__(coordinates, image)

    @property
    def is_road(self):
        return self.__is_road


class Enemy(Unit):

    def __init__(self, max_health, route, damage, steps_for_cell):
        super().__init__(route[0], QPixmap('images/soldier1.png'))
        self.__health = max_health
        self.__route = route
        self.__current_route_point = 0
        self.__damage = damage
        self.steps_for_cell = steps_for_cell

    @property
    def health(self):
        return self.__health

    @property
    def damage(self):
        return self.__damage

    @property
    def is_alive(self):
        return self.__health > 0

    @property
    def got_to_route_end(self):
        return self.__current_route_point == len(self.__route) - 1

    def get_damage(self, damage):
        self.__health -= damage

    def move(self):
        if not self.got_to_route_end:
            direction = self.__route[self.__current_route_point + 1] - self.__route[self.__current_route_point]
            step = direction / self.steps_for_cell
            self._coordinates = self.coordinates + step
            if self.coordinates == self.__route[self.__current_route_point + 1]:
                self.__current_route_point += 1


class Tower(Unit):

    def __init__(self, coordinates, damage, shooting_range):
        super().__init__(coordinates, QPixmap('images/tower.png'))
        self.__damage = damage
        self.__shooting_range = shooting_range

    @property
    def damage(self):
        return self.__damage

    def is_able_to_shoot(self, target_coordinates):
        return self._coordinates.get_distance(target_coordinates) < self.__shooting_range

    def try_to_shoot(self, target):
        if type(target) is Enemy and self.is_able_to_shoot(target.coordinates):
            return True
        return False


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


class Arrow(Unit):
    def __init__(self, coordinates, enemy, damage):
        super().__init__(coordinates, QPixmap('images/arrow.png'))
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
