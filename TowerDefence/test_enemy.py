from Units.Enemies import Orc
import sys
from Point import Point
from PyQt5.QtWidgets import QApplication


app = QApplication(sys.argv)
orc = Orc([Point(0, 0)])


def test_health():
    assert orc.health == Orc.MAX_HEALTH


def test_damage():
    assert orc.damage == Orc.DAMAGE


def test_is_alive():
    assert orc.is_alive


def got_to_the_route_end():
    assert orc.got_to_route_end


def test_get_damage():
    damage = 1
    previous = orc.health
    orc.get_damage(damage)
    assert orc.health == previous - damage
