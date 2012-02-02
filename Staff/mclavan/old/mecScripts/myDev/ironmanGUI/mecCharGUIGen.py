'''
#cri_advGirl_gui_me.py
# C:\Users\mclavan\Documents\My Dropbox\00_SBA_Admin\classMaterials\criLecture10_new\


How to Run:

import mecCharGUIGen.py
reload(mecCharGUIGen.py)
mecCharGUIGen.py.gui()
'''


import maya.cmds as cmds
import os, os.path, glob

# Setting up the icon paths

imgPath = os.path.split(__file__)
# iconPath = os.path.join(imgPath, "icons")
iconCharPath = os.path.join(imgPath[0], "icons", "char_icons")
iconPath = os.path.join(imgPath[0], "icons", "other_icons")


def gui():
	'''
	This function generates the window for adventure girl's interface.
	'''
	win = "mecIronWin"
	winWidth = 262
	winHeight = 277
	
	if( cmds.window( win, q=True, ex=True) ):
		cmds.deleteUI(win)
		
	cmds.window(win, title="Ironman Selection Rig", w=winWidth, h=winHeight)
	mainCol = cmds.columnLayout()
	
	# Char Selection goes here
	visCntrls(mainCol)
	
	charSelFrm = cmds.frameLayout( cll=True, label="Character Select" )
	advSelGui = CharSelectGUI(iconCharPath, charSelFrm)
	cmds.setParent(mainCol)
	
	cmds.showWindow(win)
	
	print("Ironman GUI")

def visCntrls(curParent):
	'''
	Different visibility controls for character.
	'''

	imgDef = lambda x: os.path.join( iconPath, x )
	
	visRC = cmds.rowColumnLayout( nc=5, cw=[[1,60],[2,60],[3,60],[4,60],[5,60]], parent=curParent)
	cmds.symbolButton( image=imgDef( 'outliner.xpm' ), w=60, h=45 )
	cmds.symbolButton( image=imgDef( 'mainRig.xpm' ), w=60, h=45 )
	
	jointVis = cmds.symbolCheckBox(image=imgDef("JointVis_On.xpm"), w=60, h=45,
		oni=imgDef("JointVis_On.xpm") ,
		ofi=imgDef("JointVis_Off.xpm") )
	# cmds.connectControl( jointVis, "rig.v")
	
	ctrlVis = cmds.symbolCheckBox(image=imgDef("ctrlVis_On.xpm"), w=60, h=45,
		oni=imgDef("ctrlVis_On.xpm") ,
		ofi=imgDef("ctrlVis_Off.xpm") )
	cmds.symbolCheckBox(image=imgDef("keySel_on.xpm"), w=60, h=45,
		oni=imgDef("keySel_on.xpm") ,
		ofi=imgDef("keySel_off.xpm") )

	# cmds.connectControl( ctrlVis, "move_all_control.visibility")
	
	# Row and High Rez
	
	# Dress
	
	# Face Controls
	
	# T-Pose

	cmds.setParent(curParent)
	



'''
#
#
Where is the error check for files that aren't apart the character selection area.
Or if there is expansion. (SymbolCheckBox)
#
#

'''

def selectCtrl(self, ctrl, switchMode=None, addMode=False ):
	'''
	Selects the control icons.
	'''
	prefSwitch = True
	
	# Prefered switch
	if( prefSwitch and switchMode ):
		# Switch to the proper mode
		if( switchMode.lower() == "rotate" ):
			cmds.RotateTool()
		else:
			cmds.MoveTool()			
		
		print("Switching to %s." %switchMode)
	
		
		if( addMode ):
			cmds.select( ctrl, add=True )
		else:
			cmds.select( ctrl, replace=True )

import cPickle as pickle			
			
