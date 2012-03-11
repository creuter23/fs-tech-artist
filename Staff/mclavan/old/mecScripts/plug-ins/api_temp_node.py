'''
Maya Scripted Plug-in - Node Template
api_temp_node.py


'''


import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import sys

# Command Name
kMyNodeName = "mecCheckNode"

# node id 
myNodeID = OpenMaya.MTypeId(0x00333) # What is the range of node ID
# Range can be between 0 - 0x7FFFF


# example Line
# mecCheckCommand -mf 3.0
# cmds.mecCheckCommand( mf=3.0 )

'''
# Creating a command!
# 1) initializePlugin(mobject) 
# 2) uninitializePlugin(mobject)
# 3) nodeCreator
# 4) nodeInitizer
# 5) node class (Truly custom!)
'''


# scripted Command class (The work horse)
class scriptedNode( OpenMayaMPx.MPxNode):
	# Class Variables - input and output are just my examples
	input = OpenMaya.MObject()
	output = OpenMaya.MObject()
	
	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)
	def compute(self, plug, dataBlock):
		'''
		The compute function is required for creating a command.
		'''
		
		# Computing the output values from what is being inputted
		
		if( plug == scriptedNode.output ):
			# Data Handle to get values from the attribute
			dataHandle = dataBlock.inputValue( scriptedNode.input )
			# Convert data into proper type.
			inputFloat = dataHandle.asFloat()
			
			# DO SOMETHING WITH THE DATA
			result = inputFloat * 3   
			print("myNode Results: %s" %result)
			
			# Data Handle for the output value
			outputHandle = dataBlock.outputValue( scriptedNode.output )
			outputHandle.setFloat(result)
			dataBlock.setClean(plug)
			
			# ?? is outputValue and inputValue named that because 
			# 	of the names I gave the attributes or something else?
			

		
def nodeCreator():
	return OpenMayaMPx.asMPxPtr( scriptedNode() )  # Gives Maya control
	
def nodeInitizer():
	'''
	Creates the attributes and sets them up.
	'''
	# Numeric Attribute
	# Attribute #1
	nAttr = OpenMaya.MFnNumericAttribute()
	scriptedNode.input = nAttr.create( "input", "in", OpenMaya.MFnNumericData.kFloat, 0.0) # 0.0 is default value.
	# attribute properties (readable, writeable, storable, keyable, etc...)
	nAttr.setStorable(1)	

	# Attribute #2	
	nAttr = OpenMaya.MFnNumericAttribute()
	scriptedNode.output = nAttr.create( "output", "out", OpenMaya.MFnNumericData.kFloat, 0.0) # 0.0 is default value.
	# attribute properties (readable, writeable, storable, keyable, etc...)
	nAttr.setStorable(1)		
	nAttr.setWritable(1)		
	
	# Adding attributes to the node
	scriptedNode.addAttribute( scriptedNode.input )
	scriptedNode.addAttribute( scriptedNode.output )
	
	# Piping data through the node
	scriptedNode.attributeAffects(scriptedNode.input, scriptedNode.output)
	
	

def initializePlugin(mobject):
	'''
	registerCommand is the only thing that will change here.
	'''
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.registerNode( kMyNodeName, myNodeID, nodeCreator, nodeInitizer) 
	except:
		sys.stderr.write( "Failed to register node: %s\n" %kMyCommandName )
		raise
		
def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( myNodeID )
	except:
		sys.stderr.write( "Failed to unregister node: %s\n" %kMyCommandName)
		raise
