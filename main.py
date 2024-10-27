""" Main """
from gui.main_window import MainWindow
from config.env import set_environment

if __name__ == '__main__':
    set_environment()
    root = MainWindow()
    root.mainloop()