class CharSelect_Base(object):
	# This class needs to create the layout structure for the character selection area.
	def __init__(self, imgPath, curParent=None):
		self.frmLayout = cmds.formLayout(parent=curParent)
		# It needs create all the gui components.
		# Loop through all the images calling the IMG class for each one
		self.imgPath = imgPath
			
		self.processImages()
		cmds.setParent(curParent)
		
	def processImages(self):
		imagePaths = glob.glob(os.path.join( self.imgPath, '*.xpm'))
		# I need to determine how many rows there are?
		# I will also need place gui components it the proper row, to be placed later.
		# The rows list will contain all the IMG instances in there proper order.
		
		self.rows = {}
		# The internal list will be the IMG instance
		# self.rows = [[row1], [row2], [row3] ]
		#                       Row 1                          Row 2           ...
		# self.rows = [[img1, img2, img3, img4, img5], [img6, img7, img8, img9], etc...]
		#			    columnLayout
		# self.rows = [[img1, img2, [img3,img4], img5, img6], [img6, img7, img8, img9], etc...]
		# The internal list will be the IMG instance
		# self.rows = {1: [imgs], 2: [imgs], 3: [imgs] }
		#                       Row 1                          Row 2           ...
		# self.rows = {1:[img1, img2, [img3,img4], img5, img6], 2:[img6, img7, img8, img9], etc...]
		# 			      stacked imgs
		
		# First place place components under formLayout
		for curPath in imagePaths:
			# This loop with call the IMG class for each gui component 
			# that is needed.  It will store them to be placed later.
			curIMG = IMG_Gui(curPath, self.frmLayout, 1)
			# Determining which row it should be in.
			
			# Are we at a new row or does the row currently exists?
			if( self.rows.has_key(curIMG.row) ):
				# Check to see if there is a stacked column
				if( curIMG.subColumn ):
					if( curIMG.subColumn == 1 ):
						self.rows[curIMG.row].append( [curIMG] )
					else:
						self.rows[curIMG.row][-1].append( curIMG )
				else:
					self.rows[curIMG.row].append(curIMG) 
			else:
				if( curIMG.subColumn ):
					if( curIMG.subColumn == 1 ):
						self.rows[curIMG.row] = [[curIMG]]
						# Else shouldn't be required because if were are 
						#   at the second column then the row exists.  
						#   It will reside in the statement above.
				else:			
					self.rows[curIMG.row] = [curIMG]
	
		self.numOfRows = len(self.rows)
		# print("Num of Rows: %s" %self.numOfRows, self.rows)
		

		# Second place them in proper order
		for row in range( 1, self.numOfRows+1 ):
			# First Row All Connected to top
			# First Item of each row 
			# Top
			# Previous
			topItem = None
			leftItem = None
			
			'''
			for g in self.rows[row]:
				if( type(g) == list ):
					print(row, [ item.fileName for item in g ] ) # [elem*2 for elem in li]
				else:
					print(row, g.fileName)
			print("")				
			'''	
			'''
			This all has to be printed out first.
			'''
			for rowItem in self.rows[row]:
				# Top
				if( row == 1 ):
					# Top should remain None
					# FormConnect top
					if( type(rowItem) != list and rowItem.column == 1 ):
						# Are we column 1
						# if so connect to leftForm
						# print( "FileName: %s Attached to TOP: Form & LEFT: Form" %(rowItem.fileName) )
						cmds.formLayout(self.frmLayout, edit=True, 
							attachForm=[[rowItem.gui, "top", 0],[rowItem.gui, "left", 0]])
						# Setting new left
						leftItem = rowItem
					# elif( type(rowItem) == list and rowItem # Needs to loop through each list element
					elif( type(rowItem) == list):
						# First Column of the First Row
						# Attach to Form TOP and Left
