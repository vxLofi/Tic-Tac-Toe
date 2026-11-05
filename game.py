import math
from pathlib import Path
import random
import json
import copy
import time

practice_board = [None, None, None, 'O', 'O', None, None, 'X', None]

# 1 = regular, 2 = disappearing (set in __main__, read by every function)
game_mode = 1

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

class TicTacToe:
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

    def legal_moves(self, board=None):
        if board is None:
            board = self.board
        legal_moves = [i for i, square in enumerate(board) if square is None]
        return legal_moves

 
    def make_move(self, square: int, mover = None, encoder=None):
        self.O_reward = 0
        self.X_reward = 0

        if mover is None:
            mover = self.current_player

        self.board[square] = mover

        if encoder is not None:
            encoder.update_board(mover, square)

        results = self.check_winner(mover)
        check_for_draw = self.is_draw()

        if results and mover == "O":
            self.O_reward += 1
            self.X_reward -= 1
            return "win"
        elif results and mover == "X":
            self.O_reward -= 1
            self.X_reward += 1
            return "loss"

        if check_for_draw:
            self.O_reward += 0.2
            self.X_reward += 0.2
            return "draw"


        if mover == "O":
            self.current_player = "X"
            return      
        else:
            self.current_player = "O"
            return
        
    def check_winner(self, mover):
        WINS = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], #Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8], #Vertical
        [0, 4, 8], [2, 4, 6]             #Diagonal
    ]
        for winning_combination in WINS:
            if self.board[winning_combination[0]] == self.board[winning_combination[1]] == self.board[winning_combination[2]] == mover:
                return winning_combination
        else:
            return False

    def is_draw(self):
        if None not in self.board:
            return True

class DisappearingBoardEncoder:
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
        self.epsilon = 1.0
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.999
        if game_mode == 2: #Disappearing explores for longer
            self.epsilon_min = 0.1
            self.epsilon_decay = 0.9995
        #----------------------------------------
        self.lr = 0.01
        self.q_table = {}
        self.gamma = 0.99
        self.net = NeuralNetwork()
        self.personal_stats = {"wins": 0, "losses": 0, "draws": 0}

    def load_weights(self, filename):
        with open(filename) as f:
            data = json.load(f)

        n = len([key for key in data if key.startswith("W")]) #W1 ... Wn
        weights = [data[f"W{i + 1}"] for i in range(n)]
        biases = [data[f"b{i + 1}"] for i in range(n)]

        #Only load it if it was saved for the same layout as the current network
        sizes = (len(weights[0][0]),) + tuple(len(b) for b in biases)
        if sizes != self.net.sizes:
            print(f"Skipped {filename}: it was saved for layout {sizes} but the network is {self.net.sizes}")
            return

        self.net.Weights, self.net.biases = weights, biases

        #----------------------------------------
    def choose_move(self, game, mover, state=None, evaluation=False):
        # Get the list of legal moves available for the current player
        available_moves = game.legal_moves()

        if state is None:
            state = encode_board(game.board, mover)


        #Check if AI should explore
        if not evaluation and random.random() < self.epsilon:
            return random.choice(available_moves)

        move_scores = self.net.forward(state)

        #Check for highest value move inside "available_moves"
        hvm = max(move_scores[i] for i in available_moves)
        #Check for highest value move index/indeces inside "available_moves"
        best_move_indices = [move_index for move_index in available_moves if move_scores[move_index] == hvm]

        return random.choice(best_move_indices)

    def learn(self, state, action, reward, next_state, done):
        if done:
            target = reward
        else:
            scores = self.net.forward(next_state)
            target = reward + self.gamma * max(scores[i] for i in range(9) if next_state[i] == 0)

        self.net.train_step(state, action, target, self.lr)

