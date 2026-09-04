from PySide6.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QMainWindow, QLabel, QPushButton, QStackedLayout, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6 import QtGui

class SelectionPageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        selection_page_container = QWidget()
        self.setCentralWidget(selection_page_container)
        selection_page_layout = QVBoxLayout(selection_page_container)

        self.selection_label = QLabel("Choose a game mode to play:")
        self.selection_label.setAlignment(Qt.AlignCenter)
        self.selection_label.setStyleSheet("font-size: 24px;")
        selection_page_layout.addWidget(self.selection_label)

        self.classic_button = QPushButton("Classic")
        self.classic_button.setStyleSheet("font-size: 24px;")
        selection_page_layout.addWidget(self.classic_button)

        self.disappearing_button = QPushButton("Disappearing")
        self.disappearing_button.setStyleSheet("font-size: 24px;")
        selection_page_layout.addWidget(self.disappearing_button)

        self.ai_button = QPushButton("Play against AI")
        self.ai_button.setStyleSheet("font-size: 24px;")
        selection_page_layout.addWidget(self.ai_button)
