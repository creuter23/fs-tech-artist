'''
Lecture 11 - Strings, Lists, & standard library

'''


'''
Parts 1 Strings & List methods
'''
# http://docs.python.org/
# http://docs.python.org/library/string.html

'''
String Concatination
'''
# http://rgruet.free.fr/PQR26/PQR2.6.html
# old
selected = cmds.ls(sl=True)[0]
cmds.setAttr( selected + ".ty", 3 )

# new
selected = cmds.ls(sl=True)[0]
cmds.setAttr( "%s.ty" %selected, 3 )

# frame padding
# "obj.001.iff"
value = 1
fileName = "obj.%03d.iff" %value
print(fileName)

obj = "img1"
fileType = "iff"
value = 1
fileName = "%s.%03d.iff" %(obj, value, fileType)
print(fileName)



'''
String methods
'''
# python help docs

# split()
# replace()
# find()
# join

# Base examples

'''
# Split - Breaking up strings into list
'''
line = "Character Rigging Lecture 11 String and List Methods"
lineParts = line.split()
# ["Character", "Rigging", "Lecture", "11", "String", "and", "List", "Methods"]

obj = "object.attr"
pieces = obj.split(".")
# ['object', 'attr']

'''
# Replace
'''
icon = "lt_arm_icon"
rIcon = icon.replace( "lt", "rt" )

line = " ".join(line)
# "Character Rigging Lecture 11 String and List Methods"
line2 = ",".join(line)
# "Character,Rigging,Lecture,11,String,and,List,Methods"

attr = ".".join(pieces)
# "object.attr"

'''
Lists
'''
# http://docs.python.org/tutorial/datastructures.html

# index
names = ["Bob", "George", "Susan", "Sam", "Michael"]
names[0]
names[2]
names[-1]

# slices
names[0:2]  # index 0 and 1
names[1:] # index 1 to end
names[0:-1] # index 0 till second from the end.

# len (length command)
nameLength = len(names)

'''
List methods
'''
# append
# Adding to the end of list

# extend
# Add the contents of a list into the current list

# pop
# list.pop([i])
names.pop() # pops "Michael" from the end of the list
name = names.pop(0) # pops the first item from list and returns it to name.

# insert
# list.insert( index, x )
names.insert(0, "Michael")

# remove 
# list.remove( x )
names.remove("George")

'''
Selecting the faces from one object, and appling it to another.
'''
#-- Steps
# Assuming the user has faces selected.
# 1) Get Selection
# 
# 2) Remove object name
#  - replace with different objects


# Interface
import maya.cmds as cmds

def selFaces():	
	cmds.window(w=100, h=60)
	cmds.columnLayout( rs=2, co=["both",10] )
	cmds.button( label="Get Faces", w=100,
		command=storeSel)
	cmds.button( label="Select Faces", w=100,
		command=selectFaces)
	cmds.showWindow()

def storeSel(*args):
	'''
	Stores Selected faces in the script as a global variable
	'''

	print( "Faces Stored" )
	
	
def selectFaces(*args):
	'''
	Uses stored faces, removes object and replaces it with selected one.
	'''

	print( "Faces Selected" )
	
	
#-- Steps
# Get Selection
# Store it
# Assuming the user has faces selected.
selected = cmds.ls(sl=True)
# Result: [u'HighBody.f[740:1644]', u'HighBody.f[2156:2248]', u'HighBody.f[2989:3893]', u'HighBody.f[4405:4497]'] # 

# Assuming the user selects the a transform
selected = cmds.ls(sl=True)[0]
# Remove object name
#  - replace with different objects
# split method
# 'HighBody.f[740:1644]'
# 'HighBody' & '.f[740:1644]'

faces = []
# Empty List
for sel in selected:
	pieces = sel.split(".")  # ['HighBody', 'f[740:1644]']
	faces.append( selected + "." + pieces[-1] )
	

def storeSel(*args):
	'''
	Stores Selected faces in the script as a global variable
	'''
	selected = cmds.ls(sl=True)
	global faces
	faces = selected

	pieces = selected[0].split(".")	
	print( "Faces on Object: %s stored" %pieces[0] )
	
	
