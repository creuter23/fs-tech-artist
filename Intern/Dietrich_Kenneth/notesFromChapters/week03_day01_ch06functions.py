'''
Notes from Chapter 6: Functions
to make a function, call it
def instructions():
This is called a function definition, which defines what the function does, but
does not run the function itself.

Use docstrings (or document strings) to document functions
Ex:
"""This is a docstring"""

Abstraction: happens when you have a block of code put under a function. This way,
for the block of code to initiate, you just need to write the function.

Encapsulation: When no variable you create in a function, including its parameters,
can be directly accessed outside its function. This... is a good thing.

Scopes: represent different areas of your program that are separate from each other.

Global variable: Any variable that you create in the global scope.

Local Variable: Any variable you create insade a function.

#Planning a program example with tic tac toe
display the game instructions
determine who goes first
create an empty tic-tac-toe board
display the board
while nobody's won and it's not a tie
    if it's the human's turn
        get the human's move
        update the board with the move
    otherwise
        calculate the computer's move
        update the board with the move
    display the board
    switch turns
congratualate the winner or declare a tie



'''

# Tic-Tac-Toe
# Plays the game of tic-tac-toe against a human opponent

# global constants
# THE MAIN BASE OF THE GAME
X = "X"
O = "O"
EMPTY = " "
TIE = "TIE"
NUM_SQUARES = 9

# the display_instruct() Function

def display_instruct():
    """Display game instructions."""
    print(
    """
    Welcome to the greatest intellectual challenge of all time: Tic-Tac-Toe.
    This will be a showdown between your human brain and my silicon processor.
    
    You will make your move known by entering a number, 0 -8. The number
    will correspond to the board position as illistrated:
                    0 | 1 | 2
                    ---------
                    3 | 4 | 5
                    ---------
                    6 | 7 | 8
    Prepare yourself, human. The ultimate battle is about to begin. \n
    """
    
# the ask_yes_no() Function

def ask_yes_no(question):
    """Ask a yes or no question."""
    response = None
    while response not in ("y", "n"):
        response = input(question).lower()
    return response
    )
    
# the ask_number() Function

def ask_number(question, low, high):
    """Ask for a number within a range."""
    response = None
    while response not in range(low, high):
        response = int(input(question))
    return response

# the pieces() Function

def pieces():
    """Determine if player or computer goes first."""
    go_first = ask_yes_no("Do you require the first move? (y/n): ")
    if go_first == "y":
        print("\nThen take the first move. You will need it.")
        human = X
        computer = O
    else:
        print("\nYour bravery will be undoing... I will go first")
        computer = X
        human = O
    return computer, human

# the new_board() Function

def new_board():
    """Create new game board."""
    board = []
    for square in range(NUM_SQUARES):
            board.append(EMPTY)
    return board

# the display_board() Function

def display_board(board):
    """Display game board on screen."""
    print(*\n\t*, board[0], "|", board[2])
    print("\t", "---------")
    print("\t", board[3], "|", board[4], "|", board[5])
    print("\t", "---------")
    print("\t", board[6], "|", board[7], "|", board[8], "\n")
    
# the leval_moves() Function

def legal_moves(board):
    """Create list of legal moves."""
    moves = []
    for square in range(NUM_SQUARES):
        if board[square] == EMPTY:
            moves.append(square)
    return moves

# the winner() Function

def winner(board):
    """Determine the game winner."""
    WAYS_TO_WIN = ((0, 1, 2),
                   (3, 4, 5),
                   (6, 7, 8),
                   (0, 3, 6),
                   (1, 4, 7),
                   (2, 5, 8),
                   (0, 4, 8),
                   (2, 4, 6))
    for row in WAYS_TO_WIN:
        if board[row[0]] == board[row[1]] == board[row[2]] != EMPTY:
            winner = board [row[0]]
            return winner
    if EMPTY not in board:
        return TIE
    return None

# the human_move() Function

def human_move(board, human):
    """Get human move."""
    legal = legal_moves(board)
    move = None
    while move not in legal:
        move = ask_number("Where will you move? (0 - 8):", 0, NUM_SQUARES)
        if move not in legal:
            print("\nThat square is already occupied, foolish human. Choose another.\n")
        print("Fine...")
        return move
    
# the computer_move() Function

def computer_move(board, computer, human):
    """Make computer move."""
    # make a copy to work with since function will be changing list
    board = board[:]
    # the best positions to have, in order
    BEST_MOVES = (4, 0, 2, 6, 8, 1, 3, 5, 7)
    
    print("I shall take square number", end=" ")
    
    # if computer can win, take that move
    for move in legal_moves(board):
        board[move] = computer
        if winner(board) == computer:
            print(move)
            return move
        # done checking this move, undo it
        board[move] = EMPTY
        
    # if human can win, block that move
    for move in legal_moves(board):
        board[move] = human
        if winner(board) == human:
            print(move)
            return move
        # done checking this move, undo it
        board[move] = EMPTY
    
    # since no one can win on the next move, pick best open square
    for move in BEST_MOVES:
        if move in legal_moves(board):
            print(move)
            return move

# the next_turn() Function

def next_turn(turn):
    """Switch turns."""
    if turn == X:
        return O
    else:
        return X
    
# the congrat_winner() function

def congrat_winner(the_winner, computer, human):
    """Congratulate the winner."""
    if the_winner != TIE:
        print(the_winner, "won!\n")
    else:
        print("It's a tie!\n")
        
    if the_winner == computer:
        print("As I predicted, human, I am triumphant once more. \n" \
              "Proof that computers are superior to humans in all regards.")
        
    elif the_winner == human:
        print("No, no! It cannot be! Somehow you tricked me, human. \n" \
              "But never again! I, the computer, so sear it!")
        
    elif the_winner == TIE:
        print("You were most lucky, human, and somehow managedto tie me. \n" \
              "Celebrate today... for this is the best you will ever achieve.")
        
# the main() Function
def main():
    display_instruct()
    computer, human = pieces()
    turn = X
    board = new_board()
    display_board(board)
    
    while not winner(board):
        if turn == human:
            move = human_move(board, human)
            board[move] = human
        else:
            move = computer_move(board, computer, human)
            board[move] = computer
        display_board(board)
        turn = next_turn(turn)
        
    the_winner = winner(board)
    congrat_winner(the_winner, computer, human)
    
# start the program
main()
input("\n\nPress the enter key to quit.")
