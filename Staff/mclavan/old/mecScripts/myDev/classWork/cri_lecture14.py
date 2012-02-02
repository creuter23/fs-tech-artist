'''
Lecture 14
Paths, Files, and Classes
cri_lecture14.py

Description:

How To Run:


'''

import maya.cmds as cmds

# To do:
# Find nodes on paths, files, and pickle
#   - attribute script on tdclub area (sba)
# Get attribute builder from tdClub notes.
# Test to make sure if maya 2011 is active on your laptop.

'''
Dictionaries
- Made up of key terms.
- Only unique keys can be used.
- Unordered
'''

'''
internalVar
(other paths TDClub podcast)

Common Flags:
userAppDir(uad) - Maya folder path
userScriptDir(usd) - Maya's version script folder (2009\scripts)
'''
cmds.internalVar( userAppDir=True )



'''
Paths
internalVar, os.path, and fileDialog
'''

'''
os.path (apart of the os module)
'''
import os.path

'''
# Splitting paths
# __file__ curent script location
'''

filePieces = os.path.split( __file__ )
# (filePath, file)
print(filePieces)

'''
# os.path.join
# Puts the proper slashes based upon your os.
'''

# Creating your own icon folder.
# __file__ current file path
filePieces = os.path.split(__file__)
fileName = "icon.xpm"
filePath = os.path.join( filePieces[0], "icons", fileName )

cmds.window()
cmds.columnLayout()
cmds.symbolButton( i=filePath )
cmds.symbolButton( i=os.path.join( filePieces[0], "icons", "newIcon.xpm") )
cmds.showWindow()


'''
# File Dialog
# flags
mode(m) 0 == read, 1 == write
directoryMask(dm) - What directory and which files to show.

Returns the path selected.
'''

filePath = cmds.fileDialog( mode=0, directoryMask="C:\filePath\*.txt" ) # will only show text files from C:\filePath

mayaFolder = cmds.internalVar( userAppDir=True )
filePath = cmds.fileDialog( mode=0, directoryMask= mayaFolder )


'''
Files
PodCast
'''

'''
Files Part 1 - Opening and Closing a file
'''

# Modes: "r", "w", "a"
# Path: "C:\filePath"

# myFile = open("C:\FilePath", "mode")

filePath = "C:\filePath"
filePath = "/Users/mclavan/Desktop"

myFile = open(filePath, "w")
# Reading and Writing goes between
myFile.close()



'''
How to get different paths will be covered after part 3
'''

'''
Files Part 2 - Writing to a file
# Just like printing
'''

filePath = "C:\filePath"
myFile = open(filePath, "w")
# Writing
myFile.write( "info to write" ) # Won't automaticly go to next line
myFile.close()

'''
Escape Sequences
\n -> newline
\t -> tab
'''


filePath = "C:\filePath"
myFile = open(filePath, "w")
# Writing
myFile.write( "object.tx\n" ) # \n newline
myFile.write( "object.ty\n" ) # Writing an attribute one line at a time.
myFile.close()

'''
Test gui()
'''
def gui():
	cmds.window(w=150, h=200)
	cmds.columnLayout()
	cmds.textScrollList("sbaTSL", w=145, h=195,
		append=cmds.ls(sl=True))
	cmds.showWindow()

'''
Files Part 3 - Reading from a file
'''

filePath = "C:\filePath"
myFile = open(filePath, "r")
# Reading all lines into a list
fileInfo = myFile.readlines()  # Each line will still have its newline "\n" at the end.

myFile.close()


'''
string Methods
rstrip & lstrip

(Podcast for more)
'''

cmds.window(w=150, h=200)
cmds.columnLayout()
cmds.textScrollList("sbaTSL", w=145, h=195)
cmds.showWindow()

for info in fileInfo:
	print("Entering " + info + " into the textScrollList")
	# rstrip will remove blank spaces and new lines character at the end of a string.
	cmds.textScrollList( "sbaTSL", edit=True, append=info.rstrip() )   

	
	
# String Methods
# split & replace
# "lt_arm_01_geo"

myObject = "lt_arm_01_geo"
pieces = myObject.split( "_" )


'''
Pickle
Preserve Data

http://docs.python.org/library/pickle.html
'''

# Basic Startup
import pickle
filePath = ""
fileName = "testPickle.txt"
fullPath = os.path.join( filePath, fileName )

fileInfo = open( fullPath, "w" )
fileInfo.close()


# Write
names = ["michael", "bob", "george", "susan"]
selected = cmds.ls(sl=True)
fileInfo = open( fullPath, "w" )
pickle.dump( names, fileInfo )
pickle.dump( selected, fileInfo )
fileInfo.close()

# Read
fileInfo = open( fullPath, "r" )
pickle.load( fileInfo )
pickle.load( fileInfo )
fileInfo.close()


'''
Part 2 - Pymel
- Preinstalled 2011
- Custom Install 2010 and before.

Pros:
- True OOP design.
	- commands return instances instead of strings
- Much faster coding
	- Easy Access to hierarchy nodes and common functionality.
	- Connecting Attributes
- Callback	
Cons:
- Must have pymel installed
- Slower than Maya's normal python.

'''

'''
Help docs


Beginning Tutorial

'''
import pymel.core as pm


# Getting selected objects

selected = pm.ls(sl=True)


# Dealing with instances


# Dealing with attributes
# get and set


# Creating nodes

# Connecting attributes


import pymel.core as pm

pm.window()
# Result: ui.Window('window1') #
pm.paneLayout()
# Result: ui.PaneLayout('window1|paneLayout10') #
pm.textScrollList( numberOfRows=8, allowMultiSelection=True,
                    append=['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
                                    'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen'],
                    selectItem='six', showIndexedItem=4 )
pm.showWindow()



'''
Part 3 - Object Oriented Programming (OOP)

Pros:
- Build your own data types.
- Keep access to much more information.

Cons:
- Code that is harder to read.
- More complicated to write.

'''


