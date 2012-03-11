""" Chapter 7 Challenge 1 """

"""
Author: Jennifer Conley
Date modified: 9/4/11

Description: Add the ability for a players score to be added to a high scores 
list along with their name. Store the data as a pickle object. 
"""

def open_file(file_name, mode):
    #Opens the file with the triva information
    try:
        the_file = open(file_name, mode)
    except(IOError),e:
        print 'Unable to open specified file' , filename, '.Ending program.', e
        raw_input ('\nPress the enter key to exit.')
        sys.exit()
    else:
        return the_file

def next_line(the_file):
    #Returns the next line from the trivia .txt file
    line = the_file.readline()
    return line

def next_block(the_file):
    #Gets the next question and answer block for the game.
    question = next_line(the_file)
    answers = []

    for each in range(4):
        answers.append(next_line(the_file))

    correct = next_line(the_file)
    if correct:
        correct = correct[0]

    points = next_line(the_file)
    explanation = next_line(the_file)

    return question, answers, correct, points, explanation

def main():
    #Creates the game structure

    import cPickle, shelve
    
    print 'Welcome to the triva game!'
    name = raw_input('\nWhat is your name? ')
    print 'Good luck', name, '!'
    trivia_file = open_file('chlg7.txt', 'r')
    score = 0

    question, answers, correct, points, explanation = next_block(trivia_file)

    while question != '':
        print question
        for each in range(4):
            print '\t', each+1, '-', answers[each]
        answer = raw_input('What is your guess? ')

        if answer == correct:
            score += int(points)
            print '\nThat is correct!'
        else:
            print '\nSorry, but that is incorrect.'
        print explanation
        print 'You have', score, 'points.\n'
    
        question, answers, correct, points, explanation = next_block(trivia_file)
    trivia_file.close()
    print 'That is the end of the game.'
    print 'Great job', name, '. You scored', score, 'points this round.'
    
    if score > 15:
        name_score = [name, score]
        
        score_file2 = open('score_file2.txt', 'w')
        cPickle.dump(name_score, score_file2)
        score_file2.close()
   
main()
raw_input('\nPress the enter key to exit.')
