from Units import Land, Castle, Enemy, Arrow, Tower
from Point import Point


class Game:

    CASTLE_HEALTH = 100

    TOWER_DAMAGE = 5
    TOWER_RANGE = 5
    TOWER_COST = 30

    ENEMY_ADD_INTERVAL = 35
    ENEMY_HEALTH = 30
    ENEMY_DAMAGE = 5
    ENEMY_GOLD = 10

    UNITS_TURN_INTERVAL = 20

    def __init__(self, map_file):
        self.__start = Point(0, 0)
        self.__finish = Point(0, 0)

        self.__tick_number = 0

        map_size = self.get_map_size(map_file)
        self.game_map = self.get_map(map_file)
        self.castle = self.get_castle()
        self.__map_width = map_size[0]
        self.__map_height = map_size[1]
        self.__enemies_route = self.get_enemies_route()

        self.arrows = []

        self.towers = []
        self.gold = 60

        self.enemies = []
        self.enemies_to_add = 1
        self.__enemies_add_ticks = 0

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
        coordinates = self.__finish + Point(1, -2)
        return Castle(coordinates, self.CASTLE_HEALTH)

    @property
    def is_units_turn(self):
        return self.__tick_number % self.UNITS_TURN_INTERVAL == 0

    def add_enemy(self):
        self.enemies.append(Enemy(self.ENEMY_HEALTH, self.__enemies_route, self.ENEMY_DAMAGE, self.UNITS_TURN_INTERVAL))
        self.enemies_to_add -= 1

    @property
    def able_to_build_tower(self):
        return self.gold >= self.TOWER_COST

    def build_tower(self, coordinates):
        self.towers.append(Tower(coordinates, self.TOWER_DAMAGE, self.TOWER_RANGE))
        self.gold -= self.TOWER_COST

    def check_enemies(self):
        for enemy in self.enemies:
            if not enemy.is_alive:
                self.enemies.remove(enemy)
                self.gold += self.ENEMY_GOLD
            elif enemy.got_to_route_end:
                self.castle.get_damage(enemy.damage)
                self.enemies.remove(enemy)

    def arrows_turn(self):
        for arrow in self.arrows:
            if arrow.got_to_enemy:
                self.arrows.remove(arrow)
            else:
                arrow.move()

    def enemies_turn(self):
        for enemy in self.enemies:
            enemy.move()

    def towers_turn(self):
        for tower in self.towers:
            for enemy in self.enemies:
                if tower.try_to_shoot(enemy):
                    self.arrows.append(Arrow(tower.coordinates, enemy, self.TOWER_DAMAGE))
                    break

    def units_turn(self):
        self.enemies_turn()
        if self.is_units_turn:
            self.towers_turn()

    def add_enemies(self):
        if self.enemies_to_add > 0:
            if self.__enemies_add_ticks == 0:
                self.add_enemy()
                self.__enemies_add_ticks = self.ENEMY_ADD_INTERVAL
            else:
                self.__enemies_add_ticks -= 1

    def update(self):
        self.__tick_number += 1
        self.check_enemies()
        self.arrows_turn()
        self.units_turn()
        self.add_enemies()