# This isn't corrent it will only check for the first column
# It needs to build the sub columns regardless.
						subTop = None
						if( rowItem[0].column == 1):
							for subCol in range( 0, len(rowItem)):
								# Loop through all the sub columns
								if( rowItem[subCol].subColumn == 1 ):
									# Normal top and normal left
									cmds.formLayout(self.frmLayout, edit=True, 
										attachForm=[[rowItem[subCol].gui, "top", 0],
										[rowItem[subCol].gui, "left", 0]])								
									subTop = rowItem[subCol]
								else:
									# subCol top and normal left
									cmds.formLayout(self.frmLayout, edit=True, 
										attachForm=[rowItem[subCol].gui, "left", 0],
										attachControl=[rowItem[subCol].gui, "top", 0, subTop.gui])	
									subTop = rowItem[subCol]
							leftItem = rowItem[0]		
						else:
							for subCol in range( 0, len(rowItem)):
								# Loop through all the sub columns
								if( rowItem[subCol].subColumn == 1 ):
									# Normal top and normal left
									cmds.formLayout(self.frmLayout, edit=True,
										attachControl=[rowItem[subCol].gui, "left", 0, leftItem.gui],
										attachForm=[rowItem[subCol].gui, "top", 0])								
									subTop = rowItem[subCol]
								else:
									# subCol top and normal left
									cmds.formLayout(self.frmLayout, edit=True, 
										attachControl=[[rowItem[subCol].gui, "top", 0, subTop.gui],
											[rowItem[subCol].gui, "left", 0, leftItem.gui]])	
									subTop = rowItem[subCol]
							leftItem = rowItem[0]
					else:
						# Connect to the item to our left
						cmds.formLayout( self.frmLayout, edit=True,
							attachForm=[rowItem.gui, "top", 0],
							attachControl=[rowItem.gui, "left", 0, leftItem.gui])
						# print( "FileName: %s Attached to TOP: Form & LEFT: %s" %(rowItem.fileName, leftItem.fileName) )
						
						# Setting new left						
						leftItem = rowItem
						
				else:
					# top in this case will always be row-1, column 1
					# rows[top][0]
					topItem = self.rows[row-1][0]
					if( type(topItem) == list): #Its a subColumn
						# Get lowest subColumn
						topItem = self.rows[row-1][0][len(topItem)-1]
						
					# ControlConnect row-1
					if( type(rowItem) != list and rowItem.column == 1):
						# Are we column 1
						# if so connect to leftForm
						# print( "FileName: %s Attached to TOP: Form & LEFT: Form" %(rowItem.fileName) )
						cmds.formLayout(self.frmLayout, edit=True,
							attachControl=[rowItem.gui, 'top', 0, topItem.gui],
							attachForm=[rowItem.gui, "left", 0])
						# Setting new left
						leftItem = rowItem
					elif( type(rowItem) == list):
						# First Column of the SubColumn Stacked Buttons
						# Attach to Form TOP and Left
						
						subTop = None
						if( rowItem[0].column == 1):
							for subCol in range( 0, len(rowItem)):
								# Loop through all the sub columns
								if( rowItem[subCol].subColumn == 1 ):
									# Normal top and normal left
									cmds.formLayout(self.frmLayout, edit=True, 
										attachForm=[rowItem[subCol].gui, "left", 0],
										attachControl=[rowItem[subCol].gui, "top", 0, topItem.gui])								
									subTop = rowItem[subCol]
								else:
									# subCol top and normal left
									cmds.formLayout(self.frmLayout, edit=True, 
										attachForm=[rowItem[subCol].gui, "left", 0],
										attachControl=[rowItem[subCol].gui, "top", 0, subTop.gui])	
									subTop = rowItem[subCol]
							leftItem = rowItem[0]		
						else:
							for subCol in range( 0, len(rowItem)):
								# Loop through all the sub columns
								if( rowItem[subCol].subColumn == 1 ):
									# Normal top and normal left
									cmds.formLayout(self.frmLayout, edit=True,
										attachControl=[[rowItem[subCol].gui, "left", 0, leftItem.gui],
										[rowItem[subCol].gui, "top", 0, topItem.gui] ])								
									subTop = rowItem[subCol]
								else:
									# subCol top and normal left
									cmds.formLayout(self.frmLayout, edit=True, 
										attachControl=[[rowItem[subCol].gui, "top", 0, subTop.gui],
											[rowItem[subCol].gui, "left", 0, leftItem.gui]])	
									subTop = rowItem[subCol]
							leftItem = rowItem[0]
	
					else:
						# Connect to the item to our left
						cmds.formLayout( self.frmLayout, edit=True,
							attachControl=[[rowItem.gui, 'top', 0, topItem.gui],[rowItem.gui, "left", 0, leftItem.gui]])
						# print( "FileName: %s Attached to TOP: %s & LEFT: %s" %(rowItem.fileName, topItem.fileName, leftItem.fileName) )
						
						# Setting new left						
						leftItem = rowItem						

	

