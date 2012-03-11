'''
File Sequencer
fileSeq.py

Description:

How To Run:
import fileSeq
fileSeq.gui()

'''

import maya.cmds as cmds
import os, os.path
import shutil

from textScrollList import TextScrollList
from callback import Callback

print("File Sequencer Loaded.")

class FileDirectory:
	def __init__(self, curPath=None):
		self.fileName = None
		self.fileType = None
		cmds.fileBrowserDialog( m=4, fc=self.getItems, ft='image', an='Import_Image', om='Import' )


	def getItems(self, fileName, fileType):
		# (u'/Users/michaelclavan/Documents/', u'directory')
		# print(fileName, fileType)
		self.fileName = fileName
		self.fileType = fileType
		
	def getPath(self):
		return self.fileName
		
	def getType(self):
		return self.fileType

win = "mecSeqWin"
def gui():
	'''
	Generates the interface for the file sequencer.
	'''
	if( cmds.window(win, ex=True) ):
		cmds.deleteUI(win)
	if( cmds.windowPref(win, ex=True) ):
		cmds.windowPref(win, r=True)
		
	cmds.window(win, h=500, w=400)
	mainCol = cmds.columnLayout()
	
	cmds.rowColumnLayout(nc=2, cw=[[1,200],[2,200]])
	global targField, destField, tslTarget, tslDestin
	
	targField = cmds.scrollField( w=200, h=50, editable=False, wordWrap=True, text='Non editable with word wrap' )
	destField = cmds.scrollField( w=200, h=50, editable=False, wordWrap=True, text='Non editable with word wrap' )
	cmds.button(label="Load Target", c=Callback(getTarget))
	cmds.button(label="Load Destination", c=Callback(getDestin))
	
	cmds.text(label = "Target Files")
	cmds.text(label = "Destination Files")
	
	tslTarget = TextScrollList(200, 200)

	tslDestin = TextScrollList(200, 200)
	cmds.setParent(mainCol)
	
	# Inputs
	fieldsGUI(mainCol)
	
	cmds.showWindow(win)
	
	print("Interface executed.")

def getTarget():
	testDir = FileDirectory()
	filePath = testDir.getPath()
	cmds.scrollField(targField, e=1, text=filePath)
	files = os.listdir(filePath)
	tslTarget.appendAll( files )
	
	
def getDestin():	
	testDir = FileDirectory()
	cmds.scrollField(destField, e=1, text=testDir.getPath())
	destinPath = cmds.scrollField( destField, q=True, text=True)			
	destFiles = os.listdir(destinPath)
	tslDestin.remAllItems()
	tslDestin.appendAll(destFiles)
	
def pathGUI(curParent):
	frm = cmds.formLayout( parent=curParent)
	
	return frm

def tslGUI(curParent):
	frm = cmds.formLayout( parent=curParent)
	
	return frm

def fieldsGUI(curParent):
	frm = cmds.formLayout( parent=curParent)
	# Row 1 labels
	txt1 = cmds.text(label="fileName", w=200)
	txt2 = cmds.text(label="##", w=60)
	txt3 = cmds.text(label="Pad", w=40)
	
	# Row 2 Fields
	global mainName, counter, pad, copyChk
	mainName = cmds.textField( w=200 )
	counter = cmds.intField( w=60, v=1 )
	pad = cmds.intField( w=40, v=3 )
	
	# Row 3 Buttons
	btn1 = cmds.button(label="Next", w=200, c=Callback(process))
	# copyChk = cmds.checkBox( label="move", v=1, 
	
	# Positioning GUI elements
	cmds.formLayout(frm, e=1, af=[])
	cmds.formLayout(frm, e=1, ac=[])
	
	# Row1
	cmds.formLayout(frm, e=1, af=[[txt1, "left", 0],[txt1, "top", 0]])
	cmds.formLayout(frm, e=1, af=[txt2, "top", 0], ac=[txt2, "left", 0, txt1])
	cmds.formLayout(frm, e=1, af=[txt3, "top", 0], ac=[txt3, "left", 0, txt2])
	
	# Row 2
	cmds.formLayout(frm, e=1, af=[mainName, "left", 0],ac=[mainName, "top", 0, txt1])
	cmds.formLayout(frm, e=1, ac=[[counter, "left", 0, mainName],[counter, "top", 0, txt1]])
	cmds.formLayout(frm, e=1, ac=[[pad, "left", 0, counter],[pad, "top", 0, txt1]])
		
	# Row 3
	cmds.formLayout(frm, e=1, af=[btn1, "left", 0],ac=[btn1, "top", 0, mainName])
	
	return frm

def process():
	print("Processing")
	# Get the items from the target tsl.
	fileNames = tslTarget.getSelItems()
	startNum = cmds.intField( counter, q=True, value=True )
	newName = cmds.textField( mainName, q=True, text=True )
	padVal = cmds.intField( pad, q=True, value=True)
	
	targetPath = cmds.scrollField( targField, q=True, text=True)
	destinPath = cmds.scrollField( destField, q=True, text=True)
	
	# Loop through one by one copying it over then renaming it.
	# newNames = []
	# "%s.%s.%s" %(newName, "%04d", "iff")
	for i in range(len(fileNames)):
		tempName = eval('"%s.%0' + str(padVal) + 'd.%s" %(newName, startNum, "iff")')
		# tempName = "%s.%03d.iff" %(newName, startNum)
		# print("Test: " + tempName)
		# Copy over
		fullTarget = os.path.join( targetPath, fileNames[i] )
		fullDestin = os.path.join( destinPath, fileNames[i] )
		# Renaming
		# fullDestin = os.path.join( destinPath, fileNames[i] )

		if( os.path.isfile( fullTarget ) ):
			shutil.copy( fullTarget, fullDestin )
			# Rename
			tempPath = os.path.join( destinPath, fileNames[i] )
			newPath = os.path.join( destinPath, tempName )
			if( os.path.exists( tempPath ) ):
				os.rename(tempPath, newPath)
				# add to the list.
				# tslDestin.appendAll(tempName)
				# print( newName )
				startNum += 1

	destFiles = os.listdir(destinPath)
	tslDestin.remAllItems()
	tslDestin.appendAll(destFiles)
	
	# Research question???
	# Does copying the file or getting the listdir on the file,
	#   return a string or an instance to a file name?
	
	cmds.intField( counter, e=1, value=startNum) 
	# destField	
	   
