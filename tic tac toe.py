def print_board(board):
    """Print the current state of the board."""
    for row in board:
        print(" | ".join(row))
        print("-" * 10)

def check_winner(board, player):
    """Check if the given player has won the game."""
    # Check rows
    for row in board:
        if all([cell == player for cell in row]):
            return True

    # Check columns
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True

    # Check diagonals
    if all([board[i][i] == player for i in range(3)]):
        return True
    if all([board[i][2 - i] == player for i in range(3)]):
        return True

    return False

def check_draw(board):
    """Check if the game is a draw."""
    for row in board:
        if " " in row:
            return False
    return True

def get_move(player):
    """Get the player's move."""
    while True:
        try:
            move = int(input("Player {}, enter your move (1-9): ".format(player))) - 1
            if move < 0 or move >= 9:
                print("Invalid move. Please try again.")
                continue
            return move
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")

def main():
    # Initialize the board
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    current_player = 0

    while True:
        print_board(board)
        move = get_move(players[current_player])
        row, col = divmod(move, 3)

        if board[row][col] != " ":
            print("This cell is already taken. Please try again.")
            continue

        board[row][col] = players[current_player]

        if check_winner(board, players[current_player]):
            print_board(board)
            print("Player {} wins!".format(players[current_player]))
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = 1 - current_player

if __name__ == "__main__":
    main()
