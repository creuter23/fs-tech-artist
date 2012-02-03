'''
mecCommand.py
'''

import maya.OpenMaya as om
import maya.OpenMayaMPx as OpenMayaMPx
import sys

'''
# Creating a command!
# 1) initializePlugin(mobject) 
# 2) uninitializePlugin(mobject)
# 3) cmdsCreator
# 4) command class (Truly custom!)
'''
# initializePlugin(mobject)
# uninitializePlugin(mobject)
# nodeCreator()
# nodeInitializer()
# class for creating the node

kMyCommandName = "mecMyPlugin"

# class mecCommand( OpenMayaMPx.MPxCommand ):
class scriptedCommand( OpenMayaMPx.MPxCommand ):
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self)
	def doIt(self,argList):
		om.MGlobal.displayWarning("My Plugin command has been executed.")		

		
def cmdCreator():
	return OpenMayaMPx.asMPxPtr( scriptedCommand() )  # Gives Maya control

'''
def nodeCreator():
	return OpenMayaMPx.asMPxPtr( mecCommand() )  # Gives Maya control
'''

	
# def nodeInitializer():
	
	

def initializePlugin(mobject):
	'''
	registerCommand is the only thing that will change here.
	'''
	mplugin = OpenMayaMPx.MFnPlugin(mobject) #done before tyring to register the command.
	try:
		# registerCommand requires( commandName, creatorFunction
		# commandName normally is something like kPluginNodeTypeName
		# mplugin.registerCommmand( kMyCommandName, nodeCreator, nodeInitializer )
		mplugin.registerCommand( kMyCommandName, cmdCreator)
	except:
		sys.stderr.write( "Failed to register command: %s\n" %kMyCommandName )
		raise
		
def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterCommand( kMyCommandName )
	except:
		sys.stderr.write( "Failed to unregister command: %s\n" %kMyCommandName)
		raise
		
