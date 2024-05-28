import random
import os
import copy

def clear_screen():
	"""
	Clears the terminal for Windows and Linux/MacOS.

	:return: None
	"""
	os.system('cls' if os.name == 'nt' else 'clear')


def print_rules():
	"""
	Prints the rules of the game.

	:return: None
	"""
	print("================= Rules =================")
	print("Connect 4 is a two-player game where the")
	print("objective is to get four of your pieces")
	print("in a row either horizontally, vertically")
	print("or diagonally. The game is played on a")
	print("6x7 grid. The first player to get four")
	print("pieces in a row wins the game. If the")
	print("grid is filled and no player has won,")
	print("the game is a draw.")
	print("=========================================")


def validate_input(prompt, valid_inputs):
	"""
	Repeatedly ask user for input until they enter an input
	within a set valid of options.

	:param prompt: The prompt to display to the user, string.
	:param valid_inputs: The range of values to accept, list
	:return: The user's input, string.
	"""

	#initialising choice variable with a garbage value (this will likely never be a valid input)
	choice = 893472

	#takes user input and compares it to the list of accepted possible inputs
	#if the input is invaid, inform the user and ask for a new one
	#if it is, return the input
	while choice not in valid_inputs:
		choice = input(prompt)
		choice.lower()
		if choice not in valid_inputs:
			print("Invalid input, please try again.")
	
	return choice


def create_board():
	"""
	Returns a 2D list of 6 rows and 7 columns to represent
	the game board. Default cell value is 0.

	:return: A 2D list of 6x7 dimensions.
	"""
	
	#initialises a matrix of 0s representing the empty board, and return it
	board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
	return board


def print_board(board):
	"""
	Prints the game board to the console.

	:param board: The game board, 2D list of 6x7 dimensions.
	:return: None
	"""
	#prints top section that does not change
	print("========== Connect4 =========")
	print("Player 1: X       Player 2: O")
	print("")
	print("  1   2   3   4   5   6   7")
	print(" --- --- --- --- --- --- ---")

	#create a temporary board, and loads in Xs, Os an empty spaces according to the numbers in the real board.
	tempboard = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
	for i in range(len(board)):
		for j in range(len(board[1])):
			if board[i][j] == 0:
				tempboard[i][j] = " "
			elif board[i][j] == 1:
				tempboard[i][j] = "X"
			else:
				tempboard[i][j] = "O"

	#prints each row of the temporary board with formatting
	for i in range(len(board)):
		print(f"| {tempboard[i][0]} | {tempboard[i][1]} | {tempboard[i][2]} | {tempboard[i][3]} | {tempboard[i][4]} | {tempboard[i][5]} | {tempboard[i][6]} |")
		print(" --- --- --- --- --- --- ---")

	#print bottom formatting
	print("=============================")

def drop_piece(board, player, column):
	"""
	Drops a piece into the game board in the given column.
	Please note that this function expects the column index
	to start at 1.

	:param board: The game board, 2D list of 6x7 dimensions.
	:param player: The player who is dropping the piece, int.
	:param column: The index of column to drop the piece into, int.
	:return: True if piece was successfully dropped, False if not.
	"""
	
	#goes down the chosen column until a piece or the bottom of the column is found,
	#then drops the current players piece one position above this and return true
	#if the row is full, return false
	if board[0][column-1] == 0:
		if board[1][column-1] != 0:
			board[0][column-1] = player
		elif board[2][column-1] != 0:
			board[1][column-1] = player
		elif board[3][column-1] != 0:
			board[2][column-1] = player
		elif board[4][column-1] != 0:
			board[3][column-1] = player
		elif board[5][column-1] != 0:
			board[4][column-1] = player
		elif board[5][column-1] == 0:
			board[5][column-1] = player
		
		return True
	else:
		return False


def execute_player_turn(player, board):
	"""
	Prompts user for a legal move given the current game board
	and executes the move.

	:return: Column that the piece was dropped into, int.
	"""
	
	#asks the current player to choose  column, verifies that the choice is within the board confines
	#then uses drop piece to drop the piece and verify if the piece has room to be dropped.
	#if not , asks again
	drop_success = False
	while drop_success == False:
		column_choice = int(validate_input("Player " + str(player) +", please enter the column you would like to drop your piece into: ", ["1", "2", "3", "4", "5", "6", "7"]))
		drop_success = drop_piece(board, player, column_choice)
		if drop_success == False:
			print("That column is full, please try again.")
	return column_choice