def selectFaces(*args):
	'''
	Uses stored faces, removes object and replaces it with selected one.
	'''
	selected = cmds.ls(sl=True)[0]
	
	
	print( "Object: % Faces Selected" %selected )
	


'''
Renaming
In Maya
'''
def fullRename( pre, name, counter, suffix ):
	'''
	Naming convention "ori_name_##_type" or "lt_arm_1_bj"
	'''
	# Get selected items from the scene
	
	# Loop through selected
	
		# Place together name pieces (arguments)
		
		# Push the coutner forward.
	
	print("Rename Complete")

def removePart( index=0 ):
	'''
	This function will remove a piece of the naming convention
	'''
	# Get selected objects
	
	# Is it going to work on multiple objects???
	
	# Break selected strings into multiple pieces
	
	# Remove index no longer needed
	
	print("Piece removed")
	
def replacePart( oldText, newText ):
	'''
	The selected text will have the requested piece removed and replaced by 
	the supplied text.
	'''
	# Get
	
	print("Old text removed by new text.")


'''
List Examples
'''

'''
textScrollList
visual list
'''
def tslGUI():
	cmds.window( title="TextScrollList Example", w=150, h=225)
	cmds.columnLayout(rs=5, columnOffset=["both",10])
	cmds.textScrollList('criTSL', w=150, h=200)
	cmds.rowColumnLayout( nc=2, columnWidth=[[1,75],[2,75]],
		columnOffset=[1,"right",5])
	cmds.button( label="Add" )
	cmds.button( label="Remove" )
	
	cmds.showWindow()

def add(*args):
	'''
	Add Selected Item sto the textScrollList
	'''
	
	
	
def remove(*args):
	'''
	Remove selected items from the textScrollList
	'''

'''
Dictionaries
- key and values
- unordered
- only unique keys
http://docs.python.org/library/stdtypes.html#mapping-types-dict
'''
dictionary = {}  # empty dictionary
dictionary = {"objectA" : value, "objectB" : value}  # length is 2
dictionary["objectA"]

# dictionary methods
# dict.keys()

# dict.has_key()

# dict.items()
for i, item in dictionary.items()
	print("Key: %s Value: %s" %(i, item))

'''
Attribute Example
'''


'''
More Loops
'''

# enumerate


# Showing all the files in a directory.

'''
Help and Web Pages
'''
# string
# maya help & showHelp commands 
cmds.help( 'textScrollList', language='python', doc=True )
cmds.showHelp( 'http://www.autodesk.com/', absolute=True )
 
# google search
# http://www.google.com/search?sourceid=chrome&ie=UTF-8&q=

def googleSearch( item ):
	google = r'http://www.google.com/search?sourceid=chrome&ie=UTF-8&q='
	cmds.showHelp( google + item, absolute=True )

googleSearch( "python" )


'''
Standard Library
'''
import os
import sys
import random
import glob
# import os, sys, random, glob

# http://docs.python.org/library/index.html

'''
# os module
http://docs.python.org/library/os.html
'''

# listing directories
os.listdir( path )
os.listdir( r'C:\Users\mclavan\Desktop' )

# is it a file or a directory
import os.path
# os.path.isfile( path )
# os.path.isdir( path )

desktop = r'C:\Users\mclavan\Desktop'
os.listdir( desktop )

'''
Renaming
In System
'''

# rename
# os.rename(old, new)
# Must be the entire path for both.

import os
oldName = r'C:\Documents and Settings\mclavan\Desktop\aquanauts_details_character_doctorBloopdool_01.jpg'
newName = r'C:\Documents and Settings\mclavan\Desktop\test.jpg'
os.rename( oldName , newName )

# environ
# os.environ

'''
# glob
import glob
glob.glob()
'''

desktop = r'C:\Users\mclavan\Desktop'
files = glob.glob( desktop

'''
Comparing files
filecmp
'''
import filecmp
file1 = r'C:\Users\mclavan\Desktop\Adivination-icon.png'
file2 = r'C:\Users\mclavan\Desktop\b.png'
filecmp.cmp( file1, file2 )


# Get two directories compare files


# sys
# running commands from the command line.
# sys.path



# random






