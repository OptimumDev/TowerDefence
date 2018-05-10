import sys
from PyQt5.QtWidgets import QApplication
from Units import Land, Castle
from Point import Point
from GameWindow import GameWindow


class Game:

    def __init__(self, map_file):
        self.__start = Point(0, 0)
        self.__finish = Point(0, 0)

        self.__castle_coordinates = []
        map_size = self.get_map_size(map_file)
        self.__game_map = self.get_map(map_file)
        self.__castle_health = 100
        self.__castle = self.get_castle()
        self.__map_width = map_size[0]
        self.__map_height = map_size[1]
        self.__enemies_route = self.get_enemies_route()

    @property
    def game_map(self):
        return self.__game_map

    @property
    def enemies_route(self):
        return self.__enemies_route

    @property
    def castle(self):
        return self.__castle

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
        road = [land.coordinates for land in self.__game_map if land.is_road]
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


if __name__ == '__main__':
    currentExitCode = GameWindow.EXIT_CODE_REBOOT
    while currentExitCode == GameWindow.EXIT_CODE_REBOOT:
        app = QApplication(sys.argv)
        window = GameWindow(Game('map.txt'))
        currentExitCode = app.exec_()
        app = None
    sys.exit(currentExitCode)
