from functools import partial
from PyQt5.QtWidgets import QMainWindow, QFrame, QPushButton, QMessageBox, qApp, QProgressBar
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtGui import QIcon, QPainter, QFont, QCursor, QPixmap
from PyQt5.Qt import Qt
from Point import Point
from Units.Towers import ArrowTower


class GameWindow(QMainWindow):

    EXIT_CODE_REBOOT = -123

    IMAGE_SIZE = 64
    HEALTH_BAR_SHIFT = IMAGE_SIZE / 2
    TIMER_INTERVAL = 16

    WIDTH = 1920
    HEIGHT = 1000

    SHIFT = 2

    FONT = QFont("times", 20)

    def __init__(self, game):
        super().__init__()
        self.__timer = QBasicTimer()
        self.__is_paused = False
        self.game = game
        self.coin_picture = QPixmap("images/coin.png")
        self.initUI()

    def initUI(self):
        self.setWindowState(Qt.WindowFullScreen)
        self.setWindowTitle('TD')
        self.setWindowIcon(QIcon('images/smorc.png'))

        self.__pause_button = QPushButton('Pause/Play', self)
        self.__pause_button.move(self.WIDTH - 350, 10)
        self.__pause_button.clicked.connect(self.pause_click)

        self.__tower_button = QPushButton('', self)
        self.__tower_button.setStyleSheet("background: transparent;");
        self.__tower_button.setGeometry(10, self.height() - 10 - self.IMAGE_SIZE * 5 / 2,
                                        self.IMAGE_SIZE * 2, self.IMAGE_SIZE * 2)
        self.__tower_button.clicked.connect(self.show_tower_cell_btns)

        self.__restart_button = QPushButton('Restart', self)
        self.__restart_button.move(self.WIDTH - 250, 10)
        self.__restart_button.clicked.connect(self.restart)

        self.__quit_button = QPushButton('Quit', self)
        self.__quit_button.move(self.WIDTH - 150, 10)
        self.__quit_button.clicked.connect(self.quit)

        self.__tower_cell_buttons = self.get_tower_cell_buttons()
        self.__tower_cell_buttons_shown = False

        self.enemies_health_bars = {}

        self.__timer.start(self.TIMER_INTERVAL, self)

        self.pause()
        self.show()

    def add_enemies_health_bars(self):
        while len(self.game.new_enemies) > 0:
            enemy = self.game.new_enemies.pop()
            bar = QProgressBar(self)
            bar.resize(self.IMAGE_SIZE, self.IMAGE_SIZE / 4)
            bar.setAlignment(Qt.AlignCenter)
            bar.setStyleSheet('QProgressBar::chunk {background-color: red;}')
            bar.setMaximum(enemy.health)
            self.enemies_health_bars[enemy] = bar
            bar.show()

    def update_enemies_health_bars(self):
        for enemy, bar in self.enemies_health_bars.items():
            if not enemy.is_alive or enemy.got_to_route_end:
                bar.close()
            else:
                coordinates = enemy.coordinates.convert_to_image_coordinates(self.IMAGE_SIZE, self.SHIFT)
                bar.move(coordinates.x, coordinates.y - self.HEALTH_BAR_SHIFT)
                bar.setValue(enemy.health)

    def get_tower_cell_buttons(self):
        tower_cell_buttons = []
        for cell in self.game.game_map:
            if not cell.is_road:
                button = QPushButton('', self)
                button.setGeometry((cell.coordinates.x) * self.IMAGE_SIZE,
                                   (self.SHIFT + cell.coordinates.y) * self.IMAGE_SIZE,
                                   self.IMAGE_SIZE, self.IMAGE_SIZE)
                button.setStyleSheet("border-image: url(images/towerButton.png) stretch;");
                button.clicked.connect(partial(self.build_tower, button))
                button.hide()
                tower_cell_buttons.append(button)
        return tower_cell_buttons

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
        coordinates = Point(button.x(), button.y()).convert_to_cell_coordinates(self.IMAGE_SIZE, self.SHIFT)
        self.game.build_tower(coordinates)
        self.show_tower_cell_btns()
        self.__tower_cell_buttons.remove(button)
        self.update()

    def create_tower_cursor(self):
        painter = QPainter()
        tower = QPixmap('images/tower.png')
        size = 2 * (ArrowTower.SHOOTING_RANGE - 1) * self.IMAGE_SIZE
        circle = QPixmap(size, size)
        circle.fill(Qt.transparent)
        painter.begin(circle)
        painter.drawEllipse(0, 0, circle.width() - 1, circle.height() - 1)
        painter.drawPixmap((circle.width() - tower.width()) / 2, (circle.height() - tower.height()) / 2, tower)
        painter.end()
        self.setCursor(QCursor(circle))

    def show_tower_cell_btns(self):
        if self.__tower_cell_buttons_shown:
            self.setCursor(Qt.ArrowCursor)
        elif self.game.able_to_build_tower:
            self.create_tower_cursor()
        for button in self.__tower_cell_buttons:
            if self.__tower_cell_buttons_shown:
                button.hide()
            elif self.game.able_to_build_tower:
                button.show()
        self.__tower_cell_buttons_shown = not self.__tower_cell_buttons_shown

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
        for enemy in self.game.enemies:
            self.draw_in_cell(enemy.image, enemy.coordinates, painter, 0, self.IMAGE_SIZE // 4)

    def draw_towers(self, painter):
        for tower in self.game.towers:
            self.draw_in_cell(tower.image, tower.coordinates, painter)

    def draw_castle(self, painter):
        painter.setFont(self.FONT)
        painter.drawText(self.width() - 230, self.IMAGE_SIZE * 2 - 10, f'Castle health: {self.game.castle.health}')
        image = self.game.castle.image
        coordinates = self.game.castle.coordinates.convert_to_image_coordinates(self.IMAGE_SIZE, self.SHIFT)
        painter.drawPixmap(coordinates.x, coordinates.y, self.IMAGE_SIZE * 3, self.IMAGE_SIZE * 3, image)

    def draw_in_cell(self, image, cell_coordinates, painter, x_shift=0, y_shift=0):
        image_coordinates = cell_coordinates.convert_to_image_coordinates(self.IMAGE_SIZE, self.SHIFT)
        x = image_coordinates.x + x_shift
        y = image_coordinates.y - y_shift
        painter.drawPixmap(x, y, self.IMAGE_SIZE, self.IMAGE_SIZE, image)

    def draw_signature(self, painter):
        painter.drawText(self.width() - 125, self.height() - 10, 'Made by Artemiy Izakov')

    def draw_gold(self, painter):
        painter.setFont(self.FONT)
        painter.drawPixmap(20 + len(f'{self.game.gold}') * 15, self.IMAGE_SIZE // 2,
                           self.IMAGE_SIZE, self.IMAGE_SIZE, self.coin_picture)
        painter.drawText(10, self.IMAGE_SIZE // 2 + 40, f'{self.game.gold}')

    def draw_projectiles(self, painter):
        for arrow in self.game.projectiles:
            self.draw_in_cell(arrow.image, arrow.coordinates, painter)

    def draw_tower_costs(self, painter):
        painter.drawPixmap(self.__tower_button.x(), self.__tower_button.y(), self.IMAGE_SIZE * 2, self.IMAGE_SIZE * 2,
                           QPixmap('images/button.png'))
        painter.drawPixmap(self.__tower_button.x() + 10, self.__tower_button.y() + 10,
                           self.IMAGE_SIZE * 2 - 20, self.IMAGE_SIZE * 2 - 20, QPixmap('images/tower.png'))
        arrow_x = self.__tower_button.x() + self.__tower_button.width() // 2 - self.IMAGE_SIZE // 2
        arrow_y = self.__tower_button.y() + self.__tower_button.height() + 5
        painter.drawPixmap(arrow_x - 5, arrow_y, self.IMAGE_SIZE // 2, self.IMAGE_SIZE // 2, self.coin_picture)
        painter.drawText(arrow_x + 30, arrow_y + self.IMAGE_SIZE // 2 - 5, f'{ArrowTower.COST}')

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.draw_signature(painter)
        self.draw_gold(painter)

        self.draw_map(painter)
        self.draw_towers(painter)
        self.draw_enemies(painter)
        self.draw_castle(painter)
        self.draw_projectiles(painter)
        self.draw_tower_costs(painter)

        painter.end()

    def timerEvent(self, event):
        if event.timerId() == self.__timer.timerId():
            self.game.update()
            self.add_enemies_health_bars()
            self.update_enemies_health_bars()
            if not self.game.castle.is_alive:
                self.game_over()
            self.update()
        else:
            QFrame.timerEvent(event)
