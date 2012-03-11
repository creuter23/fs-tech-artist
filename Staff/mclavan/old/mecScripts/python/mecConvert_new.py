'''
Image convert
- Convert images files from one director to xpm.
If elements are selected in the textScrollList then only they will be
converted.

How to Run:

import mecConvert
mecConvert.gui()
'''
import maya.cmds as cmds
import os
# The os module will give you access to different 
#   operating systems properties.
scriptName = __name__
imgCtrl = "mecCnvImg"
imgInfo = "mecCnvTxt"

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
	mainCol = cmds.columnLayout("mecCVTMC")
	
	cmds.button(label="Get Directory", w=200,
		c=pickFolder)
	cmds.scrollField( "mecCVTDir", w=winWidth,h=75,
		editable=False, wordWrap=True, text='Choose Directory' )
	# cmds.text("mecCVTDir", label="")
	
	cmds.textScrollList("mecCVTTSL",h=200, w=200, 
		allowMultiSelection=True,
		selectCommand=imgLoadImg)
	cmds.rowColumnLayout(nc=2, cw=[[1,100],[2,100]])
	cmds.button(label="Remove ALL",
		c=removeAll)
	cmds.button(label="Remove Selected",
		c=tslRemSel)
	cmds.setParent("..")
	cmds.button(label="Convert", w=200,
		c=convert)
	
	guiViewer()
	cmds.setParent(mainCol)	
	cmds.picture(image="sbaLogo.xpm", w=210, h=20)
	
	cmds.showWindow(win)

def removeAll(*args):
	cmds.textScrollList('mecCVTTSL', e=True, ra=True)
	
def guiViewer():
	'''
	Displays the image
	'''
	DynFrm = cmds.frameLayout("mecCnvFrm", label="Preview Image", cll=True, w=200)
	dynRow = cmds.rowColumnLayout("mecCnvRC",nc=1, cw=[1,200])
	'''
	dynScroll = cmds.scrollLayout( w=200,
		horizontalScrollBarThickness=8,
		verticalScrollBarThickness=16, h=100)
	dynRow2 = cmds.rowColumnLayout( nc=1, cw=[1,220])
	'''
	# Determine which type of image it is.
	# if its xpm use picture
	# else image
	cmds.picture(imgCtrl, image="imageViewer.xpm", h=43)
	# cmds.setParent(dynRow)
	cmds.text(imgInfo, label="Image Size", w=200, h=25, align="center",
		parent=dynRow)
	# Determin the size of the image



def imgLoadImg(*args):
	# mainLayout
	# imgCtrl
	# imgInfo
	filePath = cmds.scrollField( "mecCVTDir", q=True, text=True)

	currImage = cmds.textScrollList( "mecCVTTSL", q=True, si=True)[0]  #Only the first item
	import os.path
	fullPath = os.path.join( filePath, currImage )

	imgSize = imageSize( fullPath )
	
	
	cmds.deleteUI("mecCnvRC")
	# Regenerate the images
	dynRow = cmds.rowColumnLayout("mecCnvRC",nc=1, cw=[1,200],
		parent="mecCnvFrm")
	dynScroll = cmds.scrollLayout( w=200, parent=dynRow,
		horizontalScrollBarThickness=8,
		verticalScrollBarThickness=16, h=100)
	
	dynRow2 = cmds.rowColumnLayout( nc=1, cw=[1,imgSize[0]+10], parent=dynScroll)
	if(os.path.isfile(fullPath) ):	
		if( currImage.split(".")[-1] in ["xpm","bmp"] ):
			cmds.picture( image=fullPath, parent=dynRow2,
				w=imgSize[0]+20, h=imgSize[1]+20)
		else:
			cmds.image( image=fullPath, parent=dynRow2,
				w=imgSize[0], h=imgSize[1])
			# cmds.text( label="", h=20, w=imgSize[0]+20, parent=dynRow2)
	
		cmds.setParent(dynRow)
	else:
		cmds.text(label="Chosen file isn't an image.", parent=dynRow)	
	''''''
	cmds.text(label="Image Size: %sx%s" %(int(imgSize[0]), int(imgSize[1])), 
		w=200, h=25, align="center",
		parent=dynRow)
	# mainRow = cmds.rowColumnLayout( nc=1, cw=[1,180], parent="mecCnvSL")
	
	# Determine which type of image it is.
	# if its xpm use picture
	# else image
	# cmds.picture( image=fullPath, parent=mainRow)
	# cmds.text( label="Image Size: %sx%s" %(int(imgSize[0]), int(imgSize[1])), w=200, h=30, align="center", parent=mainRow)	
	
def imageSize(imgPath):
	tempFile = cmds.createNode( 'file' )
	currImage = imgPath
	cmds.setAttr( "%s.fileTextureName" %tempFile, currImage, type="string")
	
	# Do typical getting of info
	fileName = cmds.getAttr( "%s.fileTextureName" %tempFile )
	xSize= cmds.getAttr( "%s.outSizeX" %tempFile )
	ySize = cmds.getAttr( "%s.outSizeY" %tempFile )
	
	print( "%s  %s  %s" %(20*"-", file, 20*"-"))
	print( "FileName: %s\nDimensions: %s x %s" %(fileName, xSize, ySize))               
	print( 50*"-" )
	# Delete file node
	cmds.delete(tempFile)

	return [xSize, ySize, fileName]

def tslRemSel(*args):
	'''
	Remove selected elements from the textScrolList
	'''
	# Grab selected elements from the textScrollList.
	tslSel = cmds.textScrollList("mecCVTTSL", q=True, si=True)
	# Remove them one by one.
	if(tslSel):
		for tsl in tslSel:
			cmds.textScrollList("mecCVTTSL", e=True, ri=tsl)
	
	
def pickFolder(*args):
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

def convert(*args):
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

