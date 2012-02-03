'''
Final Project SBA 0907
Michael Clavan
7/14/09
mclavan_fp.py

Desc:
	The main purpose of this script is to create a keyframing script to
	make it easier to keyframe specific areas of a character rig.
	
How To Use:

import mclavan_fp
mclavan_fp_extra.gui()

'''

'''
Posible Extras
- Mac to PC gui switch
'''

import maya.cmds as cmds

print( "SBA Final Project: Keyframing Script" )

win = "sbaKeyFPWin"
winWidth = 200
winHeight = 300
scriptName = __name__
def gui():
	'''
	Main GUI procedure for the keyframing script.
	'''
	
	# Check to see if the window already exists
	if( cmds.window(win, q=True, ex=True) ):
		cmds.deleteUI(win)
		
	# main window
	cmds.window(win, title="Keyframing Script", mb=True, w=winWidth, h=winHeight)
	
	cmds.menu(label="File")
	cmds.menuItem(label="Open List",
		c=scriptName + ".readAttr()")
	cmds.menuItem( divider=True)
	cmds.menuItem(label="Save All",
		c=scriptName + ".writeAttrFile()")
	cmds.menuItem(label="Save Sel",
		c=scriptName + ".writeSelAttrFile()")
	
	cmds.menu(label="Shelf Button")
	cmds.menuItem(label="All Attrs",
		c=scriptName + ".allToShelf()")
	cmds.menuItem(label="Sel Attrs",
		c=scriptName + ".selToShelf()")
	cmds.menuItem(label="From File",
		c=scriptName + ".shelfFromFile()")
	
	cmds.menu(label="Scripts")
	cmds.menuItem(label="sbaRename",
		c="import sbaRename; sbaRename.gui()")
	cmds.menuItem(label="sbaRename help",
		c="help(sbaRename)")
	cmds.menuItem( divider=True)
	cmds.menuItem(label="sbaAttr",
		c="import sbaAttr; sbaAttr.gui()")
	cmds.menuItem(label="sbaAttr help",
		c="help(sbaAttr)")
	
	cmds.menu(label="Info")
	cmds.menuItem(label="Help",
		c="help("+scriptName+")")
	cmds.menuItem(label="About")
	# Main Layout
	mainCol = cmds.columnLayout("sbaKeyMC")

	mainRow = cmds.rowColumnLayout(nc=3, cw=[[1,200],[2,30],[3,200]],
		columnOffset=[2,"both",5])
	mainGUI(mainRow)
	cmds.button(label=">>")
	cmds.channelBox('sbaKeyCB')
	
	cmds.showWindow(win)

def writeAttrFile():
	'''
	Writes the attributes from the textScrollList to a file.
	'''
	# Let the user choose where the files is being saved to.
	# Starting point will be the maya folder.
	mayaFolder = cmds.internalVar( userAppDir=True )
	# File Dialog
	# sba will be the file extension.
	filePath = cmds.fileDialog( mode=1, directoryMask= mayaFolder+"*.sba")
	
	print( "Choosen file: " + filePath )
	
	# Gather the attributes from the textScrollList
	allItemsTSL = cmds.textScrollList( "sbaKeyTSL", q=True, allItems=True)
	
	# Open File
	attrFile = open( filePath, "w" )  # Will overwrite the file if it allready exists!
	
	# Loop through one element at a time writing it to a file.
	for item in allItemsTSL:
		attrFile.write( item + "\n" )
	
	attrFile.close()
	# Close File
	
	
	
def writeSelAttrFile():
	'''
	Writes the selected attributes from the textScrollList to a file.
	'''
	# Let the user choose where the files is being saved to.
	# Starting point will be the maya folder.
	mayaFolder = cmds.internalVar( userAppDir=True )
	# File Dialog
	# sba will be the file extension.
	filePath = cmds.fileDialog( mode=1, directoryMask= mayaFolder+"*.sba")
	
	print( "Choosen file: " + filePath )
	
	# Gather the attributes from the textScrollList
	selectedTSL = cmds.textScrollList( "sbaKeyTSL", q=True, si=True)
	
	# Open File
	attrFile = open( filePath, "w" )  # Will overwrite the file if it allready exists!
	
	# Loop through one element at a time writing it to a file.
	for item in selectedTSL:
		attrFile.write( item + "\n" )
	
	# Close File		
	attrFile.close()

	
