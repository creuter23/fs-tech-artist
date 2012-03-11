"""Chapter 5 Challenge 1 """

"""
Author: Jennifer Conley
Date Modified: 9/1/11

Description: The objective of this script is to print a list of words and
have them be printed in a random order without words being repeated.

"""

import random

word_list = ['dog', 'cat', 'snake', 'mouse', 'bird', 'hamster', 'lizard']
list_length = len(word_list)

for each in range(0,list_length):
	num = random.randrange(0,list_length)
	
	word = word_list[num]
	print word
	
	word_list.remove(word)
	list_length = len(word_list)
