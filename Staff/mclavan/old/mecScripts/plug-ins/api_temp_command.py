'''
Maya Scripted Plug-in - Command Template
api_temp_command.py


'''


import maya.OpenMaya as om
import maya.OpenMayaMPx as OpenMayaMPx
import sys

# Command Name
kMyCommandName = "mecCheckCommand"

# Flag names
kMyFlag = "-mf"
kMyLongFlag = "-myFlag"

# example Line
# mecCheckCommand -mf 3.0
# cmds.mecCheckCommand( mf=3.0 )

'''
# Creating a command!
# 1) initializePlugin(mobject) 
# 2) uninitializePlugin(mobject)
# 3) cmdsCreator
# 4) syntaxCreator
# 5) command class (Truly custom!)
'''


# scripted Command class (The work horse)
class scriptedCommand( OpenMayaMPx.MPxCommand):
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self)
	def doIt(self, args):
		'''
		The doIt function is required for creating a command.
		'''
		om.MGlobal.displayWarning("You code goes here")
		self.flagVal = 0
		
		# Parse the arguments.
		argData = om.MArgDatabase(self.syntax(), args)  # Gets the argument data
		if argData.isFlagSet(kMyFlag):  # Replace kFlagName
			self.flagVal = argData.flagArgumentDouble(kMyFlag, 0)  # Replace kFlagName leave 0 for each flag.
			# flagVal will now include the value from the argument
		
		print(self.flagVal)
		''''''
		'''
		# Example
		if argData.isFlagSet(kPitchFlag):
			pitch = argData.flagArgumentDouble(kPitchFlag, 0)
		'''			
			
		'''
		# The above example will only work for float, what about the other types.
		flagVal = argData.flagArgumentDouble(kFlagName, 0)
		flagVal = argData.flagArgumentInt(kFlagName, 0)
		flagVal = argData.flagArgumentString(kFlagName, 0)
		flagVal = argData.flagArgumentBool(kFlagName, 0)
		# Apart of the MArgDatabase class there are also MDistance, MAngle, and MTime 
		'''
		

		
def cmdCreator():
	return OpenMayaMPx.asMPxPtr( scriptedCommand() )  # Gives Maya control
	
def syntaxCreator():
	'''
	Connects the flags
	'''
	syntax = om.MSyntax()
	# Add flags to the commands here.
	syntax.addFlag(kMyFlag, kMyLongFlag, om.MSyntax.kDouble)
	return syntax

def initializePlugin(mobject):
	'''
	registerCommand is the only thing that will change here.
	'''
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.registerCommand( kMyCommandName, cmdCreator, syntaxCreator) # Command Name and cmdCreator Function
	except:
		sys.stderr.write( "Failed to register command: %s\n" %kMyCommandName )
		raise
		
def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject, "mecTools", "1.1", "Any")
	try:
		mplugin.deregisterCommand( kMyCommandName )
	except:
		sys.stderr.write( "Failed to unregister command: %s\n" %kMyCommandName)
		raise
