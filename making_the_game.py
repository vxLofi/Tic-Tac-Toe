# Simple Tic Tac Toe in Python

board = [" " for _ in range(9)]

def print_board():
    print()
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print()

def check_win(player):
    # Winning combinations: rows, columns, diagonals
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    for r in wins:
        if board[r[0]] == board[r[1]] == board[r[2]] == player:
            return True
    return False

def play_game():
    current_player = "X"
    for turn in range(9):
        print_board()
        choice = input(f"Player {current_player}, choose spot (1-9): ")
        
        if not choice.isdigit():
            print("Invalid input. Enter a number from 1 to 9.")
            continue
            
        spot = int(choice) - 1
        
        if spot < 0 or spot > 8 or board[spot] != " ":
            print("Invalid spot or already taken. Try again.")
            continue
            
        board[spot] = current_player
        
        if check_win(current_player):
            print_board()
            print(f"Player {current_player} wins!")
            return
            
        current_player = "O" if current_player == "X" else "X"
        
    print_board()
    print("It's a tie!")

if __name__ == "__main__":
    play_game()
