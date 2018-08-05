from functools import partial
from PyQt5.QtWidgets import QMainWindow, QFrame, QPushButton, QMessageBox, qApp
from PyQt5.QtCore import QBasicTimer, QSize
from PyQt5.QtGui import QIcon, QPainter, QFont, QCursor, QPixmap
from PyQt5.Qt import Qt
from Point import Point
from Game import Game


class GameWindow(QMainWindow):

    EXIT_CODE_REBOOT = -123

    IMAGE_SIZE = 64
    TIMER_INTERVAL = 33

    WIDTH = 1920
    HEIGHT = 1000

    FONT = QFont("times", 20)

    def __init__(self, game):
        super().__init__()
        self.__timer = QBasicTimer()
        self.__is_paused = False
        self.game = game
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 30, self.WIDTH, self.HEIGHT)
        self.setWindowTitle('TD')
        self.setWindowIcon(QIcon('images/smorc.png'))

        self.__pause_btn = QPushButton('Pause/Play', self)
        self.__pause_btn.move(50, 610)
        self.__pause_btn.clicked.connect(self.pause_click)

        self.__tower_btn = QPushButton(f'Build Tower ({Game.TOWER_COST}G)', self)
        self.__tower_btn.move(150, 610)
        self.__tower_btn.clicked.connect(self.show_tower_cell_btns)

        self.__restart_btn = QPushButton('Restart', self)
        self.__restart_btn.move(self.WIDTH - 250, 10)
        self.__restart_btn.clicked.connect(self.restart)

        self.__quit_btn = QPushButton('Quit', self)
        self.__quit_btn.move(self.WIDTH - 150, 10)
        self.__quit_btn.clicked.connect(self.quit)

        self.__tower_cell_btns = []
        for cell in self.game.game_map:
            if not cell.is_road:
                button = QPushButton('', self)
                button.setGeometry((cell.coordinates.x) * self.IMAGE_SIZE,
                                   (1 + cell.coordinates.y) * self.IMAGE_SIZE,
                                   self.IMAGE_SIZE, self.IMAGE_SIZE)
                button.setStyleSheet("border-image: url(images/towerButton.png) stretch;");
                button.setIconSize(QSize(self.IMAGE_SIZE, self.IMAGE_SIZE))
                button.clicked.connect(partial(self.build_tower, button))
                button.hide()
                self.__tower_cell_btns.append(button)
        self.__tower_cell_btns_shown = False

        self.__add_enemy_btn = QPushButton('Add Enemy', self)
        self.__add_enemy_btn.move(250, 610)
        self.__add_enemy_btn.clicked.connect(self.add_enemy_to_queue)

        self.__timer.start(self.TIMER_INTERVAL, self)

        self.pause()
        self.show()

    def add_enemy_to_queue(self):
        self.game.enemies_to_add += 1
        self.update()

    def game_over(self):
        self.pause()
        message = QMessageBox()
        message.setWindowIcon(QIcon('images/smorc.png'))
        message.setWindowTitle('Game Over!!!11!')
        message.setText('You Lost((9(')
        restart = message.addButton('MORE!!!!', QMessageBox.AcceptRole)
        message.addButton("That's the End", QMessageBox.RejectRole)
        message.exec()
        if message.clickedButton() == restart:
            self.restart()
        else:
            self.quit()

    def build_tower(self, button):
        coordinates = Point(button.x(), button.y()).convert_to_cell_coordinates(self.IMAGE_SIZE, 1)
        self.game.build_tower(coordinates)
        self.show_tower_cell_btns()
        self.__tower_cell_btns.remove(button)
        self.update()

    def show_tower_cell_btns(self):
        if self.__tower_cell_btns_shown:
            self.setCursor(Qt.ArrowCursor)
        elif self.game.able_to_build_tower:
            self.setCursor(QCursor(QPixmap('images/tower.png')))
        for button in self.__tower_cell_btns:
            if self.__tower_cell_btns_shown:
                button.hide()
            elif self.game.able_to_build_tower:
                button.show()
        self.__tower_cell_btns_shown = not self.__tower_cell_btns_shown

    def restart(self):
        qApp.exit(GameWindow.EXIT_CODE_REBOOT)

    def quit(self):
        qApp.exit()

    def pause_click(self):
        if self.__is_paused:
            self.unpause()
        else:
            self.pause()

    def pause(self):
        self.__is_paused = True
        self.__timer.stop()
        self.update()

    def unpause(self):
        self.__is_paused = False
        self.__timer.start(self.TIMER_INTERVAL, self)
        self.update()

    def draw_map(self, painter):
        for land in self.game.game_map:
            self.draw_in_cell(land.image, land.coordinates, painter)

    def draw_enemies(self, painter):
        painter.setFont(self.FONT)
        painter.drawText(50, 35, f'Enemies left: {self.game.enemies_to_add}')
        for enemy in self.game.enemies:
            self.draw_in_cell(enemy.image, enemy.coordinates, painter, 0, self.IMAGE_SIZE // 4)

    def draw_towers(self, painter):
        for tower in self.game.towers:
            self.draw_in_cell(tower.image, tower.coordinates, painter)

    def draw_castle(self, painter):
        painter.setFont(self.FONT)
        painter.drawText(350, 35, f'Castle health: {self.game.castle.health}')
        image = self.game.castle.image
        coordinates = self.game.castle.coordinates.convert_to_image_coordinates(self.IMAGE_SIZE, 1)
        painter.drawPixmap(coordinates.x, coordinates.y, self.IMAGE_SIZE * 3, self.IMAGE_SIZE * 3, image)

    def draw_in_cell(self, image, cell_coordinates, painter, x_shift=0, y_shift=0):
        image_coordinates = cell_coordinates.convert_to_image_coordinates(self.IMAGE_SIZE, 1)
        x = image_coordinates.x + x_shift
        y = image_coordinates.y - y_shift
        painter.drawPixmap(x, y, self.IMAGE_SIZE, self.IMAGE_SIZE, image)

    def draw_signature(self, painter):
        painter.drawText(self.WIDTH - 125, self.HEIGHT - 10, 'Made by Artemiy Izakov')

    def draw_gold(self, painter):
        painter.setFont(self.FONT)
        painter.drawText(650, 35, f'Gold: {self.game.gold}')

    def draw_arrows(self, painter):
        for arrow in self.game.arrows:
            self.draw_in_cell(arrow.image, arrow.coordinates, painter)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.draw_signature(painter)
        self.draw_gold(painter)

        self.draw_map(painter)
        self.draw_towers(painter)
        self.draw_enemies(painter)
        self.draw_castle(painter)
        self.draw_arrows(painter)

        painter.end()

    def timerEvent(self, event):
        if event.timerId() == self.__timer.timerId():
            self.game.update()
            if not self.game.castle.is_alive:
                self.game_over()
            self.update()
        else:
            QFrame.timerEvent(event)
