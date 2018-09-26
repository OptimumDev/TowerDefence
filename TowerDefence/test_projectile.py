import sys
from Point import Point
from PyQt5.QtWidgets import QApplication
from Units.Projectiles import Arrow, Projectile
from Units.Enemies import Orc


app = QApplication(sys.argv)
enemy = Orc([Point(1, 1)])
arrow = Arrow(Point(0, 0), enemy)


def test_enemy_coordinates():
    assert arrow.enemy_coordinates == enemy.coordinates + Projectile.ENEMY_RADIUS


def test_got_to_enemy():
    assert not arrow.got_to_enemy