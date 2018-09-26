from Point import Point
from Game import Game


def test_get_map_size():
    expected = 30, 7
    actual = Game.get_map_size('map.txt')
    assert expected == actual


game = Game('map.txt')


def test_enemies_turn():
    assert game.is_enemies_turn


def test_add_enemy():
    previous_enemies = len(game.enemies)
    previous_new_enemies = len(game.new_enemies)
    game.add_enemy()
    assert previous_enemies + 1 == len(game.enemies)
    assert previous_new_enemies + 1 == len(game.new_enemies)


def test_able_to_build_tower():
    assert game.able_to_build_tower


def test_build_tower():
    previous = len(game.towers)
    game.build_tower(Point(0, 0))
    assert previous + 1 == len(game.towers)


def test_check_enemies():
    previous = len(game.enemies)
    game.check_enemies()
    assert previous == len(game.enemies)


def test_update():
    previous = game.tick_number
    game.update()
    assert previous + 1 == game.tick_number
