from PyQt5.QtGui import QPixmap


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

    def __init__(self, max_health, route, damage):
        super().__init__(route[0], QPixmap('images/soldier.png'))
        self.__health = max_health
        self.__route = route
        self.__current_route_point = 0
        self.__damage = damage
        # self.__step_count = 0
        # self.__steps_for_cell = steps_for_cell

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
        # distance = 0
        if not self.got_to_route_end:
            # if self.__step_count == 0:
            self.__current_route_point += 1
            #    distance = self.__route[self.__current_route_point] - self._coordinates
            # a = distance / self.__steps_for_cell
            # self._coordinates += a
            # self.__step_count = (self.__step_count + 1) % self.__steps_for_cell
            self._coordinates = self.__route[self.__current_route_point]


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
            target.get_damage(self.damage)
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
    def __init__(self, coordinates, enemy):
        super.__init__(coordinates, QPixmap('images/arrow.png'))
