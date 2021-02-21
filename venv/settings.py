import PyQt5
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

class WindowSettings(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('WindowSettings.ui', self)
        self.musictf = False
        self.setWindowTitle('Настройки')
        self.end_button.clicked.connect(self.end)
        self.music_button.clicked.connect(self.music)
        self.label_4.setStyleSheet("QLabel { background-color: rgba(180, 180, 180, 160)}")
        self.label_5.setStyleSheet("QLabel { background-color: rgba(180, 180, 180, 160)}")
        self.df = {'Легкая': 'easy',
              'Средняя': 'Medium',
              'Сложная': 'hard'}
    def end(self):
        difficultly = self.df[self.difficultly_box.currentText()]
        with open('settings.txt', 'w') as f:
            f.write(str(difficultly + ' ' + str(self.musictf)))
        self.close()

    def music(self):
        if self.musictf == False:
            self.musictf = True
        else:
            self.musictf = False

# SCREEN settings
width, height, fps, rows, cols, offset, map_width, map_height = 610, 670, 60, 30, 28, 50, 560, 620


if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = WindowSettings()
        ex.show()

        sys.exit(app.exec())
        print(difficultly)




# color settings
# player settings
# mob settings
