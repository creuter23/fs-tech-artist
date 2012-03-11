#Guessing Game
#A scrit to pratice different if statments as well as importing the random module

import random

print "\nI'm thinking of a number between 1 and 100."
print "You have 10 tries to guess correctly."

#setting initial values
my_num = random.randrange(100) + 1
guess = int(raw_input("\nGuess my number. "))
num_guess = 1

#creating the loop
while (guess != my_num and num_guess < 10):
    if (guess > my_num):
        print "My number is lower than that. Guess again."
        guess = int(raw_input("Guess my number. "))
        num_guess += 1
        
    elif (guess < my_num):
        print "My number is higher than that. Guess again."
        guess = int(raw_input("Guess my number. "))
        num_guess += 1
        
if (guess == my_num and num_guess <10):
        print "\n\nYou guessed right! My number was", my_num, ". Congrats!"
        print "\nYou guessed it in", num_guess, "tries."
else:
    print "\nYou have run out of guesses. :("
   
raw_input("\nPress the enter key to exit.")
