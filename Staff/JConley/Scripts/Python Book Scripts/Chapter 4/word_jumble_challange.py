#Word Jumble
#Takes a word from a list and jumbles the letters.
#User must unscrable the word. Extra points are awarded for not using a hint.


import random

#Setting initial values
WORDS = ("python", "mel", "coding", "scripts")

#Hints
hint1 = "A scriting language named after a type of snake."
hint2 = "This is the scripting language for Maya."
hint3 = "Programers stay up all night..."
hint4 = "An awesome rigger never leaves home without their..."

HINTS = (hint1, hint2, hint3, hint4)

num = random.randrange(3)
word = WORDS[num]
hint = HINTS[num]
correct = word

points = 10

jumble = ""


#Creating a while loop to generate the jumbled word
while word:
    position = random.randrange(len(word))
    jumble += word[position]
    word = word[:position] + word[(position + 1):]

    
#User instructions
print \
"""
Try to unscrable the word.
You can score extra points for not using hints.
"""

print "The jumbled word is:", jumble

guess = raw_input("\nTake a guess?")
guess = guess.lower()
num_guess = 1


#Creates a while loop for if the word is incorrect
while (guess != correct) and (guess != ""):
    print "\nThat's not correct. :("
    guess  = raw_input("\nTry again? ")
    guess = guess.lower()
    num_guess += 1


#If the user does not guess correctly in 3 tries they are offered a hint
    if num_guess >= 3:
        help = raw_input("\nWould you like a hint? ")
        if help == "yes" or "Yes":
            print hint
            guess = raw_input("\nTake another guess. ")
            points = points - 5
            
        else:
            guess = raw_input("\nTake another guess. ")


#If the user guesses correctly they win
if guess == correct:
    print "\nYou guessed it! Awesome job!"
    print "\nYou scored", points, "this game."

raw_input("\n\nPress the enter key to exit.")
