'''
Image convert
- Convert images files from one director to xpm.
If elements are selected in the textScrollList then only they will be
converted.
'''
import maya.cmds as cmds
import os
# The os module will give you access to different 
#   operating systems properties.

def gui():
	'''
	GUI for Image convert script.
	'''
	
	win = "mecCVTWin"
	winWidth = 200
	winHeight = 369
	
	if( cmds.window(win, q=True, ex=True) ):
		cmds.deleteUI(win)
		
	cmds.window(win, title="Image Converter", w=winWidth, h=winHeight)
	cmds.columnLayout("mecCVTMC")
	
	cmds.button(label="Get Directory", w=200,
		c="mecConvert.pickFolder()")
	cmds.scrollField( "mecCVTDir", w=winWidth,
		editable=False, wordWrap=True, text='Choose Directory' )
	# cmds.text("mecCVTDir", label="")
	
	cmds.textScrollList("mecCVTTSL", w=winWidth, h=200,
		allowMultiSelection=True)
	cmds.rowColumnLayout(nc=2, cw=[[1,100],[2,100]])
	cmds.button(label="Remove ALL",
		c="mecConvert.cmds.textScrollList('mecCVTTSL', e=True, ra=True)")
	cmds.button(label="Remove Selected",
		c="mecConvert.tslRemSel()")
	cmds.setParent("..")
	cmds.button(label="Convert", w=200,
		c="mecConvert.convert()")
	cmds.picture(image="sbaLogo.xpm", w=210, h=20)
	
	cmds.showWindow(win)
	
def tslRemSel():
	'''
	Remove selected elements from the textScrolList
	'''
	# Grab selected elements from the textScrollList.
	tslSel = cmds.textScrollList("mecCVTTSL", q=True, si=True)
	# Remove them one by one.
	if(tslSel):
		for tsl in tslSel:
			cmds.textScrollList("mecCVTTSL", e=True, ri=tsl)
	
	
def pickFolder():
	'''
	Brings up a file browser dialog.
	- For this script I wish to select a directory instead of a file.
	Two options need to be set to pick diectories.
	mode=4 & tm="folder" 
	- The fileBrowserDialog needs to call a directory 
	fc=tslLoader --> this is the directory
	an="Choose Directory --> Label on the Dialog
	'''
	fileName = cmds.fileBrowserDialog( m=4, tm="folder", 
		fc=tslLoader, an="Choose Directory" )



def tslLoader( fileName, fileType):
	'''
	This function is loaded from the fileBrowserDialog.
	- The fileBrowserDialog passes two values to this function automaticly
	fileName --> file name and path of selected directory/file
	fileType --> What type of file is selected.
	'''
	# Remove everything in the textScrollList
	cmds.textScrollList("mecCVTTSL", e=True, ra=True)
	# Update the scrollField with the selected path.
	cmds.scrollField( "mecCVTDir", e=True, text=fileName)
	
	# Return the files in the chosen directory
	files = os.listdir(fileName)
	# Apply those files to the textScrollList
	cmds.textScrollList("mecCVTTSL", e=True, append=files)
	# return 1 means the dialog prompt worked correctly.
	# Only integers values are reconized during this return.
	return 1

def convert():
	'''
	Convert chosen files into xpm.
	'''	
	# Grab the path from the ScrollField
	targetPath = cmds.scrollField( "mecCVTDir", q=True, text=True)
	
	# Grabbing the selected elements from the textScrollList
	tslSel = cmds.textScrollList("mecCVTTSL", q=True, si=True)
	
	# - Checking to see if anything is selcted in the textScrollList
	#   if nothing is selected grab everything.
	if( not(tslSel) ):
		print("Nothing selected in textScrollList Selected.\n Converting everything.")
		tslSel = cmds.textScrollList("mecCVTTSL", q=True, ai=True)

	
	for tsl in tslSel:
		# Creating the proper path to the files.
		# split file up to get the file name with out the extension.
		baseFile = tsl.split(".")[0]
		destFile = '"' + targetPath + "/""" + baseFile + '.xpm"'
		
		sourceFile = '"' + targetPath + "/" + tsl + '"'
		
		# Switching from front slashes to backslashes if on a windows machine.
		if(cmds.about(os=True) == "nt"):
			destFile = convertSlashes( destFile )
			sourceFile = convertSlashes( sourceFile )
			
		# Compiling the command line to convert the images.
		runLine = 'imconvert ' + sourceFile + " " + destFile
		print(runLine)
		# Executing the imconvert program from the command prompt (DOS)
		os.popen2(runLine)

def convertSlashes( filePath, osType="nt" ):
	'''
	This function will convert backslashes to frontslashes and visa versa.
	filePath(string) --> The entire file path.
	osType(string) --> Anything other than nt will convert backslashes to front slashes.
	'''
	newPath = ""
	if(osType=="nt"):
		pathPieces = filePath.split("/")
		for i, pathPiece in enumerate(pathPieces):
			if( i < len(pathPieces) - 1):
				newPath += pathPiece + "\\"
			else:
				newPath += pathPiece
	else:
		pathPieces = filePath.split("\\")
		for i, pathPiece in enumerate(pathPieces):
			if( i < len(pathPieces) - 1):
				newPath += pathPiece + "/"
			else:
				newPath += pathPiece	
	# Return the converted path.			
	return newPath

"""
Script Notes
import os
os.popen2('imconvert c:\\a.bmp c:\\a.xpm')
# list all the contents of the directory
os.listdir("c:\\")



Notes on creating a textScrollList with no repeating elements.
- How many components are entering?  One or multiple
One!
use the count method that is part of the list command.

if( aList.count(var) == 0 )
	aList.append(var)
	
Multiple
You could use sets.
A set can only contain unique elements.

temp1 = set(aList)
temp2 = set(inputList)
# Return unique elements from both sets
newList = set(aList) ^ set(inputList)
# Or just return the different and append it to the textScrollList
# b - a
newlist = set(inputList) - set(aList)


aList = cmds.ls(sl=True)
aCurrent = cmds.ls(sl=True)

newList = set(aCurrent) - set(aList)
"""

def tslAdd(tslName, tslNew=[]):
	'''
	Add elements in a textScrollList while checking to see
	  if duplicates exists.  If no list is given then the items in the 
	  scene will be grabbed.
	tslName(string) --> Name of the textScrollList to add to.
	tslNew(string) --> New elements to add to the textScrollList
	'''
	tslOld = cmds.textScrollList(tslName, q=True, ai=True)
	if(not(tslNew)):
		tslNew = cmds.ls(sl=True)
	newList = []
	
	# Check to see if anything exists in the textScrollList.
	if(tslOld):	
		newList = myAlone(tslOld, tslNew)
	else:
		newList = myAlone([], tslNew)
	cmds.textScrollList(tslName, e=True, append=newList)


def myAlone(tslOld, tslNew):
	'''
	Using sets this function returns only unique elements from the
	  new list.
	'''
	newList = set(tslNew) - set(tslOld)
	return list(newList)
	
	
"""
Script Notes
cmds.textScrollList("myTSL", e=True, ra=True)
cmds.textScrollList("myTSL", e=True, append=cmds.ls(sl=True))
"""

