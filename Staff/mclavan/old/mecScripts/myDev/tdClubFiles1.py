'''
TDClub Meeting
Files Part 1
Paths

Description:
	The script shows how to get and manipulate file paths.
	
	
tdClubFiles1.py

'''

import os, os.path
import glob
import maya.cmds as cmds


'''
Finding paths
'''

'''
Maya
	internalVar command
	Common Flags
	userAppDir(uad) Return the user application directory.
	userScriptDir(usd) Returns the script folder (current version scripts folder)
	userWorkspaceDir(uwd) Return the user workspace directory (also known as the projects directory).
	
'''

path = cmds.internalVar(userAppDir=True) # Result: C:/Documents and Settings/mclavan/My Documents/maya/ # 
path = cmds.internalVar(userScriptDir=True) # Result: C:/Documents and Settings/mclavan/My Documents/maya/2009/scripts/ # 


'''
Python:
Must import os module:
	import os
	os.environ # returns a dictionary
	os.environ.keys() #returns all the keys
	os.environ['HOMEDRIVE'] # returns the defintion of the key 'HOMEDRIVE' which is C:
'''

# print out all the environ keys along with there definitions.
for key in os.environ.keys():
	print("Key: %s\nDesc: %s" %(key, os.environ[key]))
	print("-----"*10)


'''
Dealing with files and directories
'''

'''
os.path module
Your one stop for dealing with diectories, files and their extensions.

'''


# Getting to the default script directory
# os.path.join() method
scriptDir = cmds.internalVar(userAppDir=True)
scriptDir = os.path.join(scriptDir, "scripts") # Result: C:/Documents and Settings/mclavan/My Documents/maya/scripts # 


# Creating your own directory
# What if it allready exists? It throws an error
scriptDir = cmds.internalVar(userAppDir=True)
os.mkdir( os.path.join(scriptDir + "myNewDir") )

# Option 1 Exceptions (later podcast)

# Option 2 Use the os.path.exists(path) method
if( os.path.exists(os.path.join(scriptDir + "myNewDir")) ):
	print("%s exists" %(os.path.join(scriptDir + "myNewDir")))
else:
	os.mkdir( os.path.join(scriptDir + "myNewDir") )


'''
Getting the contents of a folder
'''
scriptDir = cmds.internalVar(userAppDir=True)

'''
os.listdir(path)
'''
fileList = os.listdir(scriptDir)

# determine if something is a directory or a file
for item in fileList:
	fullPath = os.path.join(scriptDir,item)
	if( os.path.isdir(fullPath) ):
		print("%s, This is a directory." %item)
	elif( os.path.isfile(fullPath) ):
		print("%s, This is a file." %item)


'''
Dealing with files and their exentsions
'''
# Splitting fileName from its extension
# Works with an entire path.
# os.path.split(path) # Returns (path, file)


# Splitting a file from its path.
# os.path.splitext(file)  # Returns (root, ext)

for item in fileList:
	fullPath = os.path.join(scriptDir,item)
	if( os.path.isdir(fullPath) ):
		print("%s, This is a directory." %item)
	elif( os.path.isfile(fullPath) ):
		pieces = os.path.splitext(item)
		print("%s, This is a file. \n\tFileName: %s \n\tExt: %s" %(item, pieces[0], pieces[1]))

'''
Returning a particular type of file from a directory.
'''

import glob
scriptDir = cmds.internalVar(userAppDir=True)
scriptDir = os.path.join(scriptDir, "scripts")
pyFiles = glob.glob( os.path.join(scriptDir,"*.py") )

for py in pyFiles:
	print("Python file: %s" %os.path.split(py)[1])
	print("Python file path: %s" %os.path.split(py)[0])


# Do a podcast on data structures for TDClub
# Lists, tupils, dictionaries, sets
# mapping?


