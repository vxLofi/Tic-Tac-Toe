from main_window import MainMenu
from selectionpage import SelectionPageWindow
from how_to_play import HowToPlayWindow
from gamestarted import DisappearingMode, GameStartedWindow, ClassicVsAI, DisappearingVsAI

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
       super().__init__()
       self.setWindowTitle("Tic-Tac-Toe Project")
       self.setGeometry(500, 200, 1000, 700)

    # Create a stacked widget to hold windows
       self.stacked_windows = QStackedWidget()
       self.setCentralWidget(self.stacked_windows)

    # Create instances of the main menu and game windows
       self.menu = MainMenu()
       self.selection_page = SelectionPageWindow()
       self.guide = HowToPlayWindow()
       self.classic_mode = GameStartedWindow()
       self.disappearing_mode = DisappearingMode()
       self.classic_vs_AI = ClassicVsAI()
       self.disappearing_vs_AI = DisappearingVsAI()

       self.stacked_windows.addWidget(self.menu)
       self.stacked_windows.addWidget(self.selection_page)
       self.stacked_windows.addWidget(self.guide)
       self.stacked_windows.addWidget(self.classic_mode)
       self.stacked_windows.addWidget(self.disappearing_mode)
       self.stacked_windows.addWidget(self.classic_vs_AI)
       self.stacked_windows.addWidget(self.disappearing_vs_AI)

    # Set the initial window to the main menu
       self.stacked_windows.setCurrentWidget(self.menu)

       game_modes = [
          self.classic_mode,
          self.disappearing_mode,
          self.classic_vs_AI,
          self.disappearing_vs_AI
       ]

       for game_mode in game_modes:
          game_mode.main_menu_button.clicked.connect(lambda: self.stacked_windows.setCurrentWidget(self.menu))
          game_mode.main_menu_button.clicked.connect(game_mode.play_again)

    # Connect the start button to switch to the game window
       self.menu.selection_button.clicked.connect(self.select_game)

    # Connect the "How to Play" button to show the "How to Play" window
       self.menu.how_to_play_button.clicked.connect(self.show_how_to_play)

    #Back button to return to main menu
       self.guide.back_button.clicked.connect(lambda: self.stacked_windows.setCurrentWidget(self.menu))

    # Connect the selection buttons to switch to the respective game modes
       self.selection_page.classic_button.clicked.connect(lambda: self.stacked_windows.setCurrentWidget(self.classic_mode))

    #Disappearing mode button
       self.selection_page.disappearing_button.clicked.connect(lambda: self.stacked_windows.setCurrentWidget(self.disappearing_mode))
    
    def select_game(self):
      self.stacked_windows.setCurrentWidget(self.selection_page)

    def show_how_to_play(self):
        self.stacked_windows.setCurrentWidget(self.guide)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()