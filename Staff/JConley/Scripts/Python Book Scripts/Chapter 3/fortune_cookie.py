#Forune Cookie Script
#A script to demonstrate if-elif-else loops

import random

#setting initial values
fortune = random.randrange(5) + 1
message = raw_input("\nWould you like a fortune? Yes or no? ")


#creating loop
if message == "yes" or "Yes":

    if fortune == 1:
        print "\nYou are talented in many ways."

    elif fortune == 2:
        print "\nA scholars ink lasts longer than a martyrs blood."

    elif fortune == 3:
        print "\nGrand adventures await those who are willing to turn the corner."

    elif fortune == 4:
        print "\nA journey of a thousand miles begins with a single step."

    elif fortune == 5:
        print "\nIf you want the rainbow, you must to put up with the rain."

    else:
        print "\nI can't give you a fortune at this time. :("
else:
    print "\nOk. : ("

raw_input("\nPress the enter key to exit.")




