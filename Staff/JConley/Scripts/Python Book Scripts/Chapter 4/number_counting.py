#Number Counting
#A script that takes in a number range from the user, and incriment by which to count


#Setting initial values
start_num = int(raw_input("What is your starting number? "))
end_num = int(raw_input("\nWhat is your ending number? "))
inc_num = int(raw_input("\nBy what incriments would you like this range counted in? "))


#Creating for in loop
for num in range(start_num, end_num, inc_num):
    print num

raw_input("\nPress the enter key to exit.")
