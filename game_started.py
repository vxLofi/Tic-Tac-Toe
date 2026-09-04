from PySide6.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QMainWindow, QLabel, QPushButton, QStackedLayout, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6 import QtGui
from winning_logic import wining_logic

class GameStartedWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_player = "O"

        container = QWidget()
        self.setCentralWidget(container)
        self.layout = QVBoxLayout(container)

        self.label = QLabel("Game has started!")
        self.label.setStyleSheet("font-size: 24px;")
        self.label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.label)

        #Make the layout for the Tic-Tac-Toe board and buttons
        self.board_layout = QStackedLayout()
        self.board_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        self.layout.addLayout(self.board_layout) ##StackedLayout from "self.board" - Index 0

        #Add the Tic-Tac-Toe board image
        self.board = QLabel()
        self.board.setPixmap(QtGui.QPixmap("./tictactoe.png").scaled(600, 600))
        self.board.setAlignment(Qt.AlignCenter)
        self.board_layout.addWidget(self.board)

        #Add the buttons to the board
        self.buttons = []
        self.available_buttons = []
        self.board = [None] * 9 
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
                        self.available_buttons.append(button)
                        self.buttons.append(button)

        self.button_layout.setAlignment(Qt.AlignCenter)
        self.board_layout.addWidget(self.button_widget) #StackedLayout from "self.board" - Index 1
        self.board_layout.setCurrentIndex(1) #Buttons infront of the board image

        #Add the "Play Again" button and "Main Menu" button
        self.end_gamesbuttons_layout = QHBoxLayout()
        self.layout.addLayout(self.end_gamesbuttons_layout)
        #Play Again button
        self.play_again_button = QPushButton("Play Again")
        self.play_again_button.setStyleSheet("font-size: 24px;")
        self.play_again_button.clicked.connect(self.play_again)
        self.end_gamesbuttons_layout.addWidget(self.play_again_button)
        #Main Menu button
        self.main_menu_button = QPushButton("Main Menu")
        self.main_menu_button.setStyleSheet("font-size: 24px;")
        self.main_menu_button.clicked.connect(self.play_again)
        self.end_gamesbuttons_layout.addWidget(self.main_menu_button)
        
    def button_clicked(self):
        button = self.sender()

        if not button.property("Enabled"):
            return  # Ignore clicks on disabled buttons

        current_button_index = self.buttons.index(button) #Set index to the index of the button in buttons
        self.board[current_button_index] = self.current_player #Set the index of button clicked to player
        
        self.available_buttons.remove(button)  # Remove the clicked button from the available buttons list
        button.setStyleSheet("background-color: transparent; border: none;")
        button.setProperty("Enabled", False)  # Disable the button after it's clicked

        if self.current_player == "O":
            print("Player O clicked the button!")
            button.setIcon(QtGui.QIcon("./tictactoe_circle.png")) #Change to circle icon for player O
        else:
            print("Player X clicked the button!")
            button.setIcon(QtGui.QIcon("./tictactoe_x.png")) #Change to cross icon for player X

        button.setIconSize(button.size())

        results = wining_logic(self.current_player, self.board)
                        
        if results:
            for btn in self.buttons:
                btn.setStyleSheet("background-color: transparent; border: none;")
                btn.setProperty("Enabled", False)

            self.label.setText(results)
            return

        if not self.available_buttons:
            self.label.setText("Game Over! It's a draw!")
            self.label.setStyleSheet("color: white; font-size: 24px;")
            print("Game Over! It's a draw!")
            return

        if self.current_player == "O":
            self.current_player = "X"
            self.label.setText("Player X's turn")
            self.label.setStyleSheet("color: red; font-size: 24px;")
        else:
            self.current_player = "O"
            self.label.setText("Player O's turn")
            self.label.setStyleSheet("color: blue; font-size: 24px;")

    #Play Again button logic
    def play_again(self):
        self.player = 0
        self.label.setText("Player O's turn")

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

        self.available_buttons = self.buttons.copy()
       