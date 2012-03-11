#Backwards
#Gets input from the user and prints it out backwards


#Gets user input
message = raw_input("What is your message? ")


#Tells user how many characters are in the message
print "Your message is", len(message), "characters long."

#Prints the user's message backwards
print "\nYour message spelled backwards is: \n"
print message[::-1]

raw_input("\nPress the enter key to exit.")
