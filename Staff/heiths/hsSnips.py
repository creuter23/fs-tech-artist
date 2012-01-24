#!/usr/bin/python

# Things I find useful/interesting...
# Some I'll breakdown... others I'll just post.
# Heith Seewald 2012



#------------- 
#I admit it's not the most pythonic way... but it's one line and does the trick.
fileName = env.sceneName().split('/')[-1].split('.')[0]
'''
Breakdown:  
     env.sceneName     gives the full path to your scene...
    .split('/')        turns the full path name into a list of folders
    [-1]               grabs the last item in the list... which is scene file with the extention
    .split('.')[0]     Another split to grab the file name without the extention...
'''

