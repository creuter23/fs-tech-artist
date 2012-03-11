#Computer Words
#A game whre the computer picks a word and the user must guess what it is.

import random

#Setting initial values
WORDS = ("book","computer","paint ball","laser tag")
word = random.choice(WORDS)
correct = word

#User instructions

print "I'm thinking of a word... It has", len(word), "characters in it."
print "You can ask me what letters are in the word and I'll tell you yes or no."
print "You only get 5 guesses before you have come up with the word. Good luck. : ) "

guess = raw_input("\nGuess a letter. ")
guess_num = 1

#Creates a while loop to run until the user runs out of guesses
while (guess_num < 5):


#Creates an if statement to evaluate if the guessed letter is in the word or not
    if guess in word:
        print "Yes,", guess, "is in my word."
        guess_num += 1
        guess = raw_input("\nTake another guess.")
        
    else:
        print "Sorry, but", guess, "is not in my word. Try again."
        guess_num += 1
        guess = raw_input("\nTake another guess.")

        
#Promps the user to guess the word
word_guess = raw_input("\nYou've run out of guesses. Try to see if you know what my word is. ")

#Creates an if statement to evaluate if the guessed word is the correct word or not
if (word_guess == correct):
    print "\nYou got it! Congrats!"

else:
    print "Sorry, but my word was", word

raw_input("\nPress the enter key to exit.")