def end_of_game(board):
	"""
	Checks if the game has ended with a winner
	or a draw.

	:param board: The game board, 2D list of 6 rows x 7 columns.
	:return: 0 if game is not over, 1 if player 1 wins, 2 if player 2 wins, 3 if draw.
	"""
	
	#checking for horizontal 4-in-a-row
	for row in range(6):
		for col in range(4):
			if board[row][col] == 1 and board[row][col+1] == 1 and board[row][col+2] == 1 and board[row][col+3] == 1:
				return 1
			elif board[row][col] == 2 and board[row][col+1] == 2 and board[row][col+2] == 2 and board[row][col+3] == 2:
				return 2

	#checking for vertical 4-in-a-row
	for row in range(3):
		for col in range(7):
			if board[row][col] == 1 and board[row+1][col] == 1 and board[row+2][col] == 1 and board[row+3][col] == 1:
				return 1
			elif board[row][col] == 2 and board[row+1][col] == 2 and board[row+2][col] == 2 and board[row+3][col] == 2:
				return 2

	#checking for diagonal down 4-in-a-row
	for row in range(3):
		for col in range(4):
			if board[row][col] == 1 and board[row+1][col+1] == 1 and board[row+2][col+2] == 1 and board[row+3][col+3] == 1:
				return 1
			elif board[row][col] == 2 and board[row+1][col+1] == 2 and board[row+2][col+2] == 2 and board[row+3][col+3] == 2:
				return 2

	#checking for diagonal up 4-in-a-row
	for row in range(3):
		for col in range(3, 7):
			if board[row][col] == 1 and board[row+1][col-1] == 1 and board[row+2][col-2] == 1 and board[row+3][col-3] == 1:
				return 1
			elif board[row][col] == 2 and board[row+1][col-1] == 2 and board[row+2][col-2] == 2 and board[row+3][col-3] == 2:
				return 2

	#if no win is found, check if entire top row is full. If this is true and no previous checks 
	#found a win, then it must be a draw.
	if board[0][0] != 0 and board[0][1] != 0 and board[0][2] != 0 and board[0][3] != 0 and board[0][4] != 0 and board[0][5] != 0 and board[0][6] != 0:
		return 3

	#if no win or draw, return 0
	return 0


def local_2_player_game():
	"""
	Runs a local 2 player game of Connect 4.

	:return: None
	"""
	
	#initialising variables to be used
	previous_move = ""
	win = 0
	player = 1
	board = create_board()

	#runs until a win occurs
	while win == 0:
		clear_screen()
		print_board(board)
		print(previous_move)

		#executes player turn and saves the column choice to be printed
		last_choice = execute_player_turn(player, board)
		previous_move = "Player " + str(player) + " dropped a piece into column " + str(last_choice)

		#tests for end game conditions (player 1/2 wins, or draw), prints result and ends the while loop
		if end_of_game(board)== 1:
			clear_screen()
			print_board(board)
			print(previous_move)
			print("Player 1 wins!")
			win = 1
		elif end_of_game(board) == 2:
			clear_screen()
			print_board(board)
			print(previous_move)
			print("Player 2 wins!")
			win = 1
		elif end_of_game(board) == 3:
			clear_screen()
			print_board(board)
			print(previous_move)
			print("Draw")
			win = 1

		#alternates player turn
		if player == 1:
			player = 2
		else:
			player = 1


def main():
	"""
	Defines the main application loop.
    User chooses a type of game to play or to exit.

	:return: None
	"""
	
	#clears terminal and initialises variables
	clear_screen()
	quit = 0

	#runs until the user chooses quit or a game is finished
	while quit == 0:
		#printing startup menu
		clear_screen()
		print("=============== Main Menu ===============")
		print("Welcome to Connect 4!")
		print("Please pick one option by entering its number...")
		print("1. View rules")
		print("2. Play a local 2 player game")
		print("3. Play a game against the computer")
		print("4. Exit")
		print("=========================================")

		#making sure user picks a valid option from those given
		choice = validate_input("Enter your option here: ", [str(1), str(2), str(3), str(4)])
		choice = int(choice)

		#different functions run depending on the player choice on main menu
		if choice == 1:
			clear_screen()
			print_rules()
			input("Press enter to return to menu")
		elif choice == 2:
			local_2_player_game()
			quit = 1
		elif choice == 3:
			game_against_cpu()
			quit = 1
		elif choice == 4:
			clear_screen()
			print("Closing Connect 4...")
			quit = 1


