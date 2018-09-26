import sys
from Point import Point
from PyQt5.QtWidgets import QApplication
from Units.Castle import Castle


app = QApplication(sys.argv)
castle = Castle(Point(0, 0), 100)


def test_get_damage():
    damage = 1
    previous = castle.health
    castle.get_damage(damage)
    assert previous == castle.health + damage