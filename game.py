import math
from pathlib import Path
import random
import json

practice_board = [None, None, None, 'O', 'O', None, None, 'X', None]

def encode_board(board, player):
    encoded_board = []
    if player == "O":
        for square in board:
            if square == "O":
                encoded_board.append(1)
            elif square == "X":
                encoded_board.append(-1)
            else:
                encoded_board.append(0)
    else:
        for square in board:
            if square == "O":
                encoded_board.append(-1)
            elif square == "X":
                encoded_board.append(1)
            else:
                encoded_board.append(0)

    return tuple(encoded_board)

def layer(W, b, inputs):
    outputs = []
    for row, bias in zip(W, b):
        total = bias
        for w, x in zip(row, inputs):
            total += w * x
        outputs.append(total)
    return outputs

def relu(values):
    return [max(0, v) for v in values]

class TicTacToe():
    def __init__(self):
        self.possible_players = ["O", "X"]
        self.current_player = random.choice(self.possible_players)
        self.board = [None] * 9
        self.O_reward = 0
        self.X_reward = 0
        self.wins = 0
        self.losses=0
        self.draws=0

    def display(self):
        symbols = [square if square else " " for square in self.board]
        print(f" {symbols[0]} | {symbols[1]} | {symbols[2]} ")
        print("---+---+---")
        print(f" {symbols[3]} | {symbols[4]} | {symbols[5]} ")
        print("---+---+---")
        print(f" {symbols[6]} | {symbols[7]} | {symbols[8]} ")
        print()

    def legal_moves(self):
        legal_moves = [i for i, square in enumerate(self.board) if square is None]
        return legal_moves

 
    def make_move(self, square: int, encoder=None):
        self.O_reward = 0
        self.X_reward = 0

        self.board[square] = self.current_player

        if encoder is not None:
            encoder.update_board(self.current_player, square)

        results = self.check_winner()
        check_for_draw = self.is_draw()

        if results and self.current_player == "O":
            self.O_reward += 0.5
            self.X_reward -= 1
            return "win"
        elif results and self.current_player == "X":
            self.O_reward -= 1
            self.X_reward += 0.5
            return "loss"

        if check_for_draw:
            self.O_reward += 0.2
            self.X_reward += 0.2
            return "draw"


        if self.current_player == "O":
            self.current_player = "X"
            return      
        else:
            self.current_player = "O"
            return
        
    def check_winner(self):
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

    def is_draw(self):
        if None not in self.board:
            return True

class DissapearingBoardEncoder():
    def __init__(self, game):
        self.game = game
        self.O_tracker = []
        self.X_tracker = []

    def update_board(self, player, choice=None):
        if choice is not None:
            tracker = self.O_tracker if player == "O" else self.X_tracker
            tracker.append(choice)

            if len(tracker) > 3:
                oldest_move = tracker.pop(0)
                self.game.board[oldest_move] = None

        own_tracker = self.O_tracker if player == "O" else self.X_tracker
        opponent_tracker = self.X_tracker if player == "O" else self.O_tracker

        encoded_board = [0] * 9 

        for i, square in enumerate(own_tracker):
            encoded_board[square] = 4 - len(own_tracker) + i

        for i, square in enumerate(opponent_tracker):
            encoded_board[square] = -(4- len(opponent_tracker) + i)

        return tuple(encoded_board)

