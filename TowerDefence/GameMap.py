class GameMap:
    def __init__(self, land, enemy_route, map_width, map_heigth, castle_coordinates):
        self.__land = land
        self.__enemy_route = enemy_route
        self.__map_width = map_width
        self.__map_heigth = map_heigth
        self.__castle_coordinates = castle_coordinates