from main_window import MainMenu
from game_started import GameStartedWindow
from how_to_play import HowToPlayWindow

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget
from PySide6.QtCore import Qt


class MainWindown(QMainWindow):
    def __init__(self):
       super().__init__()
       self.setWindowTitle("Tic-Tac-Toe Project")
       self.setGeometry(500, 300, 1000, 700)

    # Create a stacked widget to hold windows
       self.stacked_windows = QStackedWidget()
       self.setCentralWidget(self.stacked_windows)

    # Create instances of the main menu and game windows
       self.menu = MainMenu()
       self.game = GameStartedWindow()
       self.guide = HowToPlayWindow()

       self.stacked_windows.addWidget(self.menu)
       self.stacked_windows.addWidget(self.game)
       self.stacked_windows.addWidget(self.guide)

    # Set the initial window to the main menu
       self.stacked_windows.setCurrentWidget(self.menu)

    # Connect the start button to switch to the game window
       self.menu.start_button.clicked.connect(self.start_game)

    # Connect the "How to Play" button to show the "How to Play" window
       self.menu.how_to_play_button.clicked.connect(self.show_how_to_play)

    #Back button to return to main menu
       self.guide.back_button.clicked.connect(self.show_main_menu)

       self.game.play_again_button.clicked.connect(self.start_game)

       self.game.main_menu_button.clicked.connect(self.show_main_menu)

       self.classic=0
    
    def start_game(self):
      self.stacked_windows.setCurrentWidget(self.game)

    def show_how_to_play(self):
        self.stacked_windows.setCurrentWidget(self.guide)

    def show_main_menu(self):
        self.stacked_windows.setCurrentWidget(self.menu)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindown()
    window.show()
    app.exec()