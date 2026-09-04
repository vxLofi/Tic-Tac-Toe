from PySide6.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QMainWindow, QLabel, QPushButton, QStackedLayout, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6 import QtGui


def wining_logic(player, board):
    WINS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]
    for row in WINS:
        if board[row[0]] == board[row[1]] == board[row[2]] == player:
            return f"Player {player} has won!"
    else:
        return False