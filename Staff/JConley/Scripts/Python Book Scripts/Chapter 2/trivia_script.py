#Trivia Script
#Minor exersice in using different types of data from user input

name = raw_input("Name? ")
age = int(raw_input("Age? "))
weight = int(raw_input("Weight?"))

print "\nHi, " + name

dog_years = age * 7
print "\nYou are ", dog_years , "in dog years."

seconds = age * 365 * 24 * 60 * 60
print "You are over ", seconds , "seconds old."

moon_weight = weight / 6.0
print "\nYour weight on the moon would be ", moon_weight , "pounds."

sun_weight = weight * 27.1
print "\nYour weight on the sun would be ", sun_weight , "pounds."

raw_input("\n\nPress the enter key to exit.")








