import PyQt5
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from app_class import *
from pygame.math import Vector2 as vec
import sqlite3


class WindowSettings(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('WindowSettings.ui', self)
        self.musictf = False
        self.setWindowIcon(QtGui.QIcon('logo_set.png'))
        self.setWindowTitle('Настройки')
        self.end_button.clicked.connect(self.end)
        self.music_button.clicked.connect(self.music)
        self.label_4.setStyleSheet("QLabel { background-color: rgba(180, 180, 180, 160)}")
        self.label_5.setStyleSheet("QLabel { background-color: rgba(180, 180, 180, 160)}")
        self.df = {'Легкая': '1.25',
              'Средняя': '1',
              'Сложная': '0.75'}

    def end(self):
        difficultly = self.df[self.difficultly_box.currentText()]
        with open('settings.txt', 'w') as f:
            f.write(str(difficultly + ' ' + str(self.musictf)))
        self.close()
        self.wnd = Login()
        self.wnd.show()

    def music(self):
        if self.musictf == False:
            self.musictf = True
        else:
            self.musictf = False
    
    def pg_run(self):
        app = App()
        app.run()

class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.setWindowTitle('Вход')
        self.setWindowIcon(QtGui.QIcon('logo_log.png'))
        con = sqlite3.connect("base.bd")
        cur = con.cursor()
        self.result = cur.execute("""SELECT name, password FROM players""").fetchall()
        con.commit()
        self.enter_btn.clicked.connect(self.enter_log)
        self.create_btn.clicked.connect(self.enter_reg)
        self.error_label.setStyleSheet("color: rgb(255, 0, 0)")

    def enter_log(self):
        self.name = self.Name_acc_old.text()
        self.error_label.setText('')
        if self.name_check() != True:
            self.error_label.setText('Неверные данные!')
        else:
            self.error_label.setStyleSheet("color: rgb(0, 125, 125)")
            self.error_label.setText('Успешный вход')
            con = sqlite3.connect("base.bd")
            cur = con.cursor()
            self.result = cur.execute("""SELECT * FROM players""").fetchall()
            con.commit()
            self.player_name = self.name
            for i in self.result:
                if i[1] == self.name:
                    self.player_record = i[3]
            with open('player_info.txt', 'w') as f:
                f.write(str(self.player_name + ' ' + str(self.player_record)))
            self.close()
            app = App()
            app.run()

    def enter_reg(self):
        self.new_name = self.Name_acc_new.text()
        self.error_label.setText('')
        res = self.new_name_check()
        if res != True:
            self.error_label.setText(res)
        else:
            res1 = self.password_check()
            if res1:
                con = sqlite3.connect("base.bd")
                cur = con.cursor()
                cur.execute("INSERT INTO players(name, password) VALUES(?, ?)", (self.new_name, self.Password1.text()))
                self.result = cur.execute("""SELECT * FROM players""").fetchall()
                con.commit()
                self.player_name = self.new_name
                for i in self.result:
                    if i[1] == self.new_name:
                        self.player_record = i[3]
                with open('player_info.txt', 'w') as f:
                    f.write(str(self.player_name + ' ' + str(self.player_record)))
                self.close()
                app = App()
                app.run()

    def new_name_check(self):
        ok = True
        if self.new_name == '' or len(self.new_name) < 4:
            ok = 'Слишком короткое имя.'
        if ok:
            for i in self.result:
                if i[0] == self.new_name:
                    self.error_label.setText('Данное имя занято')
                    ok = False
                    continue
        return ok

    def name_check(self):
        ok = False
        for i in self.result:
            if i[0] == self.name and i[1] == self.password_acc_old.text():
                ok = True
                continue
        return ok

    def password_check(self):
        ok = True
        self.was = False
        if self.Password1.text().isdigit():
            self.error_label.setText('Пароль должен содержать буквы')
            ok = False
        if '1234' in self.Password1.text() or 'password' in self.Password1.text().lower() or 'пароль' in self.Password1.text().lower():
            self.error_label.setText('Пароль слишком простой')
            ok = False
        if len(self.Password1.text()) < 6:
            self.error_label.setText('Пароль слишком короткий')
            ok = False
        if self.Password1.text() != self.password2.text():
            self.error_label.setText('Пароли не совпадают')
            ok = False
        if self.Password1.text() == '' or self.password2.text() == '':
            self.error_label.setText('Ошибка пароля. Пустое поле')
            ok = False
        return ok
    
    
WIDTH, HEIGHT = 610, 670
TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT, ROWS, COLS, FPS = WIDTH - TOP_BOTTOM_BUFFER, HEIGHT - TOP_BOTTOM_BUFFER, 30, 28, 60
BLACK = (0, 0, 0)
RED = (208, 22, 22)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
PLAYER_COLOUR = (190, 194, 15)
START_TEXT_SIZE = 16
START_FONT = 'arial black'
if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = WindowSettings()
        ex.show()
        sys.exit(app.exec())

