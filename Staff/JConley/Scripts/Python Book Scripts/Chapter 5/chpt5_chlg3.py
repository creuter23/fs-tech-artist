"""Chapter 5 Challenge 3 """

"""
Author: Jennifer Conley
Date Modified: 9/1/11

Description: The objective of this script is to create dictionary that pairs
the names of fathers and sons together. The user will be able to add,
replace, and delete names. Data will be able to be displayed as only sons,
only fathers, or a list of both names.
"""

dict = {'John' : 'Jerry', 'Jason' : 'Jerry', 'Jim' : 'Henry'}

print 'You have several different options to choose from...'
print 'Select an option by typing in the number next to your choice.'
print '1. Find the name of a father based on the name of the son.'
print '2. Add a son / father set of names.'
print '3. Replace a pair of names.'
print '4. Delete a pair of names.'
print '5. Print names.'
print '6. Exit.'

choice = int(raw_input('What would you like to do? '))
while choice != 6:
    if choice == 1:
        son= raw_input('Which name would you like to search for? ')
        if son in dict:
            father = dict[son]
            print father + ' is the father of ' + son + '.'
            choice = int(raw_input('What would you like to do? '))

    elif choice == 2:
        son = raw_input('What is the name of the son you want to add? ')
        if son not in dict:
            father = raw_input('Who is the father? ')
            dict[son] = father
            print son + ' is now listed as being the son of ' + father + '.'
            choice = int(raw_input('What would you like to do? '))
            
        else:
            print 'That name is already listed.'
            choice = int(raw_input('What would you like to do? '))

    elif choice == 3:
        son = raw_input("What is the name of the son who's father you want to replace? ")
        if son in dict:
            father = raw_input("What is the father's name? ")
            dict[son] = father
            print father + ' is now listed as the father of ' + son + '.'
            choice = int(raw_input('What would you like to do? '))
            
        else:
            print son + ' is not listed. Try adding him to the dictionary.'
            choice = int(raw_input('What would you like to do? '))

    elif choice == 4:
        son = raw_input('What is the name of the son you want to remove from the list? ')
        if son in dict:
            del dict[son]
            print son + ' has been removed from the list.'
            choice = int(raw_input('What would you like to do? '))           

    elif choice == 5:
        display = raw_input('Do you want a list of sons, fathers, or both? ')
        display = display.lower()
        if display == 'sons':
            print dict.keys()
            choice = int(raw_input('What would you like to do? '))

        elif display == 'fathers':
            print dict.values()
            choice = int(raw_input('What would you like to do? '))

        elif display == 'both':
            print dict.items()
            choice = int(raw_input('What would you like to do? '))

        else:
            print 'That is not a valid choice.'
            choice = int(raw_input('What would you like to do? '))

raw_input('Exiting the program.')


