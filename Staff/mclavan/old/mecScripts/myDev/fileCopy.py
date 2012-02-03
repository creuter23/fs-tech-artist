import os, os.path
import shutil

def fileCopy( pathA, pathB, myFile ):
	'''
	# Paths will be aquired from the script.
	pathA = r'C:\Documents and Settings\mclavan\Desktop\FolderA'
	pathB = r'C:\Documents and Settings\mclavan\Desktop\FolderB'
	'''
	
	pathFullA = os.path.join( pathA, myFile )
	pathFullB = os.path.join( pathB, myFile )
	
	print("Source Path: %s" %pathFullA )
	print("Target Path: %s" %pathFullB )
	
	# shutil.copyfile( pathFullA, pathB )
	shutil.copyfile( pathFullA, pathFullB )


def multiFileCopy( rootPath, destPath, myType="*.jpg" ):
	# Loop area
	'''
	rootPath = r"C:\Documents and Settings\mclavan\Desktop\FolderA"
	destPath = r"C:\Documents and Settings\mclavan\Desktop\FolderB"
	'''
	
	# what are the files i need.
	# os.listdir( rootPath )
	
	jpgFiles = glob.glob( os.path.join(rootPath, myType) )
	
	for jpgFile in jpgFiles:
		fileCopy( rootPath, destPath, os.path.split(jpgFile)[1] )


def copyFileGui():
	# Get the root path from textField
	destDir = cmds.textField( "textFName1", q=True, text=True )
	# Get the dest path from 
	targDir = cmds.textField( "textFName2", q=True, text=True )
	
	# Call the multiFileCopy
	multiFileCopy( destDir, targDir, "*.pdc" )
	