class Agent:
    #hvm = highest value move
    #lr = learning rate/alpha
    def __init__(self): 
        #Permanet Values
        #Epsilon Values
        self.epsilon = 0
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.999
        #----------------------------------------
        self.lr = 0.01
        self.q_table = {}
        self.gamma = 0.99
        self.net = NeuralNetwork()

    def load_weights(self, filename, O_filename):
        with open(filename) as f:
            data = json.load(f)
            self.net.W1, self.net.b1 = data["W1"], data["b1"]
            self.net.W2, self.net.b2 = data["W2"], data["b2"]

        with open(O_filename) as r:
            data = json.load(r)
            self.net.O_W1, self.net.O_b1 = data["W1"], data["b1"]
            self.net.O_W2, self.net.O_b2 = data["W2"], data["b2"]
        #----------------------------------------
    def choose_move(self, board, mover, state=None):
        # Get the list of legal moves available for the current player
        available_moves = game.legal_moves()

        if state is None:
            state = encode_board(board, mover)


        #Check if AI should explore
        if random.random() < self.epsilon:
            return random.choice(available_moves)

        move_scores = self.net.forward(state, mover)

        #Check for highest value move inside "available_moves"
        hvm = max(move_scores[i] for i in available_moves)
        #Check for highest value move index/indeces inside "available_moves"
        best_move_indices = [move_index for move_index in available_moves if move_scores[move_index] == hvm]

        return random.choice(best_move_indices)

    def learn(self, state, action, mover, reward, next_state, done):
        if done:
            target = reward
        else:
            scores = self.net.forward(next_state, mover)
            target = reward + self.gamma * max(scores[i] for i in range(9) if next_state[i] == 0)

        self.net.train_step(state, action, target, self.lr, mover)

class NeuralNetwork:
    def __init__(self):
        self.W1 = [[random.gauss(0, 0.1) for _ in range(9)] for _ in range(18)]
        self.b1 = [0.0] * 18

        self.W2 = [[random.gauss(0, 0.1) for _ in range(18)] for _ in range(9)]
        self.b2 = [0.0] * 9

        #Weights for opponent
        self.O_W1 = [[random.gauss(0, 0.1) for _ in range(9)] for _ in range(18)]
        self.O_b1 = [0.0] * 18

        self.O_W2 = [[random.gauss(0, 0.1) for _ in range(18)] for _ in range(9)]
        self.O_b2 = [0.0] * 9

    def forward(self, inputs, mover):
        if mover == "O":
            W1, b1 = self.W1, self.b1
            W2, b2 = self.W2, self.b2
        else:
            W1, b1 = self.O_W1, self.O_b1
            W2, b2 = self.O_W2, self.O_b2

        self.inputs = inputs
        hidden = layer(W1, b1, inputs)
        self.relu_layer = relu(hidden)
        return layer(W2, b2, self.relu_layer)

    def backward(self, action, error, mover):
        self.blames = []
        self.error = error
        if mover == "O":
            W2 = self.W2
        else:
            W2 = self.O_W2

        for i in range(18):
            blame = error * W2[action][i]
            if self.relu_layer[i] == 0:  
                blame = 0
            self.blames.append(blame)

    def update_weights(self, action, lr, mover):
        def clip_gradient(gradient):
            if not math.isfinite(gradient):
                raise ValueError(f"Invalid gradient: {gradient}")

            return max(-1.0, min(1.0, gradient))

        if mover == "O":
            W1, b1 = self.W1, self.b1
            W2, b2 = self.W2, self.b2
        else:
            W1, b1 = self.O_W1, self.O_b1
            W2, b2 = self.O_W2, self.O_b2

        for i in range(18):
            slope = self.error * self.relu_layer[i]
            W2[action][i] -= lr * clip_gradient(slope)

        b2[action] -= lr * clip_gradient(self.error)

        for i in range(18):
            for k in range(9):
                slope = self.blames[i] * self.inputs[k]
                W1[i][k] -= lr * clip_gradient(slope)

            b1[i] -= lr * clip_gradient(self.blames[i])

    def train_step(self, inputs, action, target, lr, mover):
        prediction = self.forward(inputs, mover)[action]
        self.backward(action, prediction - target, mover)
        self.update_weights(action, lr, mover)

class PopulationTournament:
    def __init__(self, population_size):
        self.population_size = population_size
        self.population = []

