""" Main """
from config.env import set_environment
set_environment()


from gui.main_window import MainWindow

if __name__ == '__main__':
    root = MainWindow()
    root.mainloop()
