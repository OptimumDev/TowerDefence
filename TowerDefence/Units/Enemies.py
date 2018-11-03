from PyQt5.QtGui import QPixmap
from Units.Unit import Unit
from Directions import Directions


class Enemy(Unit):

    STEPS = 5

    def __init__(self, max_health, route, damage, steps_for_cell, images_directory):
        super().__init__(route[0], QPixmap('images/soldier1.png'))
        self.images_directory = images_directory
        self.images = self.get_image_dictionary()
        self.current_direction = Directions.Right
        self.current_image = 0
        self.__health = max_health
        self.__route = route
        self.__current_route_point = 0
        self.__damage = damage
        self.steps_for_cell = steps_for_cell

    def get_image_dictionary(self):
        image_dictionary = {}
        for direction in [Directions.Right, Directions.Left, Directions.Up, Directions.Down]:
            image_dictionary[direction] = [QPixmap(f'images/{self.images_directory}/{direction}/1.png'),
                                           QPixmap(f'images/{self.images_directory}/{direction}/2.png'),
                                           QPixmap(f'images/{self.images_directory}/{direction}/3.png'),
                                           QPixmap(f'images/{self.images_directory}/{direction}/4.png'),
                                           QPixmap(f'images/{self.images_directory}/{direction}/5.png')]
        return image_dictionary

    @property
    def image(self):
        self.current_image = (self.current_image + 4 / self.steps_for_cell) % self.STEPS
        return self.images[self.current_direction][int(self.current_image)]

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
            self.current_direction = direction.convert_to_direction()
            step = direction / self.steps_for_cell
            self._coordinates = self.coordinates + step
            if self.coordinates == self.__route[self.__current_route_point + 1]:
                self.__current_route_point += 1


class Orc(Enemy):

    MAX_HEALTH = 25
    DAMAGE = 5
    STEPS_FOR_CELL = 40
    IMAGES_DIRECTORY = "orcs"

    def __init__(self, route):
        super().__init__(self.MAX_HEALTH, route, self.DAMAGE, self.STEPS_FOR_CELL, self.IMAGES_DIRECTORY)