import sys
from PyQt5.QtWidgets import QApplication
from GameWindow import GameWindow
from Game import Game


if __name__ == '__main__':
    currentExitCode = GameWindow.EXIT_CODE_REBOOT
    while currentExitCode == GameWindow.EXIT_CODE_REBOOT:
        app = QApplication(sys.argv)
        window = GameWindow(Game('map.txt'))
        currentExitCode = app.exec_()
        app = None
    sys.exit(currentExitCode)