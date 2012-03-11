# Heads or Tails to 100 counter
# Counts up to 100 and then displays Heads, or Tails
'''
count = 0
while True:
    count += 1
# end loop if count greater than 100
# not working: says 'break' outside loop
if count > 100:
    break

print(count)
'''
# randomize heads or tails
import random

coin_side = random.randint(1,2)

if coin_side == 1:
    # Heads
    print("Heads")

if coin_side == 2:
    # Tails
    print("Tails")

input("\n\nPress the enter key to exit.")
