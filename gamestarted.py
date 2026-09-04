from PySide6.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QMainWindow, QLabel, QPushButton, QStackedLayout, QVBoxLayout, QWidget
from PySide6.QtCore import QPropertyAnimation, Qt
from PySide6 import QtGui

class GameStartedWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_player = "O"
        self.buttons = []
        self.board = [None] * 9

        container = QWidget()
        self.setCentralWidget(container)
        self.layout = QVBoxLayout(container)

        self.starting_widgets()

        self.add_buttons()

    def starting_widgets(self):
        # Add a label to indicate the game has started
        self.starting_label = QLabel("Player O's turn")
        self.starting_label.setStyleSheet("color: #00BFFF; font-size: 24px;")
        self.starting_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.starting_label)

        #Make the layout for the Tic-Tac-Toe board and buttons
        self.board_layout = QStackedLayout()
        self.board_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        self.layout.addLayout(self.board_layout) ##StackedLayout from "self.board" - Index 0

        #Add the Tic-Tac-Toe board image
        self.board_image = QLabel()
        self.board_image.setPixmap(QtGui.QPixmap("./assets/tictactoe.png").scaled(600, 600))
        self.board_image.setAlignment(Qt.AlignCenter)
        self.board_layout.addWidget(self.board_image)

        #Add the "Play Again" button and "Main Menu" button
        self.end_gamesbuttons_layout = QHBoxLayout()
        self.layout.addLayout(self.end_gamesbuttons_layout)
        self.play_again_button = QPushButton("Play Again")
        self.play_again_button.setStyleSheet("font-size: 24px;")
        self.play_again_button.clicked.connect(self.play_again)
        self.end_gamesbuttons_layout.addWidget(self.play_again_button)

        self.main_menu_button = QPushButton("Main Menu")
        self.main_menu_button.setStyleSheet("font-size: 24px;")
        self.end_gamesbuttons_layout.addWidget(self.main_menu_button)

    def add_buttons(self):
        self.button_widget = QWidget()
        self.button_layout = QGridLayout(self.button_widget)
        self.button_layout.setHorizontalSpacing(16)
        self.button_layout.setVerticalSpacing(13)
        for row in range(3):
                    for col in range(3):
                        button = QPushButton()
                        button.setFixedSize(150, 150)
                        button.setStyleSheet("""
                        QPushButton {
                            background-color: transparent;
                            border: none;
                        }

                        QPushButton:hover {
                            background-color: rgba(255, 255, 255, 50);
                        }
                    """)
                        button.setProperty("Enabled", True)
                        button.clicked.connect(self.button_clicked)
                        self.button_layout.addWidget(button, row, col)
                        self.buttons.append(button)

        self.button_layout.setAlignment(Qt.AlignCenter)
        self.board_layout.addWidget(self.button_widget) #StackedLayout from "self.board" - Index 1
        self.board_layout.setCurrentIndex(1) #Buttons infront of the board image

    def button_clicked(self):
        button = self.sender()

        if not button.property("Enabled"):
            return

        current_button_index = self.buttons.index(button)
        self.board[current_button_index] = self.current_player

        button.setStyleSheet("background-color: transparent; border: none;")
        button.setProperty("Enabled", False)  # Disable the button after it's clicked

        if self.current_player == "O":
            print("Player O clicked the button!")
            button.setIcon(QtGui.QIcon("./assets/tictactoe_circle.png")) #Change to circle icon for player O
        else:
            print("Player X clicked the button!")
            button.setIcon(QtGui.QIcon("./assets/tictactoe_x.png")) #Change to cross icon for player X

        button.setIconSize(button.size())

        wining_result = self.check_for_win()

        if wining_result:
            for btn in self.buttons:
                btn.setStyleSheet("background-color: transparent; border: none;")
                btn.setProperty("Enabled", False)
            self.starting_label.setText(f"Player {self.current_player} has won!")
            return

        if None not in self.board:
            self.starting_label.setText("Game Over! It's a draw!")
            self.starting_label.setStyleSheet("color: white; font-size: 24px;")
            print("Game Over! It's a draw!")
            return

        if self.current_player == "O":
            self.current_player = "X"
            self.starting_label.setText("Player X's turn")
            self.starting_label.setStyleSheet("color: red; font-size: 24px;")
        else:
            self.current_player = "O"
            self.starting_label.setText("Player O's turn")
            self.starting_label.setStyleSheet("color: #00BFFF; font-size: 24px;")

    def start_wining_line_animation(self, winning_combination):
        pass
    
    def check_for_win(self):
        WINS = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], #Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8], #Vertical
        [0, 4, 8], [2, 4, 6]             #Diagonal
    ]
        for winning_combination in WINS:
            if self.board[winning_combination[0]] == self.board[winning_combination[1]] == self.board[winning_combination[2]] == self.current_player:
                return winning_combination
        else:
            return False

    def play_again(self):
        self.current_player = "O"
        self.starting_label.setText("Player O's turn")
        self.starting_label.setStyleSheet("color: #00BFFF; font-size: 24px;")

        for button in self.buttons:
            button.setIcon(QtGui.QIcon())
            button.setProperty("Enabled", True)
            button.setStyleSheet("""
                                    QPushButton {
                                        background-color: transparent;
                                        border: none;
                                    }
            
                                    QPushButton:hover {
                                        background-color: rgba(255, 255, 255, 50);
                                    }
                                """)

        self.board = [None] * 9

