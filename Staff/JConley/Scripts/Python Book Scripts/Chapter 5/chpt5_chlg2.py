"""Chapter 5 Challenge 2 """

"""
Author: Jennifer Conley
Date Modified: 9/1/11

Description: The objective of this script is to create a Character Creator
program. The user will be given 30 points to spend on attributes for their
character; Strength, Health, Wisdom, and Dexterity.

The user will be able to spend the points any way they wish as well as
redistribute the points to other attributes if they wish.

"""

points = 30

stamina = 0
strength = 0
spirit = 0
agility = 0

stats = (['stamina', stamina], ['strength', strength],
['spirit', spirit], ['agility', agility])

print 'You have ' + str(points) + ' points to spend on stats for your character.'
print 'Your stats are currently:'
print '1. ' + stats[0][0] + '\t ' + str(stats[0][1])
print '2. ' + stats[1][0] + '\t ' + str(stats[1][1])
print '3. ' + stats[2][0] + '\t ' + str(stats[2][1])
print '4. ' + stats[3][0] + '\t ' + str(stats[3][1])

change = raw_input('Do you want to change your stats? ')
change = change.lower()

while change == 'yes':
    plusMinus = raw_input('Do you want to add or subtract poitns? ')
    plusMinus =  plusMinus.lower()
    
    stat = int(raw_input('Which stat would you like to chagne? 1, 2, 3, or 4? '))
    stat = stat - 1

    change_points = int(raw_input('How many points would you like to ' + plusMinus + '? '))
    
    if plusMinus == 'add':
        if (change_points <= points) and (points > 0):
            stats[stat][1] += change_points
            points -= change_points

            print 'Your starts are now:'
            print '1. ' + stats[0][0] + '\t ' + str(stats[0][1])
            print '2. ' + stats[1][0] + '\t ' + str(stats[1][1])
            print '3. ' + stats[2][0] + '\t ' + str(stats[2][1])
            print '4. ' + stats[3][0] + '\t ' + str(stats[3][1])

            print 'You have ' + str(points) + ' points left.'

            change = raw_input('Do you want to change your stats? ')

        elif (change_points > points) or (points == 0):
            print 'You do not have enough points to do that.'
            change = raw_input('Do you want to change your stats? ')

    elif plusMinus == 'subtract':
        if (change_points <= stats[stat][1]):        
            stats[stat][1] -= change_points
            points += change_points

            print 'Your starts are now:'
            print '1. ' + stats[0][0] + '\t ' + str(stats[0][1])
            print '2. ' + stats[1][0] + '\t ' + str(stats[1][1])
            print '3. ' + stats[2][0] + '\t ' + str(stats[2][1])
            print '4. ' + stats[3][0] + '\t ' + str(stats[3][1])

            print 'You have ' + str(points) + ' points left.'

            change = raw_input('Do you want to change your stats? ')

        elif (change_points > points) or (points == 0):
            print 'You do not have enough points to do that.'
            change = raw_input('Do you want to change your stats? ') 

    else:
        print 'You did not specify a legal action.'
        change = raw_input('Do you want to change your stats? ')
        


        