def readAttr():
	'''
	Read attributes from a chosen file.
	'''
	
	# Get information from file
	# Starting at the maya folder and limiting to extension .sba
	mayaFolder = cmds.internalVar( userAppDir=True )
	# File Dialog
	# sba will be the file extension.
	filePath = cmds.fileDialog( mode=0, directoryMask= mayaFolder+"*.sba")
		
	print( "Choosen file: " + filePath )
	
	# Open File
	attrFile = open( filePath, "r" )  # Will overwrite the file if it allready exists!

	attrs = attrFile.readlines()
	
	# Close File		
	attrFile.close()

	# loop through file content adding to the textScrollList
	for attr in attrs:
		# Check to see if the attribute allready exists in the textScrollList
		attr = attr.rstrip()
		# all the current tsl items
		allItemsTSL = cmds.textScrollList("sbaKeyTSL", q=True, allItems=True)
		if( allItemsTSL and ( attr in allItemsTSL) ):
			print( attr + " all ready exists in the list.")
		else:
			cmds.textScrollList("sbaKeyTSL", edit=True, append=attr)			
			
import maya.mel as mel	
def allToShelf():
	'''
	Saves all the textScrollList attributes to the shelf to be keyframed.
	'''	
	results = cmds.promptDialog( title="Creating a shelf button.", message="Enter Shelf Button Name:", button=['OK','Cancel'],
			defaultButton='OK', cancelButton='Cancel', dismissString='Cancel' )
	
	fileName = cmds.promptDialog(query=True, text=True)
		
	# if( results ):

	# Get the current shelf
	currentShelf= mel.eval( 'global string $gShelfTopLevel;\rstring $shelves = `tabLayout -q -selectTab $gShelfTopLevel`;' )
	
	# Compile the info from the textScrollList
	# Get all the attrs from the textScrollList
	allItemsTSL = cmds.textScrollList( "sbaKeyTSL", q=True, allItems=True )
	
	# Calling my function to complies the attribute to be keyframed correctly.
	keyFrameLines = compileKeyframes(allItemsTSL)
	
	# Create the shelfButton
	cmds.shelfButton( l=fileName, iol=fileName, c=keyFrameLines, image='setKey.xpm',  parent= currentShelf  )
	
def compileKeyframes(attrs):
	'''
	Creates the keyframe line for the shelf button.
	'''
	keyFrameLines = "import maya.cmds as cmds\n"
	for attr in attrs:
		keyFrameLines += "cmds.setKeyframe( '" + attr + "' )\r"
	
	print( keyFrameLines )
	
	return keyFrameLines
	
	
def selToShelf():
	'''
	Saves all the selected textScrollList attributes to the shelf to be keyframed.
	'''
	results = cmds.promptDialog( title="Creating a shelf button.", message="Enter Shelf Button Name:", button=['OK','Cancel'],
			defaultButton='OK', cancelButton='Cancel', dismissString='Cancel' )
	
	fileName = cmds.promptDialog(query=True, text=True)
		
	# if( results ):

	# Get the current shelf
	currentShelf= mel.eval( 'global string $gShelfTopLevel;\rstring $shelves = `tabLayout -q -selectTab $gShelfTopLevel`;' )
	
	# Compile the info from the textScrollList
	# Get all the attrs from the textScrollList
	selectedTSL = cmds.textScrollList( "sbaKeyTSL", q=True, si=True )
	
	# Calling my function to complies the attribute to be keyframed correctly.
	keyFrameLines = compileKeyframes(selectedTSL)
	
	# Create the shelfButton
	cmds.shelfButton( l=fileName, iol=fileName, c=keyFrameLines, image='setKey.xpm',  parent= currentShelf  )
	
def shelfFromFile():
	'''
	Creates a shelf button to keyframe the attributes straight from a previously saved file.
	'''
	# Get information from file
	# Starting at the maya folder and limiting to extension .sba
	mayaFolder = cmds.internalVar( userAppDir=True )
	# File Dialog
	# sba will be the file extension.
	filePath = cmds.fileDialog( mode=0, directoryMask= mayaFolder+"*.sba")
		
	print( "Choosen file: " + filePath )
	
	# Open File
	attrFile = open( filePath, "r" )  # Will overwrite the file if it allready exists!

	attrs = attrFile.readlines()
	
	# Close File		
	attrFile.close()

	attrToShelf = []
	# loop through file content adding to the attrToShelf variable.
	for attr in attrs:
		attrToShelf.append( attr.rstrip() )
	
	print( attrToShelf )
	
	results = cmds.promptDialog( title="Creating a shelf button.", message="Enter Shelf Button Name:", button=['OK','Cancel'],
			defaultButton='OK', cancelButton='Cancel', dismissString='Cancel' )
	
	fileName = cmds.promptDialog(query=True, text=True)
		
	# if( results ):

	# Get the current shelf
	currentShelf= mel.eval( 'global string $gShelfTopLevel;\rstring $shelves = `tabLayout -q -selectTab $gShelfTopLevel`;' )
	
	
	# Calling my function to complies the attribute to be keyframed correctly.
	keyFrameLines = compileKeyframes(attrToShelf)
	
	print(keyFrameLines)
	# Create the shelfButton
	cmds.shelfButton( l=fileName, iol=fileName, c=keyFrameLines, image='setKey.xpm',  parent= currentShelf  )
		
	
	
