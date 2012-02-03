'''
API Plug in creation
info_apiPlugIn.py


Description:
	- These nodes go through how to create a python plug-in in Maya.


How To Run:
	
import info_apiPlugIn
reload( info_apiPlugIn )

'''

import maya.cmds as cmds
import maya.OpenMaya as om


'''
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import sys
'''


def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		# kPluginCmdName is meant to be a pointer but in python 
		# 	it's just a string name of the command.
		mplugin.registerCommand( kPluginCmdName, cmdCreator )
	except:
		sys.stderr.write( "Failed to register command: %s\n" %
		kPluginCmdName )
	raise
	
	
def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		# kPluginCmdName is meant to be a pointer but in python 
		# 	it's just a string name of the command.
		mplugin.deregisterCommand( kPluginCmdName )
	except:
		sys.stderr.write( "Failed to unregister command: %s\n"
			% kPluginCmdName )
	raise	

	
class scriptedCommand(OpenMayaMPx.MPxCommand):
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self)
	def doIt(self,argList):
		print "Hello World!"

# What is this doing?
# Seem that this is the starter.
'''
It is very important to call the OpenMayaMPx.asMPxPtr() on the newly created proxy object. This
call transfers ownership of the object from Python to Maya. Program errors will occur if you do
not make this call since Python can unreference this object and destroy it. This will leave a
dangling pointer in Maya.
'''
def cmdCreator():
	return OpenMayaMPx.asMPxPtr( scriptedCommand() )
	
	
# What runs everything?