class CharSelectGUI(CharSelect_Base):
	'''
	This class loads up a character selection area complete with connected controls,
		these controls will be loaded from a file that was setup by the CharSelect_Input Class
	'''
	def __init__(self, imgPath, curParent=None):
		CharSelect_Base.__init__(self, imgPath, curParent)	
		
		self.loadCtrls()
		self._setupCtrlEnv()
		
	def _setupCtrlEnv(self):
		# Loop through all the controls
		for i, row in self.rows.items():
			for m, ctrl in enumerate( row ):
				if( type(ctrl) != list):
					if( ctrl.ctrlType == "ctrl" or ctrl.ctrlType == "chk" ):
						# self.ctrls[ctrl.fileName] = None
						ctrl.setCommand( Callback(self.ctrlSystem, ctrl.fileName ) )
				elif( type(ctrl) == list):
					for subCol in range( 0, len(ctrl)):
						if(ctrl[subCol].ctrlType == "ctrl" or ctrl[subCol].ctrlType == "chk" ):
							ctrl[subCol].setCommand( Callback(self.ctrlSystem, ctrl[subCol].fileName ) )
					
	# control fileName folderName.mec  "charSel.mec"
	def ctrlSystem(self, ctrl):

		if( self.ctrls[ctrl][0] ):
			cmds.select( self.ctrls[ctrl][0], r=True)
			if( self.ctrls[ctrl][1] == "rotate" ):
				cmds.RotateTool()
			elif( self.ctrls[ctrl][1] == "trans" ):
				cmds.MoveTool()				
		else:
			print("Nothing setup.")	


	def selectCtrl(self, ctrl, switchMode=None, addMode=False ):
		'''
		Selects the control icons.
		'''
		prefSwitch = True
		
		# Prefered switch
		if( prefSwitch and switchMode ):
			# Switch to the proper mode
			if( switchMode.lower() == "rotate" ):
				cmds.RotateTool()
			else:
				cmds.MoveTool()			
			
			print("Switching to %s." %switchMode)
		
			
			if( addMode ):
				cmds.select( ctrl, add=True )
			else:
				cmds.select( ctrl, replace=True )
			
	def loadCtrls(self):
		self.dataName = os.path.split(self.imgPath)[-1] + ".mec"
		fullPath = os.path.join( os.path.split(self.imgPath)[0], self.dataName )
		myFile = open( fullPath, 'r' )
		fileInfo = pickle.load( myFile )
		myFile.close()
		
		self.ctrls = fileInfo
		
		
class CharSelect_Input(object):
	'''
	This should create its own window.  So I can setup the inputs
	'''
	def __init__(self, imgPath):
		# CharSelect_Base.__init__(self, imgPath, curParent)
		self.imgPath = imgPath
		
		self.ctrls = {}
		
		self._win = cmds.window( title="Character Selection Setup", menuBar=True )
		cmds.menu(label="Setup")
		cmds.menuItem( label="Show", command=Callback(self.showCtrls))
		cmds.menuItem( label="Load", command=Callback(self.loadCtrls))
		cmds.menuItem( label="Save", command=Callback(self.saveCtrls))
		cmds.menuItem( divider=True )
		self.testMode = cmds.menuItem( label="Test Mode", checkBox=False )
		self._mainCol = cmds.columnLayout()

		self.charSel = CharSelect_Base( self.imgPath, self._mainCol )
		
		cmds.showWindow( self._win )
		cmds.window( self._win, edit=True, title="Character Selection Setup: %s" %self.charSel.rows[1][0].name)
		self.setupCtrlEnv()
		# print(self.charSel.rows.items())
		
	# Current image needs to give control here to set its values
	def setupCtrlEnv(self):
		# Loop through all the controls
		for i, row in self.charSel.rows.items():
			for m, ctrl in enumerate( row ):
				if( type(ctrl) != list):
					if( ctrl.ctrlType == "ctrl" or ctrl.ctrlType == "chk" ):
						# self.ctrls[self.charSel.rows[i][m]] = "It's a control"   # Temp for setting up the control
						self.ctrls[ctrl.fileName] = [[], None]
						ctrl.setCommand( Callback(self.ctrlSystem, ctrl.fileName ) )
						pop = cmds.popupMenu( parent=ctrl.gui )
						rbCol = cmds.radioMenuItemCollection( parent=pop)
						cmds.menuItem(label="Rotate", cl=rbCol, rb=False, c=Callback( self._setSwitch, ctrl.fileName, "rotate" ))
						cmds.menuItem(label="Translate", cl=rbCol, rb=False, c=Callback( self._setSwitch, ctrl.fileName, "trans" ))
						cmds.menuItem( divider=True )
						cmds.menuItem(label="None", cl=rbCol, rb=True, c=Callback( self._setSwitch, ctrl.fileName, None ))
				elif( type(ctrl) == list):	
					for subCol in range( 0, len(ctrl)):
						if(ctrl[subCol].ctrlType == "ctrl" or ctrl[subCol].ctrlType == "chk" ):
							self.ctrls[ctrl[subCol].fileName] = [[], None]
							ctrl[subCol].setCommand( Callback(self.ctrlSystem, ctrl[subCol].fileName ) )
							pop = cmds.popupMenu( parent=ctrl[subCol].gui )
							rbCol = cmds.radioMenuItemCollection( parent=pop)
							cmds.menuItem(label="Rotate", cl=rbCol, rb=False, c=Callback( self._setSwitch, ctrl[subCol].fileName, "rotate" ))
							cmds.menuItem(label="Translate", cl=rbCol, rb=False, c=Callback( self._setSwitch, ctrl[subCol].fileName, "trans" ))
							cmds.menuItem( divider=True )
							cmds.menuItem(label="None", cl=rbCol, rb=True, c=Callback( self._setSwitch, ctrl[subCol].fileName, None ))							
					# ctrl.setCommand( Callback(self.ctrlSystem, self.charSel.rows[i][m] ) ) #ctrl.fileName) ) # Trying to pass the instance
					# ctrl.setCommand( "print('Test works')" )
	
	def _setSwitch(self, ctrl, switch):
		self.ctrls[ctrl][1] = switch
		
	# control fileName folderName.mec  "charSel.mec"
	def ctrlSystem(self, ctrl):
		if(cmds.menuItem( self.testMode, q=True, checkBox=True)):
			if( self.ctrls[ctrl][0] ):
				cmds.select( self.ctrls[ctrl][0], r=True)
				if( self.ctrls[ctrl][1] == "rotate" ):
					cmds.RotateTool()
				elif( self.ctrls[ctrl][1] == "trans" ):
					cmds.MoveTool()				
			else:
				print("Nothing setup.")	
					
		else:
			selected = cmds.ls(sl=True)
			self.ctrls[ctrl][0] = selected			
		print("Control: %s Set-> %s" %(ctrl, (",".join(self.ctrls[ctrl][0])) ))
		# Load

		
	def showCtrls(self):
		for ctrl in self.ctrls.keys():
			# I want the name of image and what control it will select
			# print( self.ctrls[ctrl] )
			
			print("Ctrl: %s Command: %s" %(ctrl, self.ctrls[ctrl]))
			''''''
	def saveCtrls(self):
		self.dataName = os.path.split(self.imgPath)[-1] + ".mec"
		fullPath = os.path.join( os.path.split(self.imgPath)[0], self.dataName )
		myFile = open( fullPath, 'w' )
		pickle.dump( self.ctrls, myFile )
		myFile.close()
		
	def loadCtrls(self):
		self.dataName = os.path.split(self.imgPath)[-1] + ".mec"
		fullPath = os.path.join( os.path.split(self.imgPath)[0], self.dataName )
		myFile = open( fullPath, 'r' )
		fileInfo = pickle.load( myFile )
		myFile.close()
		
		self.ctrls = fileInfo
		
	def readCtrls(self):
		self.dataName = os.path.split(self.imgPath)[-1] + ".mec"
		fullPath = os.path.join( os.path.split(self.imgPath)[0], self.dataName )
		myFile = open( fullPath, 'r' )
		fileInfo = pickle.load( myFile )
		myFile.close()

		print(fileInfo)
		
		for ctrl in fileInfo.keys():
			# I want the name of image and what control it will select
			# print( self.ctrls[ctrl] )
			print("Ctrl: %s Command: %s" %(ctrl, fileInfo[ctrl]))	
			
		del fileInfo
		
