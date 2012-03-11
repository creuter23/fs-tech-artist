#Coin Flip
#Flips a coin 100 times while keeping trake of he number of heads and tails

import random

#Setting initial values
flip = 0
heads = 0
tails = 0

#Creating loop
while flip < 100:
    flip += 1

    coin = random.randrange(2)

    if coin == 0:
        heads += 1
    else:
        tails += 1

print "The coin was flipped", flip , "times.\n"
print heads, "of those times it landed on heads.\n"
print tails, "imes the coin landed on tails.\n"
raw_input("\nPress the enter key to exit.")

