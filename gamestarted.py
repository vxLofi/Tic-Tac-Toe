from PySide6.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QMainWindow, QLabel, QPushButton, QStackedLayout, QVBoxLayout, QWidget
from PySide6.QtCore import QPropertyAnimation, Qt
from PySide6 import QtGui
import random
from pathlib import Path
import game as ai
from game import Agent, encode_board

def pick_random_file(folder_path):
    path = Path(folder_path)

    files = [f for f in path.iterdir() if f.is_file() and f.suffix == ".json"]
    chosen = random.choice(files)
    print(chosen)

    return chosen

class GameStartedWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.possible_players = ['O', 'X']

        self.current_player = random.choice(self.possible_players)
        self.buttons = []
        self.board = [None] * 9

        container = QWidget()
        self.setCentralWidget(container)
        self.layout = QVBoxLayout(container)

        self.starting_widgets()

        self.add_buttons()

    def starting_widgets(self):
        # Add a label to indicate the game has started
        self.starting_label = QLabel(f"Player {self.current_player}'s turn")
        if self.current_player == "O":
            self.starting_label.setStyleSheet("color: #00BFFF; font-size: 24px;")
        else:
            self.starting_label.setStyleSheet("color: red; font-size: 24px;")
        self.starting_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.starting_label)

        #Make the layout for the Tic-Tac-Toe board and buttons
        self.board_layout = QStackedLayout()
        self.board_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        self.layout.addLayout(self.board_layout) #StackedLayout from "self.board" - Index 0

        #Add the Tic-Tac-Toe board image
        self.board_image = QLabel()
        self.board_image.setPixmap(QtGui.QPixmap(str(Path(__file__).parent / "assets" / "tictactoe.png")).scaled(600, 600))
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
            button.setIcon(QtGui.QIcon(str(Path(__file__).parent / "assets" / "tictactoe_circle.png"))) #Change to circle icon for player O
        else:
            print("Player X clicked the button!")
            button.setIcon(QtGui.QIcon(str(Path(__file__).parent / "assets" / "tictactoe_x.png"))) #Change to cross icon for player X

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
        self.X_tracker = []
        self.O_tracker = []

    def button_clicked(self):
        button = self.sender()
        
        if not button.property("Enabled"):
            return

        button.setProperty("Enabled", False)

        if self.current_player == "O":
            self.player_O_button_tracker.append(button)
            self.O_tracker.append(self.buttons.index(button))
        else:
            self.player_X_button_tracker.append(button)
            self.X_tracker.append(self.buttons.index(button))

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
            button.setIcon(QtGui.QIcon(str(Path(__file__).parent / "assets" / "tictactoe_circle.png"))) #Change to circle icon for player O
        else:
            print("Player X clicked the button!")
            button.setIcon(QtGui.QIcon(str(Path(__file__).parent / "assets" / "tictactoe_x.png"))) #Change to cross icon for player X

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

        print("Current Board State:", self.board)

    def play_again(self):
        # Reset the game board and player turns
        super().play_again()
        self.player_O_button_tracker.clear()
        self.player_X_button_tracker.clear()


class ClassicVsAI(GameStartedWindow):
    def __init__(self):
        super().__init__()
        self.agent = Agent()
        #self.agent.load_weights(str(Path(__file__).parent / "weights for classic" / "latest_weights.json"), str(Path(__file__).parent / "weights for classic" / "latest_O_weights.json"))
        #self.agent.load_weights("tictactoe/weights for classic/latest_O_weights.json", "tictactoe/weights for classic/latest_weights.json")
        self.agent.load_weights(pick_random_file("tictactoe/weights for classic"))
        self.current_player = "O"
        self.starting_label.setText("Player O's turn")
        self.starting_label.setStyleSheet("color: #00BFFF; font-size: 24px;")

    def button_clicked(self):
        super().button_clicked()
        if self.current_player == "X":
            choice = self.choose_move(self.board, self.current_player)
            self.buttons[choice].click()

        print("Current Board State:", self.board)

    def choose_move(self, board, mover):
                # Get the list of legal moves available for the current player
        available_moves = self.legal_moves()
        state = encode_board(board, mover)

        move_scores = self.agent.net.forward(state)

        #Check for highest value move inside "available_moves"
        hvm = max(move_scores[i] for i in available_moves)
        #Check for highest value move index/indeces inside "available_moves"
        best_move_indices = [move_index for move_index in available_moves if move_scores[move_index] == hvm]

        return random.choice(best_move_indices)

    def legal_moves(self):
        legal_moves = [i for i, square in enumerate(self.board) if square is None]
        return legal_moves

    def play_again(self):
        super().play_again()
        self.agent.load_weights(pick_random_file("tictactoe/weights for classic"))

class DisappearingVsAI(DisappearingMode, ClassicVsAI):
    def __init__(self):
        super().__init__()
        ai.game_mode = 2
        self.agent = Agent()
        #self.agent.load_weights(str(Path(__file__).parent / "weights for disappearing" / "latest_dissapearing_weights.json"), str(Path(__file__).parent / "weights for disappearing" / "latest_O_dissapearing_weights.json"))
        self.current_player = "O"
        self.agent.load_weights(pick_random_file("tictactoe/weights for disappearing"))
        self.starting_label.setText("Player O's turn")
        self.starting_label.setStyleSheet("color: #00BFFF; font-size: 24px;")

    def button_clicked(self):
        super().button_clicked()
        if self.current_player == "X":
            choice = self.choose_move(self.current_player)
            self.buttons[choice].click()

    def choose_move(self, mover):
        available_moves = self.legal_moves()
        state = [0] * 9

        own_tracker = (self.player_O_button_tracker if mover == "O" else self.player_X_button_tracker)

        opponent_tracker = (self.player_X_button_tracker if mover == "O" else self.player_O_button_tracker)

        for i, button in enumerate(own_tracker):
            square = self.buttons.index(button)
            state[square] = 4 - len(own_tracker) + i

        for i, button in enumerate(opponent_tracker):
            square = self.buttons.index(button)
            state[square] = -(4 - len(opponent_tracker) + i)

        state = tuple(state)
        print(mover, state)

        move_scores = self.agent.net.forward(state)

        highest_score = max( move_scores[square] for square in available_moves)

        best_moves = [ square for square in available_moves if move_scores[square] == highest_score]

        return random.choice(best_moves)

    def legal_moves(self):
        return super().legal_moves()

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
        self.agent.load_weights(pick_random_file("tictactoe/weights for disappearing"))

    