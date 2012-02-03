'''
TDClub Meeting
Files Part 2
Paths 
Practical Example

Description:
	The script shows how to get and manipulate file paths.
	
	
import tdClubFiles2
reload(tdClubFiles2)
tdClubFiles2.gui()

'''


'''
Dynamic GUI creation
'''
import maya.cmds as cmds
import os, os.path, glob

# Main

# Tabs

# Frames

# Files

win = "tdClubWin"
winWidth = 300
winHeight = 300
scriptName = __name__
# Main
def gui():
	'''
	Gui element for getting the desired path.
	'''
	
	global mainCol
	
	if( cmds.window(win,q=True, ex=True) ):
		cmds.deleteUI(win)
		
	cmds.window( win, w=winWidth, h=winHeight)
	# mainCol = cmds.columnLayout()
	mainCol = cmds.rowColumnLayout( nc=1, w=winWidth, h=winHeight, cw=[1,winWidth+10])	
	# Get proper directory.
	# Focus on a directory in the maya folder
	scriptDir = cmds.internalVar(userAppDir=True)
	scriptDir = os.path.join(scriptDir, "testDir") # Result: C:/Documents and Settings/mclavan/My Documents/maya/scripts # 
	
	# Does the directory exists?
	# If it does then execute the script.
	if(os.path.exists(scriptDir)):
		print("Run Script")
		#print(scriptDir)
		#print(os.walk(scriptDir).next()[0])
		tabDirs = os.walk(scriptDir).next()[1]
		tdTab(scriptDir, tabDirs, mainCol )
		
	else:
		print("Directory doesn't exists.")
		
	cmds.showWindow(win)
def tdTab(myPath, myDirs, parent):
	'''
	Depending upon how many directory are located in the folder,
		create tabs for each one.
	'''
	print("Create tabs")
	
	# On the nuke side this will be the folder that contain the render passes.
	
	cmds.setParent(parent)
	global tabs, mainTab
	tabs = []
	mainTab = cmds.tabLayout(w=winWidth, h=winWidth, p=parent)	
	# Just create the tabs
	for myDir in myDirs:

		# tabMainCol = cmds.columnLayout()
		tabMainCol = cmds.rowColumnLayout( nc=1, w=winWidth, h=winHeight, cw=[1,winWidth+10])
		# tabMainCol = cmds.formLayout()
		
		#cmds.text(l="This is tab: %s" %myDir, w=winWidth, h=winHeight)
		# Call frameLayout function
		framePath = os.path.join(myPath, myDir)
		frameDirs = os.walk(framePath).next()[1]
		#print(framePath)
		#print(frameDirs)
		tdFrame(framePath, frameDirs, tabMainCol )		
		
		tabs.append(tabMainCol)
		cmds.tabLayout(mainTab, e=True, tl=[tabMainCol, myDir])
		cmds.setParent(mainTab)
		
	cmds.setParent(parent)
	return tabs
	
def tdFrame(framePath, frameDirs, parent):
	'''
	Generates frames for each directory
	'''
	print("Create Frames")
	
	global frames
	frames = []
	# mainTab = cmds.tabLayout(w=winWidth, h=winWidth, p=parent)	
	# Just create the tabs
	mainScroll = cmds.scrollLayout(w=winWidth+10, h=winHeight)
	row = cmds.rowColumnLayout(nc=1, w=winWidth+10, h=winHeight, cw=[1,winWidth-15])
	for frameDir in frameDirs:
		
		tempFrame = cmds.frameLayout(label=frameDir, w=winWidth, cll=True, cl=True)
		frameCol = cmds.columnLayout(w=winWidth)
		
		# Run symbol button creator script
		# cmds.text(label="This is frame: %s" %frameDir, w=winWidth, h=winHeight/3)
		
		filePath = os.path.join(framePath, frameDir)
		files = os.walk(filePath).next()[2]
		print(filePath)
		print(files)
		imports = dynGUI(filePath, files, frameCol )					

		
		cmds.setParent(row)
		frames.append(tempFrame)
	
	cmds.setParent(parent)
	
def dynGUI( filePath, items, parent ):
	'''
	
	filePath(string) is the filePath that each file will be at.
	items(string list) will be files or directories
	parent(string) which gui component will the the newly created gui components will be connected to.
	'''
	
	# items will be formatted correctly so only what is needed is included.
	# keeping track of all the gui components created.
	guiCom = []
	
	'''
	newPath = os.path.join( filePath,item )
	files = glob.glob( os.path.join(newPath,"*.mb") )
	'''
	
	# Mainlayout for the gui.
	items = glob.glob( os.path.join(filePath, "*.mb"))
	print("here is glob")
	print( os.path.join(filePath, "*.mb") )
	print(items)
	cmds.setParent(parent)
	mainRow = cmds.rowColumnLayout( nc=2, cw=[[1,winWidth/2],[2, winWidth/2]] )
	
	for item in items:
	
		
		
		# Need to check to see if there is an image version like it.
		# Extra the file name
		fileParts = os.path.split(item)
		fileParts = os.path.splitext(fileParts[1])
		
		# Check to see if the image exists?
		'''
		iconBtn = cmds.button( w=winWidth/2, h=30, label=fileParts[0], parent=mainRow,
			c="print('Load file: %s')" %(item))
		'''
		iconBtn = cmds.iconTextButton( label=fileParts[0],  style="iconAndTextHorizontal",
			 marginWidth=10,   marginHeight=5, labelOffset=5,
			w=winWidth/2, h=50 , parent=mainRow,
			c=scriptName + ".cmds.file(r'%s', i=True )" %item)
			#c="print('Load file: %s')" %(item))
	
		# file -i "C:/Users/mclavan/Documents/maya/testDir/body/frm1/bones.mb";

		if( os.path.exists(os.path.join(filePath,fileParts[0]+".xpm")) ):
			cmds.iconTextButton(iconBtn, edit=True, image=os.path.join(filePath,fileParts[0]+".xpm") )
		elif( os.path.exists(os.path.join(filePath,fileParts[0]+".bmp")) ):
			cmds.iconTextButton(iconBtn, edit=True, image=os.path.join(filePath,fileParts[0]+".bmp") )
		else:
			print("Didn't find a match. %s  != %s" %(os.path.join(filePath,fileParts[0]+".xmp"), item))
		''''''
		print("Icon Button:%s %s" %(item, iconBtn))
		guiCom.append(iconBtn)
	
		
	return guiCom		
