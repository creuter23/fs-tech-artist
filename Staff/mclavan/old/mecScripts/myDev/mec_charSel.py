'''
mec_charSel.py

How to Run:

import mec_charSel
mec_charSel.gui()


'''
# Working with classes.


# Lets build a auto character selection.

# This script will auto load based on a folder and its name.

# iconName_row_col_type.ext
# ironMan_01_01_img.xpm
# ironMan_03_02_ctrl.xpm
# Checkbox options. 
# ironMan_03_03_togOn.xmp ironMan_03_03_togOff.xmp
# ironMan_03_03_tog_On.xmp ironMan_03_03_tog_Off.xmp
# Extension would work even if they are bmp.

import os, os.path
import glob
# from mecMaya.callback import Callback
from mecMaya import callback
import maya.cmds as cmds

class CharSel(object):
	def __init__( self, path, name, parent, iconType="xpm" ):
		self.path = path
		self.parent = parent
		self.controls = []
		self.icons = []
		# need a loader function.
		self.getFiles(name, iconType)
		self.createControls()

	def selectControl( self, control ):
		print( "%s has been pressed." %control )
		
	def createControls(self):
		# name and type ['control Name', 'type']

		# loop for each icon
		# I need to use call back here.
		# self.mainLayout = cmds.columnLayout( parent=self.parent )
		
		leftElement = ""
		topElement = ""
		
		self.mainLayout = cmds.formLayout( parent=self.parent )
		for i, icon in enumerate(self.icons):
			fullPath = os.path.join( self.path, icon )
			iconParts = os.path.splitext(icon)[0].split("_")
			# example ironMan_01_01_img.xpm
			# ["ironMan", "01", "01", "img"]
			'''
			controlName = cmds.picture( image=fullPath, parent=self.mainLayout )
			'''
			controlName = cmds.symbolButton( image=fullPath, parent=self.mainLayout,
				c=callback.Callback( self.selectControl, icon ))
			
		
			# Column Placement
			if( int(iconParts[2]) == 1 ):
				# Attach to form top
				# Form placement
				cmds.formLayout( self.mainLayout, edit=True, af=[controlName, "left", 0])
				leftElement = controlName
				
				# Check to see if we are NOT in the first row.
				if(int(iconParts[1]) != 1):
					topElement = self.control[-1]
				print("%s is in the first column." %icon)					
	
			else:
				cmds.formLayout( self.mainLayout, edit=True, ac=[controlName, leftElement, "left", 0)
				leftElement = controlName
				print("%s is in column #%s" %(icon, topElement))
				
			# Row Placement
			if( int(iconParts[1]) == 1 ):
				cmds.formLayout( self.mainLayout, edit=True, af=[controlName, "top", 0])
				print("%s is in the first row." %icon)
				# Attach to form top
			else:
				# Attach to the form element above.
				cmds.formLayout( self.mainLayout, edit=True, ac=[controlName, topElement, "top", 0)
				print("%s is under %s." %(icon, topElement)
				
			self.controls.append( controlName )
		
		# Form Layout seems like  better choice for dyanamic generation of elements.
		# 1st place all the element into the layout
		# 2nd move them into position.
		# Is it at the top (first row)?
		# Is it the first column (all the way to the left)?
		# What am I going to connect these situation to.  
			# I guess attach it to the form.
		# How many rows?
		
		# How many columns?
		
		
			
			
		print(self.controls)
# I will have to get the width and height of the icon to do this correctly.

		
		
		
	def getFiles(self, name, icon='xpm'):
		
		# Load all the files from the given directory.
		
		# Check to see if the directory exists.
		files = os.listdir( self.path )
		
		# Returns all the files in the directory.
		# files = glob.glob( os.path.join( self.path, "*.%s" %icon ) )
		# print( os.path.join( self.path, "*.%s" %icon ) )
		print(files)
		
		# seperating the file types
		for item in files:
			if( icon in item ):
# print( "Is %s inside of %s" %(name, item) )
				if( name in item ):
					self.icons.append(item)
				
		print( self.icons )
		
	
class FormGrid(object):
	'''
	Easier manipulation of the form layout.
	'''
	def __init__(self, parent):
		self.layoutName = cmds.formLayout( parent=parent )
		self.formElements = []
		self.parent = parent
	def createElements( fileName ):
		iconType = fileName.split()[-1]
		items = fileName.split("_")
		newElement = FormGridElement( self.parent, iconName, path )
	
		
class Element(object):
	'''
	
	'''
	def __init__(self, parent, iconName, path):
		pieces = iconName.split()[-1]
		self.name = pieces[0]
		self.row = pieces[1]
		self.column = pieces[2]	
		self.controlType = pieces[3]
		self.iconType = pieces[4]
		self.iconName = iconName
		self.path = path
		self.parent = parent
		# self.element
		self.initDimensions()
		
		self.topElement = ""
		self.leftElement = ""
		self.createControl()
		
	# Create control
	def createControl(self):
		filePath = os.path.join( self.path, self.iconName ) 
		if( self.controlType == "img" ):
			# Creating an picture
			if( self.controlType == "xpm"):
				self.element = cmds.picture( image=filePath )
			else:
				self.element = cmds.image( image=filePath )
		elif( self.controlType == "ctrl" ):
			# Creating a symbol button
			self.element = cmds.symbolButton( image=filePath )
		
			
	def setCommand(self, script):
		if( self.controlType == "ctrl" ):
			cmds.symbolButton(self.element, edit=True, command=script)
	
	def getAllInfo(self):
		return {self.iconName : [self.name, self.row, self.column, self.controlType, self.iconType, self.path, self.element]}
	
		def getTopElement(self):
		return self.topElement
	def getLeftElement(self):
		return self.leftElement
			
	def setTopElement(self, control=""):
		self.topElement = control
	def setLeftElement(self, control=""):
		self.leftElement = control
	
	def initDimensions(self):
		# Creating a temp window.
		# This window will never be shown.
		filePath = os.path.join( self.path, self.iconName )
		win = cmds.window()
		cmds.columnLayout()
		if( self.iconType == "xpm" ):
			# Create a picture
			pic = cmds.picture( i=filePath )
			self.width = cmds.picture( pic, q=True, w=True)
			self.height = cmds.picture( pic, q=True, h=True)
		else:
			# Create a image
			pic = cmds.image( i=filePath )
			self.width = cmds.image( pic, q=True, w=True)
			self.height = cmds.image( pic, q=True, h=True)		
	
		cmds.deleteUI(win)
		
'''		
There isn't a really good way in maya to get a icon or picture image size.
So, a work around is using the picture gui component.  Symbol button 
puts a border around the icon but picture doesn't.  
So, the picture's width and height would be correct.

string $path = "C:\\Users\\mclavan\\Documents\\maya\\2009-x64\\prefs\\icons\\";
string $file = "cometAttrEditor.bmp";
$file = "Chann.xpm";
           if(`window -exists mecGetDimensions`)
		deleteUI mecGetDimensions;
            if( `windowPref -exists mecGetDimensions` )
            		windowPref -r mecGetDimensions;

            window -w 300 -h 300 -t "PictureDimensions" 
            		-titleBar 1 -mnb 1 -mxb 1 -mb 1
            		-tlb 0 -sizeable 1 mecGetDimensions;
            
            columnLayout;
            picture -i ($path+$file) mecGetDimensionsPic;
print($path+$file+"\n");
string $width = `picture -q -w mecGetDimensionsPic`;
string $height = `picture -q -h mecGetDimensionsPic`;

print( "Width: " + $width + "  Height: " + $height );
deleteUI mecGetDimensions;
		



	# Assign Position
	def posControl(self):	
		cmds.formLayout( self.parent, 
'''		
'''		
# Column Placement
if( int(iconParts[2]) == 1 ):
	# Attach to form top
	# Form placement
	cmds.formLayout( self.mainLayout, edit=True, af=[controlName, "left", 0])
	leftElement = controlName
	
	# Check to see if we are NOT in the first row.
	if(int(iconParts[1]) != 1):
		topElement = self.control[-1]
	print("%s is in the first column." %icon)					

else:
	cmds.formLayout( self.mainLayout, edit=True, ac=[controlName, leftElement, "left", 0)
	leftElement = controlName
	print("%s is in column #%s" %(icon, topElement))
	
# Row Placement
if( int(iconParts[1]) == 1 ):
	cmds.formLayout( self.mainLayout, edit=True, af=[controlName, "top", 0])
	print("%s is in the first row." %icon)
	# Attach to form top
else:
	# Attach to the form element above.
	cmds.formLayout( self.mainLayout, edit=True, ac=[controlName, topElement, "top", 0)
	print("%s is under %s." %(icon, topElement)
'''