class IMG(object):
	'''
	This class has the base information for the image.
	This includes the images base name, extention, width, and height
	Data:
		self.imgPath (current file path)
		self.parent (parent gui object)
		self.fullFileName (file name with extension)
		self.fileName (file name with out extension)
		self.fileExt (file extension ".xpm")
		self.width (image width)
		self.heigth (image height)
	'''
	def __init__(self, curImgPath):

		if( os.path.exists( curImgPath ) ):
			self.imgPath = curImgPath
			self.fullFileName = os.path.split(self.imgPath)[-1]
			self.fileName, self.fileExt = os.path.splitext(self.fullFileName)
			self.imgSize()
			
			# print("FileName:  %s  Ext: %s  Width: %s  Heigth: %s" %(self.fullFileName, self.fileExt, self.width, self.height))
		
		else:
			print("Image Path Doesn't exist: %s" %curImgPath)

	def imgSize(self):			
		# Creating a temp file node.
		tempFile = cmds.createNode( 'file' )
		cmds.setAttr( "%s.fileTextureName" %tempFile, self.imgPath, type="string")
		
		# Do typical getting of info
		fileName = cmds.getAttr( "%s.fileTextureName" %tempFile )
		self.width= int(cmds.getAttr( "%s.outSizeX" %tempFile ))
		self.height = int(cmds.getAttr( "%s.outSizeY" %tempFile ))
		
		# Delete file node
		cmds.delete(tempFile)			