def cpu_player_easy(board, player):
	"""
	Executes a move for the CPU on easy difficulty. This function 
	plays a randomly selected column.

	:param board: The game board, 2D list of 6x7 dimensions.
	:param player: The player whose turn it is, integer value of 1 or 2.
	:return: Column that the piece was dropped into, int.
	"""
	
	#uses random to pick a valid column, and uses drop piece function to drop it 
	#drop piece also ensures there is room in the column to drop the piece
	drop_success = False
	while drop_success == False:
		tempboard = copy.deepcopy(board)
		column_choice = random.randint(1,len(board[0]))
		drop_success = drop_piece(tempboard, player, column_choice)
		# if drop_success == False:
		# 	print("That column is full, please try again.")
	drop_piece(board, player, column_choice)
	return column_choice


def cpu_player_medium(board, player):
	"""
	Executes a move for the CPU on medium difficulty.
	It first checks for an immediate win and plays that move if possible. 
	If no immediate win is possible, it checks for an immediate win 
	for the opponent and blocks that move. If neither of these are 
	possible, it plays a random move.

	:param board: The game board, 2D list of 6x7 dimensions.
	:param player: The player whose turn it is, integer value of 1 or 2.
	:return: Column that the piece was dropped into, int.
	"""
	
	#tells the cpu which piece to search for when looking for an enemy win
	if player == 1:
		enemy = 2
	else:
		enemy = 1

	#checks are performed by creating a temporary board, dropping player or enemy piece 
	#in every column and using the end_of_game function to see if dropping that piece 
	#leads to a win or loss, then drops a piece in the real board as required

	#checking if player can win, if so, drop piece and return choice
	for i in range(1, len(board[0])+1):
		temp_board = copy.deepcopy(board)
		drop_piece(temp_board, player, i)
		if end_of_game(temp_board) == player:
			drop_piece(board, player, i)
			return i
			
	#checking if enemy can win, if so, drop piece to block and return choice
	for i in range(1, len(board[0])+1):
		temp_board = copy.deepcopy(board)
		drop_piece(temp_board, enemy, i)
		if end_of_game(temp_board) == enemy:
			drop_piece(board, player, i)
			return i
	
	#if cpu cannot win immediately or block an enemy win, use the easy cpu logic to drop in a random column
	drop_success = False
	while drop_success == False:
		tempboard = copy.deepcopy(board)
		column_choice = random.randint(1,len(board[0]))
		drop_success = drop_piece(tempboard, player, column_choice)
		# if drop_success == False:
		# 	print("That column is full, please try again.")
	drop_piece(board, player, column_choice)
	return column_choice

