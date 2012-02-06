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
# Plays the game of tic-tac-toe against a human opponen

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
    )