def mainGUI(parent):
	'''
	This function represents the guts of the gui for this script.
		- Adding and Removing elements from the TSL.
		- Keyframing elements from the TSL
	'''
	# Guts of the gui
	cmds.columnLayout()
	cmds.textScrollList("sbaKeyTSL", w=winWidth, h=200, ams=True)
	
	# Rem and Add buttons
	cmds.rowColumnLayout( nc=2, cw=[[1,winWidth/2],[2,(winWidth-5)/2]])
	cmds.button(label="Remove All", w=winWidth/2,
		c=scriptName + ".tslRemAll()")
	cmds.button(label="Remove Sel", w=winWidth/2,
		c=scriptName + ".tslRemSel()")	
	cmds.button(label="Add Attr", w=winWidth/2,
		c=scriptName + ".addAttrTSL()")	
	cmds.button(label="Add Obj", w=winWidth/2,
		c=scriptName + ".addObjTSL()")
	cmds.setParent("..")
		
	cmds.button(label="Keyframe All", w=winWidth,
		c=scriptName + ".keyFrameAll()")
	cmds.button(label="Keyframe Sel", w=winWidth,
		c=scriptName + ".keyframeSel()")	
		
	cmds.setParent(parent)
	
	
def tslRemAll():
	'''
	Renmove all elements from the textScrollList.
	'''
	cmds.textScrollList( "sbaKeyTSL", edit=True, ra=True )
	
	
def tslRemSel():
	'''
	Remove the selected elements from the textScrollList
	'''
	selectedTSL = cmds.textScrollList( "sbaKeyTSL", q=True, si=True)
	
	for selTSL in selectedTSL:
		print("Removing " + selTSL + " from the textScrollList.")
		cmds.textScrollList( "sbaKeyTSL", edit=True, ri=selTSL )
		
	
def addAttrTSL():
	'''
	Add the selected attributes from the channelBox to the textScrollList
	'''
	# Grab selected objects
	selected = cmds.ls(sl=True)
	# Grab selected channelBox objects
	selectedCB = cmds.channelBox('sbaKeyCB', q=True, selectedMainAttributes=True)
	
	# Loop through selected.
	for sel in selected: 
		# Loop through selected channelBox
		for selCB in selectedCB:
			# Put attribute together "object.attribute"
			attr = sel + "." + selCB
			
			# Get all the items inside the textScrollList.
			tslItems = cmds.textScrollList( "sbaKeyTSL", q=True, allItems=True)
			'''
			if( attr in tslItems):
				# Add to your textScrollList
				print( attr + " allready exists inside the textScrollList." )
			else:
				cmds.textScrollList( "sbaKeyTSL", edit=True, append=attr )
			'''
			
			if( tslItems and (attr in tslItems) ):
				# Add to your textScrollList
				print( attr + " allready exists inside the textScrollList." )
			else:
				cmds.textScrollList( "sbaKeyTSL", edit=True, append=attr )
	
	
def addObjTSL():
	'''
	Add the selected object to the textScrollList
	'''
	# Grab selected
	selected = cmds.ls(sl=True)
	# Add them to the textScrollList
	cmds.textScrollList( "sbaKeyTSL", edit=True, append=selected )
	
def keyFrameAll():
	'''
	Keyframe all the attribute contained in the textScrollList
	'''	
	# Get all the elments from the textScrollList
	allTSL = cmds.textScrollList( "sbaKeyTSL", q=True, allItems=True )
	# Keyframe textScrollList's attributes
	cmds.setKeyframe(allTSL)
	
def keyframeSel():
	'''
	Keyframe all the selected attributes from the textScrollList
	'''
	# Get the selected textScrollList Items
	selectedTSL = cmds.textScrollList( "sbaKeyTSL", q=True, si=True)
	
	# Keyframe the attribute gathered
	cmds.setKeyframe(selectedTSL)
	