class NeuralNetwork:
    def __init__(self):
        sizes = {"Classic": [9, 18, 9], "Disappearing": [9, 32, 32, 9]} #Define the network sizes for different game modes

        self.Weights = []
        self.biases = []

        layers = sizes["Classic" if game_mode == 1 else "Disappearing"] #Initialize the network layers based on the game mode
        self.sizes = tuple(layers)
        

        for i in range(len(layers) - 1):
            self.Weights.append([[random.gauss(0, 0.1) for _ in range(layers[i])] for _ in range(layers[i+1])])
            self.biases.append([0.0] * layers[i+1])


    def forward(self, inputs):
        self.activations = [inputs]
        x = inputs
        for i in range(len(self.Weights)):
            x = layer(self.Weights[i], self.biases[i], x)
            if i < len(self.Weights) - 1:
                x = relu(x)
            self.activations.append(x)
        output = x  
        return output

    def backward(self, action, error):
        self.error = error
        self.blames = [None] * len(self.Weights)
 
        last_blames = [0.0] * len(self.biases[-1])
        last_blames[action] = error
        self.blames[-1] = last_blames
 
        for i in reversed(range(1, len(self.Weights))):
            W = self.Weights[i]
            layer_input = self.activations[i]
            blames_below = []
            for k in range(len(layer_input)):
                blame = 0.0
                for j in range(len(W)):
                    blame += self.blames[i][j] * W[j][k]
                if layer_input[k] == 0: 
                    blame = 0.0
                blames_below.append(blame)
            self.blames[i - 1] = blames_below

    def update_weights(self, lr):
        def clip_gradient(gradient):
            if not math.isfinite(gradient):
                raise ValueError(f"Invalid gradient: {gradient}")
 
            return max(-1.0, min(1.0, gradient))
 
        for i in range(len(self.Weights)):
            W, b = self.Weights[i], self.biases[i]
            layer_input = self.activations[i]
 
            for j in range(len(W)):
                for k in range(len(layer_input)):
                    W[j][k] -= lr * clip_gradient(self.blames[i][j] * layer_input[k])
 
                b[j] -= lr * clip_gradient(self.blames[i][j])

    def train_step(self, inputs, action, target, lr):
        prediction = self.forward(inputs)[action]
        self.backward(action, prediction - target)
        self.update_weights(lr)

class Evaluator:
    def __init__(self, game, cache=None):
        self.game = game
        self.player = None
        self.opponent = None
        self.score_cache = cache if cache is not None else {}
        self.best_move = None

    def set_players(self):
        self.player = self.game.current_player
        self.opponent = "X" if self.player == "O" else "O"

    def evaluate(self, board):
        WINS = [
                [0, 1, 2], [3, 4, 5], [6, 7, 8], #Horizontal
                [0, 3, 6], [1, 4, 7], [2, 5, 8], #Vertical
                [0, 4, 8], [2, 4, 6]             #Diagonal
            ]
        for winning_combination in WINS:
            if board[winning_combination[0]] == board[winning_combination[1]] == board[winning_combination[2]] == self.player:
                return 1

            if board[winning_combination[0]] == board[winning_combination[1]] == board[winning_combination[2]] == self.opponent:
                return -1

        return 0

    def minmax(self, board, depth, isMax, alpha=float('-inf'), beta=float('inf')):
        score = self.evaluate(board)

        if score == 1:
            return score - depth * 0.1

        if score == -1:
            return score + depth * 0.1

        if None not in board:
            return 0

        if isMax:
            best = float('-inf')
            for i in range(9):
                if board[i] is None:
                    board[i] = self.player
                    best = max(best, self.minmax(board, depth + 1, False, alpha, beta))
                    board[i] = None
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
            return best
        else:
            best = float('inf')
            for i in range(9):
                if board[i] is None:
                    board[i] = self.opponent
                    best = min(best, self.minmax(board, depth + 1, True, alpha, beta))
                    board[i] = None
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
            return best

    def evaluate_move(self, board, ai_choice):
        self.set_players()
        cache_key = (tuple(board), self.player)

        if cache_key not in self.score_cache:
            move_scores = {}
        
            for i in range(9):
                if board[i] is None:
                    board[i] = self.player
                    move_scores[i] = self.minmax(board, 0, False)
                    board[i] = None
            self.score_cache[cache_key] = move_scores

        move_scores = self.score_cache[cache_key]

        best_score = max(move_scores.values())
        chosen_score = move_scores[ai_choice]
        reward = (chosen_score - best_score) / 2
        self.best_move = max(move_scores, key=move_scores.get)

        return reward if reward != 0 else 0.2

    def get_best_move(self, board):
        self.set_players()
        cache_key = (tuple(board), self.player)

        if cache_key not in self.score_cache:
            move_scores = {}
        
            for i in range(9):
                if board[i] is None:
                    board[i] = self.player
                    move_scores[i] = self.minmax(board, 0, False)
                    board[i] = None
            self.score_cache[cache_key] = move_scores

        move_scores = self.score_cache[cache_key]
        best_score = max(move_scores.values())
        best_moves = [move for move, score in move_scores.items() if score == best_score]
        return random.choice(best_moves)

