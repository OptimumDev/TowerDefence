from PyQt5.QtGui import QPixmap
from Units.Unit import Unit
from Units.Projectiles import Arrow


class Tower(Unit):

    def __init__(self, coordinates, shooting_range, shooting_rate, cost, image):
        super().__init__(coordinates, image)
        self.__shooting_range = shooting_range
        self.shooting_rate = shooting_rate
        self.current_tick = 0
        self.cost = cost

    @property
    def time_to_shoot(self):
        return self.current_tick % self.shooting_rate == 0

    def is_able_to_shoot(self, target_coordinates):
        return self._coordinates.get_distance(target_coordinates) < self.__shooting_range

    def try_to_shoot(self, target):
        if self.is_able_to_shoot(target.coordinates):
            return True
        return False

    def update(self):
        self.current_tick += 1


class ArrowTower(Tower):

    SHOOTING_RANGE = 5
    SHOOTING_RATE = 40
    COST = 30
    NAME = 'Arrow Tower'

    def __init__(self, coordinates):
        super().__init__(coordinates, self.SHOOTING_RANGE, self.SHOOTING_RATE, self.COST, QPixmap('images/tower.png'))

    def get_projectile(self, target):
        return Arrow(self.coordinates, target)