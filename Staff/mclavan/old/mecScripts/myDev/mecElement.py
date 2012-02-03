# mecElement.py

import os, os.path
import glob
# from mecMaya.callback import Callback
from mecMaya import callback
import maya.cmds as cmds


class Element(object):
	'''
	
	'''
	def __init__(self, parent, iconName, path):
		filePieces = iconName.split(".")
		# print(filePieces)
		pieces = filePieces[0].split("_")
		self.name = pieces[0]
		self.row = pieces[1]
		self.column = pieces[2]	
		self.controlType = pieces[3]
		self.iconType = filePieces[1]
		self.iconName = iconName
		self.path = path
		self.parent = parent
		# self.element
		
		
		self.topElement = ""
		self.leftElement = ""
		self.createControl()
		self.initDimensions()
	# Create control
	def createControl(self):
		filePath = os.path.join( self.path, self.iconName ) 
		print(filePath)
		if( self.controlType == "img" ):
			# Creating an picture
			if( self.controlType == "xpm"):
				self.element = cmds.picture( image=filePath, p=self.parent )
			else:
				self.element = cmds.image( image=filePath, p=self.parent )
		elif( self.controlType == "ctrl" ):
			# Creating a symbol button
			self.element = cmds.symbolButton( image=filePath, p=self.parent )
		
			
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
		print( "Icon Width: %s, Height: %s" %(self.width, self.height))
		cmds.deleteUI(win)