class DisappearingMode(GameStartedWindow):
    def __init__(self):
        super().__init__()

        self.player_O_button_tracker = []
        self.player_X_button_tracker = []

    def button_clicked(self):
        button = self.sender()
        
        if not button.property("Enabled"):
            return

        button.setProperty("Enabled", False)

        if self.current_player == "O":
            self.player_O_button_tracker.append(button)
        else:
            self.player_X_button_tracker.append(button)

        current_button_index = self.buttons.index(button)
        self.board[current_button_index] = self.current_player


        if self.current_player == "O" and len(self.player_O_button_tracker) > 3:
            # Remove the oldest button from player O's tracker
            oldest_button = self.player_O_button_tracker.pop(0)
            oldest_button_index = self.buttons.index(oldest_button)
            self.board[oldest_button_index] = None
            oldest_button.setProperty("Enabled", True)
            oldest_button.setIcon(QtGui.QIcon())
        elif self.current_player == "X" and len(self.player_X_button_tracker) > 3:
            # Remove the oldest button from player X's tracker
            oldest_button = self.player_X_button_tracker.pop(0)
            oldest_button_index = self.buttons.index(oldest_button)
            self.board[oldest_button_index] = None
            oldest_button.setProperty("Enabled", True)
            oldest_button.setIcon(QtGui.QIcon())

        if self.current_player == "O":
            print("Player O clicked the button!")
            button.setIcon(QtGui.QIcon("./assets/tictactoe_circle.png")) #Change to circle icon for player O
        else:
            print("Player X clicked the button!")
            button.setIcon(QtGui.QIcon("./assets/tictactoe_x.png")) #Change to cross icon for player X

        button.setIconSize(button.size())

        wining_result = self.check_for_win()

        if wining_result:
            for btn in self.buttons:
                btn.setStyleSheet("background-color: transparent; border: none;")
                btn.setProperty("Enabled", False)
            self.starting_label.setText(f"Player {self.current_player} has won!")
            return

        if self.current_player == "O":
            self.current_player = "X"
            self.starting_label.setText("Player X's turn")
            self.starting_label.setStyleSheet("color: red; font-size: 24px;")
        else:
            self.current_player = "O"
            self.starting_label.setText("Player O's turn")
            self.starting_label.setStyleSheet("color: #00BFFF; font-size: 24px;")

    def play_again(self):
        # Reset the game board and player turns
        super().play_again()
        self.player_O_button_tracker.clear()
        self.player_X_button_tracker.clear()


class ClassicVsAI(GameStartedWindow):
    #For future AI implementation using own neural network
    pass

class DisappearingVsAI(GameStartedWindow):
    #For future AI implementation using own neural network
    pass