class IMG_Gui(IMG):
	'''
	This class inherits the base image information from the IMG class.
	This class also seperates image data into specific data for using the
		images in a character selection gui.
	This class also genrates the proper interface component, based on the 
		naming system in the image name.
	Data: 
		self.parent (parent gui object)
		self.name (base name)
		self.row 
		self.column
		self.subColumn (This contains which sub column the image may need to be.)
		self.ctrlOff (For symbolCheckboxes its off image name, Only "chk")
		self.ctrlType (Control type "img", "ctrl", "chk")
		self.gui (contains name of the interface generated.
	Data (IMG class):
		self.imgPath (current file path)
		self.fullFileName (file name with extension)
		self.fileName (file name with out extension)
		self.fileExt (file extension ".xpm")
		self.width (image width)
		self.heigth (image height)		
	'''
	def __init__(self, curImgPath, parent=None, create=False):
		IMG.__init__(self, curImgPath )
		self.gui=None
		self.parent = parent
		self.imgBreakDown()
		
		if( create ):
			self.create( parent)
		# print("Root:  %s  Row: %.2d  Column: %.2d  Type: %s" %(self.name, self.row, self.column, self.ctrlType))  
	
	def imgBreakDown(self):
		'''
		Breaks the image into pieces so it can be positioned easier.
		'''
		
		pieces = self.fileName.split('_')
		# if( len(pieces) > 3 )
		
		self.name = pieces[0]
		self.row = int(pieces[1])
		self.column = int(pieces[2])
		self.ctrlOff = None
		self.subColumn = None
		self.ctrlType = pieces[-1]
		
		if( len(pieces) == 5 ):
			self.subColumn = int(pieces[3])
			print("Image is a sub: %s col:%s" %(self.fileName, self.subColumn))
			
		if( self.ctrlType == "chk" ):
			self.ctrlOff = self.name.replace("On", "Off") + self.fileExt

	def setCommand(self, cmd, cmdOff=False):
		if( self.ctrlType == "ctrl" ):
			cmds.symbolButton( self.gui, edit=True, command=cmd)
		elif( self.ctrlType == "chk"):
			cmds.symbolCheckBox( self.gui, edit=True, command=cmd)
			cmds.symbolCheckBox( self.gui, edit=True, onCommand=cmd)
			if( cmdOff ):
				cmds.symbolCheckBox( self.gui, edit=True, offCommand=cmdOff)
		if( cmdOff ):
			self.command = [cmd, cmdOff]
		else:
			self.command = cmd
	
	def getCommand(self):
		return self.command
		
	def create(self, parent):
		'''
		Checks to see the type of control it is.
		'''
		if(parent): 
			self.parent = parent
			
		if( self.parent and self.ctrlType == "img"):
			if( ".xpm" == self.fileExt ):
				self.gui = cmds.picture( image=self.imgPath ,w=self.width, h=self.height )
			else:
				self.gui = cmds.image( image=self.imgPath ,w=self.width, h=self.height ) 
		elif( self.parent and self.ctrlType == "ctrl"):
			self.gui = cmds.symbolButton(image=self.imgPath ,w=self.width, h=self.height)
		elif( self.parent and self.ctrlType == "chk"):
			imgDef = lambda x: os.path.join( os.path.split(self.imgPath)[0], x )
		
			self.gui = cmds.symbolCheckBox(image=self.imgPath ,w=self.width, h=self.height,
				onImage=self.imgPath, offImage=imgDef(self.ctrlOff))
				
	
import maya.mel as mel

mel.eval( 'python("import sys")' )


class Callback():
	_callData = None
	def __init__(self,func,*args,**kwargs):
		self.func = func
		self.args = args
		self.kwargs = kwargs
	
	def __call__(self, *args):
		Callback._callData = (self.func, self.args, self.kwargs)
		mel.eval('global proc py_%s(){python("sys.modules[\'%s\'].Callback._doCall()");}'%(self.func.__name__, __name__))
		try:
			mel.eval('py_%s()'%self.func.__name__)
		except RuntimeError:
			pass
		
		if isinstance(Callback._callData, Exception):
			raise Callback._callData
		return Callback._callData 
	
	@staticmethod
	def _doCall():
		(func, args, kwargs) = Callback._callData
		Callback._callData = func(*args, **kwargs)