if __name__ == "__main__":
    game = TicTacToe()
    agent = Agent()
    nn = NeuralNetwork()
    encoder = DissapearingBoardEncoder(game)

    weight, O_weight = Path("latest_weights.json"), Path("latest_O_weights.json")

    if weight.exists() and O_weight.exists():
        agent.load_weights(weight, O_weight)

    def save_weights(net, filename, O_filename):
        data = {
            "W1": net.W1,
            "b1": net.b1,
            "W2": net.W2,
            "b2": net.b2
        }

        O_data = {
            "W1": net.O_W1,
            "b1": net.O_b1,
            "W2": net.O_W2,
            "b2": net.O_b2
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        with open(O_filename, "w") as f:
            json.dump(O_data, f, indent=4)

    iterations = 1000000
    report_every = 10000
    last = {"wins": 0, "losses": 0, "draws": 0, "illegal": 0}
    best_win_rate = 0

    game_mode = input("Enter game mode: \n1. Regular: 1\n2. Dissapearing: 2\n")

    for t in range(iterations):
        game.board = [None] * 9
        game.current_player = random.choice(game.possible_players)
        pending = None
        if (t + 1) % report_every == 0:
            wins = game.wins - last["wins"]
            losses = game.losses - last["losses"]
            draws = game.draws - last["draws"]
            print(f"Games {t + 1 - report_every + 1}-{t + 1} | "
                f"Wins {wins / report_every:.1%} | "
                f"Losses {losses / report_every:.1%} | "
                f"Draws {draws / report_every:.1%} | "
                f"Epsilon {agent.epsilon:.3f}")
            last = {"wins": game.wins, "losses": game.losses,
                    "draws": game.draws}

            if game_mode == "1":
                save_weights(agent.net, "latest_weights.json", "latest_O_weights.json")

            elif game_mode == "2":
                save_weights(agent.net, "latest_dissapearing_weights.json", "latest_O_dissapearing_weights.json")
                

        pending = {"O": None, "X": None}
        if game_mode == "1":
            while True:
                mover = game.current_player
                state = encode_board(game.board, mover)
                if pending[mover] is not None:
                    #Check who learns for this move
                    sta, cho = pending[mover]
                    agent.learn(sta, cho, mover, 0, state, False)

                # Choose a move based on the current state and player
                choice = agent.choose_move(game.board, mover)
                game_state = game.make_move(choice)
                # Store the pending transition for learning after the next move
                pending[mover] = (state, choice)

                # Check if the game has ended after the move using "game_state"
                if game_state in ("win", "loss", "draw"):
                    rewards = {"O": game.O_reward, "X": game.X_reward}
                    for player in ("O", "X"):
                        if pending[player] is not None:
                            sta, cho = pending[player]
                            agent.learn(sta, cho, player, rewards[player], encode_board(game.board, player), True)
                    if game_state == "win": game.wins += 1
                    elif game_state == "loss": game.losses += 1
                    elif game_state == "draw": game.draws += 1
                    agent.epsilon = max(agent.epsilon_min, agent.epsilon * agent.epsilon_decay)
                    break
        elif game_mode == "2":

            encoder.O_tracker.clear()
            encoder.X_tracker.clear()
            while True:
                mover = game.current_player
                state = encoder.update_board(mover)
                if pending[mover] is not None:
                    sta, cho = pending[mover]
                    agent.learn(sta, cho, mover, 0, state, False)

                choice = agent.choose_move(game.board, mover, state)
                game_state = game.make_move(choice, encoder)
                pending[mover] = (state, choice)
            
                if game_state in ("win", "loss", "draw"):
                    rewards = {"O": game.O_reward, "X": game.X_reward}
                    for player in ("O", "X"):
                        if pending[player] is not None:
                            sta, cho = pending[player]
                            agent.learn(sta, cho, player, rewards[player], encoder.update_board(player, choice), True)
                    if game_state == "win": game.wins += 1
                    elif game_state == "loss": game.losses += 1
                    elif game_state == "draw": game.draws += 1
                    agent.epsilon = max(agent.epsilon_min, agent.epsilon * agent.epsilon_decay)
                    break

    print("Total wins:", game.wins, "| losses:", game.losses, "| draws:", game.draws)