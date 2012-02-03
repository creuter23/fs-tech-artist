
import maya.cmds as cmds
import os, os.path
import xml.etree.ElementTree as ET

# root = ET.Element()
# mainTabs = []
# frames = []
myPath = os.path.join(cmds.internalVar(userAppDir=True), "myStuff")
fileN = "modTest2.xml"

def loadDir():
	'''
	Directory structures are broken down into three area.
	- mainFolder is going to be the tab names.
	- framesFolder are directors which will be represented by frameLayouts.
	- files --> the second folder will contain files to be imported.
		xpm image will share the same name and be used to put an icon
		on the button.
		"one.ma" & "one.xpm"
		If no image is included then a default one or nothing will be used.
	'''
	
	root = ET.Element("modImport")
	
	# mainTabs = [f for f in os.listdir(myPath) if os.path.isdir(os.path.join(myPath, f))]	
	for item in os.listdir(myPath):
		tabPath = os.path.join(myPath, item)
		if( os.path.isdir(tabPath)):
			tab = ET.SubElement(root, item)
			# Set attribute path
			tab.attrib["path"] = tabPath
			'''
			elem = Element("tag")
			elem.attrib["first"] = "1"
			elem.attrib["second"] = "2"
			'''
			# Frame Loop
			# Get Frames
			
			for frameItem in os.listdir(tabPath):
				framePath = os.path.join(tab.get("path"),frameItem)
				if( os.path.isdir(tabPath)):
					frame = ET.SubElement(tab, frameItem)
					# Set attribute path
					frame.attrib["path"] = framePath
				

					for fileItem in os.listdir(framePath):
						filePaths = os.path.join(frame.get("path"), fileItem)
						# fullFile = os.path.join(filePath, fileItem)
						if( os.path.isfile(filePaths)):
							# Look for the extension
							# Image goes as a tag under
							fileParts = os.path.splitext(fileItem)
							if( (fileParts[1] == ".ma") or fileParts[1] == ".mb"):
								myFile = ET.SubElement(frame, fileParts[0])
								myFile.attrib["path"] = filePaths
								myFile.text = fileItem
							else:
								
								for frm in frame:
									print( frm.tag )
									print( frm.text )
								'''
								myFile = ET.SubElement(frame, fileParts[0])
								myImage = ET.SubElement(myFile, fileParts[1][1:])
								myImage.text = fileItem
								'''
					# File Loop
	
	tree = ET.ElementTree(root)
	tree.write(os.path.join(cmds.internalVar(userAppDir=True), fileN))
	
	"""
	mainTabs = [f for f in os.listdir(myPath) if os.path.isdir(os.path.join(myPath, f))]
	for tab in mainTabs:
		tempPath = os.path.join(myPath,tab)
		
		frames = [f for f in os.listdir(os.path.join(myPath,tab)) if os.path.isdir(os.path.join(tempPath, f))]
	"""
	
	'''
	os.listdir(myPath+tab)
	for tab in mainTabs:
		if( os.path.isdir(os.path.join(myPath+tab, f)))
	frames = [f for f in os.listdir(myPath) if os.path.isdir(os.path.join(myPath, f))]
	'''
	
# mainTabs isn't alphabetical (EXTRA add on)
	


