from app_class import *


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WindowSettings()
    ex.show()
    sys.exit(app.exec())