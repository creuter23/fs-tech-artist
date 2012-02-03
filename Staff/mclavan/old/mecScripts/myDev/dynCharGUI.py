'''
Dynamic character gui
dynCharGUI

import dynCharGUI
reload(dynCharGUI)
dynCharGUI.gui()

'''


'''
This scripts takes into account 3 types.
- pictures
- symbolButtons
- symbolCheckboxes

"char_row_col_type.xpm"
ex:
"advGirl_01_01_pic.xpm"
"advGirl_02_01_ctrl.xpm"

"advGirl_02_02_cb.xpm"
"advGirl_02_02_cb_off.xpm"

'''

# Icon manager
# xml generator
# annotation tracker
# renamer
# control connection
# reset and keyframe options
# namespace monitor


import os, os.path, glob
import maya.cmds as cmds
import xml.etree.ElementTree as ET





curDir = os.path.split(__file__)[0]
curIcons = os.path.join(curDir, "icons")

# Open and Close xml
xmlFile = open( os.path.join(curDir, "icons.xml") )
print(xmlFile)

xmlIcons = ET.parse(xmlFile)

elem = xmlIcons.getroot()
print(elem[0])
''''''
xmlFile.close()


"""
# get the files
icons = glob.glob( os.path.join(curIcons, "*.xpm"))

for i, icon in enumerate(icons):
	# Need to decide if we need a new row.
	# Break up current icon
	# icon will be the entire path.
	fileName = os.path.split(icon)
	fileParts = os.path.splitext(fileName)
	iconPieces = fileParts[0].split("_")	
	
	# Current Row
	curRow = iconPieces[1]
	# Current Column
	curCol = iconPieces[1]
	# rowColumn function
	# takes width, height, & number of elements.
	# returns created layout
	
	# Might be able to return all the widths or heights from the xml at one time.
	
	if(curRow == 0):  # Create a new rowColumnLayout
		curRowCol = cmds.rowColumnLayout(nc=??, cw=??)
		allRowCols.append(curRowCol)

	if( iconPieces[-1] == "pic" ):
		cmds.picture(image=icon)
	elif( iconPieces[-1] == "ctrl" ):
		cmds.symbolButton(image=icon)
	elif( iconPieces[-1] == "cb" )
		cmds.symbolCheckBox( image=icon,
			onImage=icon,
			offImage=icons[i+1])
	# off cb is skipped because "off" isn't check for.
	
	# rowColumn method setParent
	# or formLayout.
		
"""
'''
XML
# Open
file = open(filename, "r")
# Parse
tree = parse(file)
# Get Root
elem = tree.getroot()
'''

'''
Accessing elements

Searching


'''