r"""
# Sample Code
import cri_advGirl_gui_me
reload(cri_advGirl_gui_me)
import maya.cmds as cmds
import os.path
filePath = r'C:\Users\mclavan\Documents\My Dropbox\00_SBA_Admin\classMaterials\criLecture10_new\advGirl_icons_smaller\images\xpm'
cmds.window()
mainCol = cmds.columnLayout()
img1 = cri_advGirl_gui_me.IMG( os.path.join(filePath, 'AdvGirl_01_01_img.xpm') )
img2 = cri_advGirl_gui_me.IMG( os.path.join(filePath, 'AdvGirl_01_02_ctrl.xpm') )
img3 = cri_advGirl_gui_me.IMG( os.path.join(filePath, 'AdvGirl_01_03_ctrl.xpm') )
img4 = cri_advGirl_gui_me.IMG( os.path.join(filePath, 'AdvGirl_01_04_ctrl.xpm') )
img5 = cri_advGirl_gui_me.IMG( os.path.join(filePath, 'AdvGirl_01_05_img.xpm') )


mainRow = cmds.rowColumnLayout(nc=5, 
	cw=[[1,img1.width],[2,img2.width],[3,img3.width], [4,img4.width], [5, img5.width]])
img1.generateGUI(mainRow)
img2.generateGUI(mainRow)
img3.generateGUI(mainRow)
img4.generateGUI(mainRow)
img5.generateGUI(mainRow)
cmds.showWindow()
"""

