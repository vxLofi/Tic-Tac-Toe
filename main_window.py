from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget
from PySide6.QtCore import Qt

from game_started import GameStartedWindow

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)


    #Title label
        self.label = QLabel("Welcome to Tic-Tac-Toe!")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24px;")

    #Start Main Menu Button
        self.start_button = QPushButton("Start Game")
        self.start_button.setStyleSheet("font-size: 24px;")

    #How to Play Button
        self.how_to_play_button = QPushButton("How to Play")
        self.how_to_play_button.setStyleSheet("font-size: 24px;")

    #Layout for the buttons and label of main
        layout.addWidget(self.label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.how_to_play_button)
