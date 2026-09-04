from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget
from PySide6.QtCore import Qt

class HowToPlayWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)

        self.instructions = QLabel("How to Play Tic-Tac-Toe:\n\n"
                            "1. The game is played on a 3x3 grid.\n "
                            "2. Players take turns placing their marks (X or O) on the grid.\n "
                            "3. The first player to get 3 of their marks in a row (up, down, across, or diagonally) wins.\n "
                            "4. If all 9 squares are filled with no winner, the game is a draw.")
        self.instructions.setStyleSheet("font-size: 24px;")

        self.back_button = QPushButton("Back to Main Menu")
        self.back_button.setStyleSheet("font-size: 24px;")

        self.instructions.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.instructions)
        layout.addWidget(self.back_button)