def cpu_player_hard(board, player):
	"""
	Executes a move for the CPU on hard difficulty.
	This function creates a copy of the board to simulate moves.
    
	Functions the same as the medium CPU: checks for a winning move, checks for a blocking move,
	but then before playing a random piece it checks if it can make a 3 in a row or block the
	opponent from making a 3 in a row. This should lead to more chances for the hard bot to run into
	4 in a row opportunities than the medium bot, and on average win more games. 

	:param board: The game board, 2D list of 6x7 dimensions.
	:param player: The player whose turn it is, integer value of 1 or 2.
	:return: Column that the piece was dropped into, int.
	"""
	#tells the cpu which piece to search for when looking for an enemy win
	if player == 1:
		enemy = 2
	else:
		enemy = 1

	#checking if player can win, if so, drop piece and return choice
	for i in range(1, len(board[0])+1):
		temp_board = copy.deepcopy(board)
		drop_test = drop_piece(temp_board, player, i)
		if end_of_game(temp_board) == player and drop_test == True:
			drop_piece(board, player, i)
			return i
			
	#checking if enemy can win, if so, drop piece to block and return choice
	for i in range(1, len(board[0])+1):
		temp_board = copy.deepcopy(board)
		drop_test = drop_piece(temp_board, enemy, i)
		if end_of_game(temp_board) == enemy and drop_test == True:
			drop_piece(board, player, i)
			return i
	

	#--------------------------------------------
	#here look for 3 in a row or block 3 in a row
	#checking if player can get 3, if so, drop piece and return choice
	for i in range(1, len(board[0])+1):
		temp_board = copy.deepcopy(board)
		drop_test = drop_piece(temp_board, player, i)
		if three_in_a_row(temp_board) == player and drop_test == True:
			drop_piece(board, player, i)
			return i
			
	#checking if enemy can get 3, if so, drop piece to block and return choice
	for i in range(1, len(board[0])+1):
		temp_board = copy.deepcopy(board)
		drop_test = drop_piece(temp_board, enemy, i)
		if three_in_a_row(temp_board) == enemy and drop_test == True:
			drop_piece(board, player, i)
			return i

	#--------------------------------------------
	#here look for 2 in a row
	#checking if player can get 2, if so, drop piece and return choice
	for i in range(1, len(board[0])+1):
		temp_board = copy.deepcopy(board)
		drop_test = drop_piece(temp_board, player, i)
		if two_in_a_row(temp_board) == player and drop_test == True:
			drop_piece(board, player, i)
			return i
			
	# #checking if enemy can get 2, if so, drop piece to block and return choice
	# for i in range(1, len(board[0])+1):
	# 	temp_board = copy.deepcopy(board)
	# 	drop_piece(temp_board, enemy, i)
	# 	if two_in_a_row(temp_board) == enemy:
	# 		drop_piece(board, player, i)
	# 		return i
	
	#--------------------------------------------



	#if none of the previous cases occur
	#execute a random move 
	drop_success = False
	while drop_success == False:
		tempboard = copy.deepcopy(board)
		column_choice = random.randint(1,len(board[0]))
		drop_success = drop_piece(tempboard, player, column_choice)
		# if drop_success == False:
		# 	print("That column is full, please try again.")
	drop_piece(board, player, column_choice)
	return column_choice


	#MAKING A 7


def game_against_cpu():
	"""
	Runs a game of Connect 4 against the computer.

	:return: None
	"""
	
	#allows user to choose a cpu difficulty
	clear_screen()
	print("====================")
	print("Difficulties:")
	print("1. Easy CPU")
	print("2. Medium CPU")
	print("3. Hard CPU")
	print("====================")
	diff = validate_input("Please enter the number corresponding to the desired difficulty: ", [str(1), str(2), str(3)])
	diff = int(diff)

	#initialising variables
	previous_move_player = ""
	previous_move_cpu = ""
	win = 0
	player = 1
	board = create_board()

	#main game loop
	while win == 0:
		clear_screen()
		print_board(board)
		print(previous_move_player)
		print(previous_move_cpu)
		
		#saves the players previous choice to print
		last_choice_player = execute_player_turn(player, board)
		previous_move_player = "Player " + str(player) + " dropped a piece into column " + str(last_choice_player)

		player = 2

		#depending on the chosen difficulty, execute a cpu move
		if diff == 1:
			last_choice_cpu = cpu_player_easy(board, 2)
		elif diff == 2:
			last_choice_cpu = cpu_player_medium(board, 2)
		elif diff == 3:
			last_choice_cpu = cpu_player_hard(board, 2)

		#saves cpu move to be printed
		previous_move_cpu = "The CPU dropped a piece into column " + str(last_choice_cpu)

		player = 1



		#testing for end of game, prints result and ends loop
		if end_of_game(board)== 1:
			clear_screen()
			print_board(board)
			print(previous_move_player)
			print(previous_move_cpu)
			print("Player 1 wins!")
			win = 1
		elif end_of_game(board) == 2:
			clear_screen()
			print_board(board)
			print(previous_move_player)
			print(previous_move_cpu)
			print("CPU wins!")
			win = 1
		elif end_of_game(board) == 3:
			clear_screen()
			print_board(board)
			print(previous_move_player)
			print(previous_move_cpu)
			print("Draw")
			win = 1


if __name__ == "__main__":
	main()
