from functools import partial
from PyQt5.QtWidgets import QMainWindow, QFrame, QPushButton, QMessageBox, qApp
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtGui import QIcon, QPainter, QFont
from Units import Tower, Enemy
from Point import Point


class GameWindow(QMainWindow):

    EXIT_CODE_REBOOT = -123

    def __init__(self, game):
        super().__init__()
        self.__game_map = game.game_map
        self.__tick_number = 0
        self.__width = 1600
        self.__height = 800
        self.__font = QFont("times", 20)

        self.__castle = game.castle

        self.__towers = []
        self.__tower_damage = 5
        self.__tower_shooting_range = 5
        self.__tower_cost = 30

        self.__gold = 60

        self.__enemies = []
        self.__enemies_to_add = 3
        self.__enemies_route = game.enemies_route
        self.__enemies_add_interval = 1
        self.__enemies_add_ticks = 0
        self.__enemies_health = 30
        self.__enemies_damage = 5
        self.__enemy_gold = 10

        self.__image_size = 50
        self.__timer_interval = 100
        self.__units_turn_ticks_interval = 10
        self.__timer = QBasicTimer()

        self.__is_paused = False

        self.__temporary_lines = []

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, self.__width, self.__height)
        self.setWindowTitle('TD')
        self.setWindowIcon(QIcon('images/smorc.png'))

        self.__pause_btn = QPushButton('Pause/Play', self)
        self.__pause_btn.move(50, 410)
        self.__pause_btn.clicked.connect(self.pause_click)

        self.__tower_btn = QPushButton('Build Tower ({}G)'.format(self.__tower_cost), self)
        self.__tower_btn.move(150, 410)
        # self.__tower_btn.setGeometry(250, 410, self.__image_size, self.__image_size)
        self.__tower_btn.clicked.connect(self.show_tower_cell_btns)

        self.__restart_btn = QPushButton('Restart', self)
        self.__restart_btn.move(self.__width - 250, 10)
        self.__restart_btn.clicked.connect(self.restart)

        self.__quit_btn = QPushButton('Quit', self)
        self.__quit_btn.move(self.__width - 150, 10)
        self.__quit_btn.clicked.connect(self.quit)

        self.__quit_btn = QPushButton('FOR THE HORDE!!!', self)
        self.__quit_btn.setGeometry(700, 600, 200, 100)
        self.__quit_btn.clicked.connect(self.for_the_horde)

        self.__tower_cell_btns = []
        for cell in self.__game_map:
            if not cell.is_road:
                button = QPushButton('', self)
                button.setGeometry((1 + cell.coordinates.x) * self.__image_size,
                                   (1 + cell.coordinates.y) * self.__image_size,
                                   self.__image_size, self.__image_size)
                button.clicked.connect(partial(self.build_tower, button))
                button.hide()
                self.__tower_cell_btns.append(button)
        self.__tower_cell_btns_shown = False

        self.__add_enemy_btn = QPushButton('Add Enemy', self)
        self.__add_enemy_btn.move(250, 410)
        self.__add_enemy_btn.clicked.connect(self.add_enemy_to_queue)

        self.__timer.start(self.__timer_interval, self)

        self.pause()
        self.show()

    def for_the_horde(self):
        for i in range(100500):
            self.add_enemy_to_queue()
        self.__timer_interval = 10
        self.unpause()
        self.__towers = []

    def add_enemy_to_queue(self):
        self.__enemies_to_add += 1
        self.update()

    def add_enemy(self):
        self.__enemies.append(Enemy(self.__enemies_health, self.__enemies_route, self.__enemies_damage))
        self.__enemies_to_add -= 1

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
        coordinates = Point(button.x(), button.y()).convert_to_cell_coordinates(self.__image_size, 1)
        self.__towers.append(Tower(coordinates, self.__tower_damage, self.__tower_shooting_range))
        self.show_tower_cell_btns()
        self.__tower_cell_btns.remove(button)
        self.__gold -= self.__tower_cost
        self.update()

    def show_tower_cell_btns(self):
        for button in self.__tower_cell_btns:
            if self.__tower_cell_btns_shown:
                button.hide()
            else:
                if self.__gold >= self.__tower_cost:
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
        self.__timer.start(self.__timer_interval, self)
        self.update()

    def draw_map(self, painter):
        for land in self.__game_map:
            self.draw_in_cell(land.image, land.coordinates, painter)

    def draw_enemies(self, painter):
        painter.setFont(self.__font)
        painter.drawText(50, 35, 'Enemies left: {}'.format(self.__enemies_to_add))
        for enemy in self.__enemies:
            self.draw_in_cell(enemy.image, enemy.coordinates, painter)

    def draw_towers(self, painter):
        for tower in self.__towers:
            self.draw_in_cell(tower.image, tower.coordinates, painter)

    def draw_castle(self, painter):
        painter.setFont(self.__font)
        painter.drawText(350, 35, 'Castle health: {}'.format(self.__castle.health))
        image = self.__castle.image
        coordinates = self.__castle.coordinates
        coordinates = coordinates.convert_to_image_coordinates(self.__image_size, 1)
        painter.drawPixmap(coordinates.x, coordinates.y, self.__image_size * 2, self.__image_size * 2, image)

    def draw_in_cell(self, image, cell_coordinates, painter):
        image_coordinates = cell_coordinates.convert_to_image_coordinates(self.__image_size, 1)
        x = image_coordinates.x
        y = image_coordinates.y
        painter.drawPixmap(x, y, self.__image_size, self.__image_size, image)

    def draw_signature(self, painter):
        painter.drawText(self.__width - 125, self.__height - 10, 'Made by Artemiy Izakov')

    def draw_gold(self, painter):
        painter.setFont(self.__font)
        painter.drawText(650, 35, 'Gold: {}'.format(self.__gold))

    @property
    def is_units_turn(self):
        return self.__tick_number % self.__units_turn_ticks_interval == 0

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.draw_signature(painter)
        self.draw_gold(painter)

        self.draw_map(painter)
        self.draw_enemies(painter)
        self.draw_towers(painter)
        self.draw_castle(painter)

        for line in self.__temporary_lines:
            painter.drawLine(*line)
        self.__temporary_lines = []

        painter.end()

    def timerEvent(self, event):
        if event.timerId() == self.__timer.timerId():
            self.__tick_number += 1

            for enemy in self.__enemies:
                if not enemy.is_alive:
                    self.__enemies.remove(enemy)
                    self.__gold += self.__enemy_gold
                if enemy.got_to_route_end:
                    self.__castle.get_damage(enemy.damage)
                    self.__enemies.remove(enemy)
                else:
                    if self.is_units_turn:
                        enemy.move()

            if not self.__castle.is_alive:
                self.game_over()

            if self.is_units_turn:
                for tower in self.__towers:
                    for enemy in self.__enemies:
                        if tower.try_to_shoot(enemy):
                            begin = tower.coordinates.convert_to_image_coordinates(self.__image_size, 1)
                            end = enemy.coordinates.convert_to_image_coordinates(self.__image_size, 1)
                            shift = self.__image_size // 2
                            self.__temporary_lines.append((begin.x + shift, begin.y + shift,
                                                           end.x + shift, end.y + shift))
                            break

                if self.__enemies_to_add > 0:
                    if self.__enemies_add_ticks == 0:
                        self.add_enemy()
                        self.__enemies_add_ticks = self.__enemies_add_interval
                    else:
                        self.__enemies_add_ticks -= 1

            self.update()
        else:
            QFrame.timerEvent(event)