"""
****************************************************************************************************
****************************************************************************************************
Error Sheet

I also need to check to make sure that the IMG class doesn't get confused with different types of xpm.
xpm that aren't meant for the character selection.

What about expanding symbolCheckBox into it as well.

I want to place multiple button inside of a cell
New naming convension
ironman_01_01_01_ctrl.xpm
ironman_01_01_02_ctrl.xpm
ironman_01_01_ctrl.xpm

symbolCheckbox 
ironmanSelOn_01_01_chk.xpm (images\characterSel_icons folder)
ironmanSelOff.xpm (images\other_icons)
# Replace On with Off
# Check to make sure the file exists.

****************************************************************************************************
****************************************************************************************************

	
def charSelection(curParent):
	'''
	Generates the Character selection part for Adventure Girl
	
	'''
	print("Icon Path: %s" %iconPath)
	frmLayout = cmds.formLayout( parent=curParent )
	
	imgDef = lambda x: os.path.join( iconCharPath, x )
	
	# Good place for a lambda function
	# Row 1
	sel_1_1 = cmds.picture( image=imgDef("AdvGirl_01_01_img.xpm"),
		w=85, h=70)
	sel_1_2 = cmds.symbolButton( image=os.path.join(iconPath, "AdvGirl_01_02_ctrl.xpm"),
		w=16, h=70)
	sel_1_3 = cmds.symbolButton( image=os.path.join(iconPath, "AdvGirl_01_03_ctrl.xpm"),
		w=59, h=70, command=Callback( selectCtrl,"head_control", "rotate"))
	sel_1_4 = cmds.symbolButton( image=os.path.join(iconPath, "AdvGirl_01_04_ctrl.xpm"),
		w=17, h=70)
	sel_1_5 = cmds.picture( image=os.path.join(iconPath, "AdvGirl_01_05_img.xpm"),
		w=85, h=70)
		
	# Row 2
	sel_2_1 = cmds.symbolButton( image=os.path.join(iconPath, "AdvGirl_02_01_ctrl.xpm"), 
		w=42, h=15, command=Callback( selectCtrl,"rt_hand_IK_control") )
	sel_2_2 = cmds.symbolButton( image=os.path.join(iconPath, "AdvGirl_02_02_ctrl.xpm"), 
		w=49, h=15, command=Callback( selectCtrl,"rt_elbow_control","translate") )
	sel_2_3 = cmds.symbolButton( image=os.path.join(iconPath, "AdvGirl_02_03_ctrl.xpm"), 
		w=36, h=15, command=Callback( selectCtrl,"shoulder_control","translate") )
	sel_2_4 = cmds.symbolButton( image=os.path.join(iconPath, "AdvGirl_02_04_ctrl.xpm"), 
		w=38, h=15, command=Callback( selectCtrl,"shoulder_control","translate"))
	sel_2_5 = cmds.symbolButton( image=os.path.join(iconPath, "AdvGirl_02_05_ctrl.xpm"), 
		w=51, h=15, command=Callback( selectCtrl,"lt_elbow_control","translate") )
	sel_2_6 = cmds.symbolButton( image=os.path.join(iconPath, "AdvGirl_02_06_ctrl.xpm"), 
		w=45, h=15, command=Callback( selectCtrl,"lt_hand_IK_control") )
	
	'''
	# Row 3
	sel_3_1 = cmds.symbolButton( image=os.path.join(iconPath, "AdvGirl_03_01_ctrl.xpm"), 
		w=42, h=15, command=Callback( selectCtrl,"rt_hand_IK_control") )
	sel_3_2 = cmds.symbolButton( image=os.path.join(iconPath, "AdvGirl_03_02_ctrl.xpm"), 
		w=49, h=15, command=Callback( selectCtrl,"rt_elbow_control","translate") )
	sel_3_3 = cmds.symbolButton( image=os.path.join(iconPath, "AdvGirl_03_03_ctrl.xpm"), 
		w=36, h=15, command=Callback( selectCtrl,"shoulder_control","translate") )
	sel_3_4 = cmds.symbolButton( image=os.path.join(iconPath, "AdvGirl_03_04_ctrl.xpm"), 
		w=38, h=15, command=Callback( selectCtrl,"shoulder_control","translate"))
	sel_3_5 = cmds.symbolButton( image=os.path.join(iconPath, "AdvGirl_03_05_ctrl.xpm"), 
		w=51, h=15, command=Callback( selectCtrl,"lt_elbow_control","translate") )
	sel_3_6 = cmds.symbolButton( image=os.path.join(iconPath, "AdvGirl_03_06_ctrl.xpm"), 
		w=45, h=15, command=Callback( selectCtrl,"lt_hand_IK_control") )
	sel_3_7 = cmds.symbolButton( image=os.path.join(iconPath, "AdvGirl_03_07_ctrl.xpm"), 
		w=45, h=15, command=Callback( selectCtrl,"lt_hand_IK_control") )	
	'''
	# Row 4

	# Row 5

	# Row 6

	# Row 7

	# Row 8

	# Row 9
	
		
	# Row 1 placement
	cmds.formLayout( frmLayout, edit=True, 
		attachForm=[[ sel_1_1 , "left", 0 ], [ sel_1_1 , "top", 0]])
	cmds.formLayout( frmLayout, edit=True, 	
		attachControl=[sel_1_2, "left", 0, sel_1_1 ],
		attachForm=[ sel_1_2 , "top", 0])
	cmds.formLayout( frmLayout, edit=True, 	
		attachControl=[sel_1_3, "left", 0, sel_1_2 ],
		attachForm=[ sel_1_3 , "top", 0])
	cmds.formLayout( frmLayout, edit=True, 	
		attachControl=[sel_1_4, "left", 0, sel_1_3 ],
		attachForm=[ sel_1_4 , "top", 0])
	cmds.formLayout( frmLayout, edit=True, 	
		attachControl=[sel_1_5, "left", 0, sel_1_4 ],
		attachForm=[ sel_1_5 , "top", 0])

	# Row 2 placement
	cmds.formLayout( frmLayout, edit=True, attachForm=[ sel_2_1 , "left", 0 ],
		 attachControl=[ sel_2_1 , "top", 0, sel_1_1 ])

	cmds.formLayout( frmLayout, edit=True, 	
		attachControl=[[sel_2_2,"left", 0, sel_2_1 ],[sel_2_2, "top", 0, sel_1_1 ]])
	cmds.formLayout( frmLayout, edit=True, 	
		attachControl=[[sel_2_3,"left", 0, sel_2_2 ],[sel_2_3, "top", 0, sel_1_1 ]])
	cmds.formLayout( frmLayout, edit=True, 	
		attachControl=[[sel_2_4,"left", 0, sel_2_3 ],[sel_2_4, "top", 0, sel_1_1 ]])
	cmds.formLayout( frmLayout, edit=True, 	
		attachControl=[[sel_2_5,"left", 0, sel_2_4 ],[sel_2_5, "top", 0, sel_1_1 ]])
	cmds.formLayout( frmLayout, edit=True, 	
		attachControl=[[sel_2_6,"left", 0, sel_2_5 ],[sel_2_6, "top", 0, sel_1_1 ]])
		
	print("Char Selection Created")

	cmds.setParent(curParent)
	
"""

'''
# Test Code

import maya.cmds as cmds
import characterGUI.cri_advGirl_gui as charGUI
reload(charGUI)
charGUI.gui()
filePath = r'C:\Users\mclavan\Documents\My Dropbox\scripts\mecScripts\myDev\characterGUI\images\characterSel_icons'

# Setting up controls
charSel = charGUI.CharSelect_Input(filePath)
charSel.charSel.rows[1][2].height

# Creating character gui
import characterGUI.cri_advGirl_gui as charGUI
cmds.window()
mainCol = cmds.columnLayout()
cmds.rowColumnLayout(nc=3)
cmds.button()
cmds.button()
cmds.button()
cmds.setParent(mainCol)
charSel = charGUI.CharSelectGUI( filePath, mainCol )
leftPath = r'C:\Users\mclavan\Desktop\homerImage\panel1'
charSel2 = charGUI.CharSelectGUI(leftPath, mainCol )


help(charSel2)
charSel2.rows[3][0].height
cmds.showWindow()


'''

		