class PopulationTournament:
    def __init__(self, population_size, iterations_per_generation):
        self.population_size = population_size
        self.iterations_per_generation = iterations_per_generation
        self.population = [Agent() for _ in range(population_size)]

        self.minmax_cache = {}

        self.minmax_queue = self.population.copy()

    def train_classic(self):
        if not self.minmax_queue:
            self.minmax_queue = self.population.copy()

        minmax_agent = random.choice(self.minmax_queue)
        self.minmax_queue.remove(minmax_agent)

        shuffled_population = [agent for agent in self.population if agent != minmax_agent]
        random.shuffle(shuffled_population)
        pairs = [(shuffled_population[i], shuffled_population[i + 1]) for i in range(0, len(shuffled_population) -1, 2)]
        pairs.append((minmax_agent, None))
        for generation in range(self.iterations_per_generation):
            for agent1, agent2 in pairs:
                if agent2 is None:
                    self.agent_vs_minmax(agent1)
                else:
                    self.agent_vs_agent(agent1, agent2)

    def train_disappearing(self):
        shuffled_population = self.population.copy()
        random.shuffle(shuffled_population)
        pairs = [(shuffled_population[i], shuffled_population[i + 1]) for i in range(0, len(shuffled_population) -1, 2)]
        for generation in range(self.iterations_per_generation):
            for agent1, agent2 in pairs:
                self.agent_vs_agent(agent1, agent2)

    def agent_vs_agent(self, agent1, agent2):
        agentO = agent1
        agentX = agent2
        pending = {"O": None, "X": None}
        game = TicTacToe()
        evaluator = Evaluator(game, self.minmax_cache)
        if game_mode == 2:
            encoder = DisappearingBoardEncoder(game)
            moves = 0
            while True:
                if game.current_player == "O":
                    agent = agentO
                    mover = "O"
                else:
                    agent = agentX
                    mover = "X"
                state = encoder.update_board(mover)
                if pending[mover] is not None:
                    sta, cho = pending[mover]
                    agent.learn(sta, cho, 0, state, False)

                if moves < 1: #Random first move in training so games start from different positions
                    choice = random.choice(game.legal_moves())
                else:
                    choice = agent.choose_move(game, mover, state)
                game_state = game.make_move(choice, mover, encoder)
                pending[mover] = (state, choice)

                moves += 1
                if game_state is None and moves >= 40:
                    game_state = "draw"
            
                if game_state in ("win", "loss", "draw"):
                    rewards = {"O": game.O_reward, "X": game.X_reward}
                    for player in ("O", "X"):
                        if pending[player] is not None:
                            sta, cho = pending[player]
                            learning_agent = agentO if player == "O" else agentX
                            learning_agent.learn(sta, cho, rewards[player], state, True)
                    if game_state == "win": game.wins += 1
                    elif game_state == "loss": game.losses += 1
                    elif game_state == "draw": game.draws += 1
                    for learning_agent in (agentO, agentX):
                        learning_agent.epsilon = max(learning_agent.epsilon_min, learning_agent.epsilon * learning_agent.epsilon_decay)
                    break
            
        else:
            moves = 0
            while True:
                if game.current_player == "O":
                    agent = agentO
                    mover = "O"
                else:
                    agent = agentX
                    mover = "X"
                state = encode_board(game.board, mover)
                if pending[mover] is not None:
                    #Check who learns for this move
                    sta, cho, rew = pending[mover]
                    agent.learn(sta, cho, rew, state, False)

                choice = agent.choose_move(game, mover)
                reward = evaluator.evaluate_move(game.board, choice)
                game_state = game.make_move(choice, mover)
                pending[mover] = (state, choice, reward)

                moves += 1
                if moves >= 25:
                    game_state = "draw"

                if game_state in ("win", "loss", "draw"):
                    rewards = {"O": game.O_reward, "X": game.X_reward}
                    for player in ("O", "X"):
                        if pending[player] is not None:
                            sta, cho, rew = pending[player]
                            learning_agent = agentO if player == "O" else agentX
                            learning_agent.learn(sta, cho, rewards[player] + rew, encode_board(game.board, player), True)
                    if game_state == "win": game.wins += 1
                    elif game_state == "loss": game.losses += 1
                    elif game_state == "draw": game.draws += 1
                    for learning_agent in (agentO, agentX):
                        learning_agent.epsilon = max(learning_agent.epsilon_min, learning_agent.epsilon * learning_agent.epsilon_decay)
                    break

    def agent_vs_minmax(self, agent1):
        agent = agent1
        pending = [None]
        game = TicTacToe()
        evaluator = Evaluator(game, self.minmax_cache)

        while True:
            mover = game.current_player
            state = encode_board(game.board, mover)
            if mover == "O":
                if pending[0] is not None:
                    sta, cho, rew = pending[0]
                    agent.learn(sta, cho, rew, state, False)
                choice = agent.choose_move(game, mover)
                reward = evaluator.evaluate_move(game.board, choice)
                pending[0] = (state, choice, reward)
            else:
                choice = evaluator.get_best_move(game.board)

            game_state = game.make_move(choice, mover)

            if game_state in ("win", "loss", "draw"):
                reward = game.O_reward
                if pending[0] is not None:
                    sta, cho, rew = pending[0]
                    agent.learn(sta, cho, reward + rew, encode_board(game.board, mover), True)
                if game_state == "win": game.wins += 1
                elif game_state == "loss": game.losses += 1
                elif game_state == "draw": game.draws += 1
                agent.epsilon = max(agent.epsilon_min, agent.epsilon * agent.epsilon_decay)
                break

    def evaluation(self):
        scores = {agent: 0 for agent in self.population}
        if game_mode == 1:
            for agent in self.population:
                for game_num in range(100): # Evaluate each agent against MnMax teacher
                    game = TicTacToe()
                    evaluator = Evaluator(game, self.minmax_cache)
                    mover = "X"
                    agent_player = "O"
                    while True:

                        if mover == agent_player:
                            choice = agent.choose_move(game, agent_player, None, True)
                        else:
                            choice = evaluator.get_best_move(game.board)

                        game_state = game.make_move(choice, mover)

                        if game_state in ("win", "loss", "draw"):
                            if game_state == "win" and mover == agent_player:
                                scores[agent] += 1
                                agent.personal_stats["wins"] += 1
                            elif game_state == "draw":
                                scores[agent] += 0.5
                                agent.personal_stats["draws"] += 1
                            else:
                                agent.personal_stats["losses"] += 1
                            break

                        mover = game.current_player
        else:
            for agent in self.population:
                for game_num in range(100): #Evaluate by playing against each other
                    game = TicTacToe()
                    mover = "X" if game_num % 2 == 0 else "O" #Alternate who moves first
                    agent_player = "O"
                    encoder = DisappearingBoardEncoder(game)
                    moves = 0
                    while True:
                        state = encoder.update_board(mover)
                        if moves < 1: #First move of every evaluation game is random
                            choice = random.choice(game.legal_moves())
                        elif mover == agent_player:
                            choice = agent.choose_move(game, agent_player, state, True)
                        else:
                            choice = self.population[(self.population.index(agent) + 1) % len(self.population)].choose_move(game, mover, state, True)

                        game_state = game.make_move(choice, mover, encoder)
                        moves += 1
                        if game_state is None and moves >= 40:
                            game_state = "draw"

                        if game_state in ("win", "loss", "draw"):
                            if game_state == "win" and mover == agent_player:
                                scores[agent] += 1
                                agent.personal_stats["wins"] += 1
                            elif game_state == "draw":
                                scores[agent] += 0.5
                                agent.personal_stats["draws"] += 1
                            else:
                                agent.personal_stats["losses"] += 1
                            break

                        mover = game.current_player

        self.update_population(scores)

    def update_population(self, scores):
        ranked_agents = sorted(self.population, key=lambda agent: scores[agent], reverse=True)

        best_agent = ranked_agents[0]
        worst_agents = ranked_agents[-2:]

        mutation_strength = 0.01

        for agent in worst_agents:
            for i in range(len(agent.net.Weights)):
                agent.net.Weights[i] = copy.deepcopy(best_agent.net.Weights[i])
                agent.net.biases[i] = copy.deepcopy(best_agent.net.biases[i])

        for row in agent.net.Weights[i]:
            for k in range(len(row)):
                row[k] += random.gauss(0, mutation_strength)
        for k in range(len(agent.net.biases[i])):
            agent.net.biases[i][k] += random.gauss(0, mutation_strength) 

        self.save_weights()

    def run(self, iteration):
        percentages = []
        self.train_classic() if game_mode == 1 else self.train_disappearing()

        if (iteration + 1) % 10 == 0:
            print("Starting evaluation...")
            self.evaluation()

            for agent in self.population:
                print(f"Agent {self.population.index(agent)}: Wins: {agent.personal_stats['wins']}, Losses: {agent.personal_stats['losses']}, Draws: {agent.personal_stats['draws']}")
            
                total_games = agent.personal_stats['wins'] + agent.personal_stats['losses'] + agent.personal_stats['draws']
                if total_games > 0:
                    draw_percentage = (agent.personal_stats['draws'] / total_games) * 100
                else:
                    draw_percentage = 0
                percentages.append(draw_percentage)

                for stat in agent.personal_stats:
                    agent.personal_stats[stat] = 0

        return percentages

    def save_weights(self):
        for agent in self.population:
            data = {}
            for i in range(len(agent.net.Weights)):
                data[f"W{i + 1}"] = agent.net.Weights[i]
                data[f"b{i + 1}"] = agent.net.biases[i]


            if game_mode == 1:
                with open(f"agent_{self.population.index(agent)+1}_weights.json", "w") as f:
                    json.dump(data, f, indent=4)
            else:
                with open(f"agent_{self.population.index(agent)+1}_disappearing_weights.json", "w") as f:
                    json.dump(data, f, indent=4)

    def load_weights(self, filename):
        with open(filename) as f:
            data = json.load(f)

        n = len([key for key in data if key.startswith("W")]) #W1 ... Wn
        weights = [data[f"W{i + 1}"] for i in range(n)]
        biases = [data[f"b{i + 1}"] for i in range(n)]

        #Only load it if it was saved for the same layout as the current network
        sizes = (len(weights[0][0]),) + tuple(len(b) for b in biases)
        if sizes != self.net.sizes:
            print(f"Skipped {filename}: it was saved for layout {sizes} but the network is {self.net.sizes}")
            return

        self.net.Weights, self.net.biases = weights, biases

if __name__ == "__main__":
    #Pick the mode first, the agents below read game_mode when they are created
    game_mode = int(input("Enter game mode: \n1. Regular: 1\n2. Disappearing: 2\n"))

    train = PopulationTournament(6, 100)

    iterations = 1000
    report_every = 1
    last = {"wins": 0, "losses": 0, "draws": 0, "illegal": 0}
    best_win_rate = 0
    done = False


    #train.load_weights()
    while True:
        for t in range(iterations):
            print(f"Starting iteration {t + 1}")
                    
            if game_mode == 1:
                results = train.run(t)

                if results:
                    if all(result == 100 for result in results):
                        print("All agents have achieved a draw rate above 98%. Saving weights...")
                        train.save_weights()
                        done = True
                        break
            elif game_mode == 2:
                results = train.run(t)

            if done:
                break

        break