import sys
from PyQt5.QtWidgets import QApplication
from Units import Land, Castle, Enemy, Arrow
from Point import Point
from GameWindow import GameWindow


class Game:

    def __init__(self, map_file):
        self.__start = Point(0, 0)
        self.__finish = Point(0, 0)

        self.__tick_number = 0

        self.__castle_coordinates = []
        map_size = self.get_map_size(map_file)
        self.game_map = self.get_map(map_file)
        self.__castle_health = 100
        self.castle = self.get_castle()
        self.__map_width = map_size[0]
        self.__map_height = map_size[1]
        self.__enemies_route = self.get_enemies_route()

        self.arrows = []

        self.towers = []
        self.tower_damage = 5
        self.tower_shooting_range = 5
        self.tower_cost = 30

        self.gold = 60

        self.enemies = []
        self.enemies_to_add = 3
        self.__enemies_add_interval = 35
        self.__enemies_add_ticks = 0
        self.__enemies_health = 30
        self.__enemies_damage = 5
        self.__enemy_gold = 10

        self.__units_turn_ticks_interval = 20

    def get_map_size(self, map_file):
        with open(map_file) as game_map:
            lines = game_map.readlines()
            map_width = len(lines[0]) - 1
            map_height = len(lines)
            return (map_width, map_height)

    def get_map(self, map_file):
        result = []
        with open(map_file) as game_map:
            y = 0
            for line in game_map.readlines():
                x = 0
                for letter in line:
                    if letter == 's':
                        self.__start = Point(x, y)
                    if letter == 'f':
                        self.__finish = Point(x, y)
                    if letter == 'c':
                        self.__castle_coordinates.append(Point(x, y))
                    if letter not in 'sfg#':
                        continue
                    result.append(Land(letter in '#sf', Point(x, y)))
                    x += 1
                y += 1
        return result

    def get_enemies_route(self):
        road = [land.coordinates for land in self.game_map if land.is_road]
        route = [self.__start]
        visited = [self.__start]
        while route[-1] != self.__finish:
            for point in route[-1].get_nearby_points():
                if point.x < 0 or point.x > self.__map_width or point.y < 0 or point.y > self.__map_height:
                    continue
                if point in road and point not in visited:
                    route.append(point)
                    visited.append(point)
        return route

    def get_castle(self):
        self.__castle_coordinates.sort()
        coordinates = self.__castle_coordinates[1]
        return Castle(coordinates, self.__castle_health)

    @property
    def is_units_turn(self):
        return self.__tick_number % self.__units_turn_ticks_interval == 0

    def add_enemy(self):
        self.enemies.append(Enemy(self.__enemies_health, self.__enemies_route, self.__enemies_damage))
        self.enemies_to_add -= 1

    def update(self):
        self.__tick_number += 1

        for enemy in self.enemies:
            if not enemy.is_alive:
                self.enemies.remove(enemy)
                self.gold += self.__enemy_gold
            if enemy.got_to_route_end:
                self.castle.get_damage(enemy.damage)
                self.enemies.remove(enemy)
            else:
                if self.is_units_turn:
                    enemy.move()

        for arrow in self.arrows:
            if arrow.got_to_enemy:
                self.arrows.remove(arrow)
            else:
                arrow.move()

        if self.is_units_turn:
            for tower in self.towers:
                for enemy in self.enemies:
                    if tower.try_to_shoot(enemy):
                        self.arrows.append(Arrow(tower.coordinates, enemy, self.tower_damage))
                        break

        if self.enemies_to_add > 0:
            if self.__enemies_add_ticks == 0:
                self.add_enemy()
                self.__enemies_add_ticks = self.__enemies_add_interval
            else:
                self.__enemies_add_ticks -= 1


if __name__ == '__main__':
    currentExitCode = GameWindow.EXIT_CODE_REBOOT
    while currentExitCode == GameWindow.EXIT_CODE_REBOOT:
        app = QApplication(sys.argv)
        window = GameWindow(Game('map.txt'))
        currentExitCode = app.exec_()
        app = None
    sys.exit(currentExitCode)
