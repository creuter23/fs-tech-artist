# import hashTest
import maya.cmds as cmds

class HashTest(object):
	
	
	def __init__(self, startObj):
		self.startObj = startObj	
		self.nodes = []
		self.info = {}
		self.slide( startObj )
		
		# Reversing the order of the list
		self.nodes.reverse()
	
	def printInfo(self):
		# print out all the items of the list in order
		for i,node in enumerate(self.nodes):
			print("-"*60)
			print("Item: %s NodeName: %s" %(i, node))
			self.info[node].printInfo()
			print("-"*60)
	'''	
	def __str__(self):		
		self.printInfo()
	'''
	
	def slide(self, objects):
		self.nodes.append(objects)
		if( Node.confirmType(objects) == 0 ): # Transform
			self.info[objects] = Transform(objects)
		elif( Node.confirmType(objects) == 1): # Group
			self.info[objects] = Group(objects)			
		else:	# Shape
			self.info[objects] = Shape(objects)

		# newObjects = cmds.listRelatives(objects, c=1, type="transform" )
		newObjects = cmds.listRelatives(objects, c=1 )

		if( not newObjects ):
			return objects

		if( newObjects ):
			for obj in newObjects:
				self.slide(obj)

class Node(object):
	def __init__(self, nodeName):
		self.nodeName = nodeName
		self.nameLen = len( nodeName )
		self.nodeType = Node.confirmType(self.nodeName)
	
	def printInfo(self):
		print( "NodeName: %s NameLength: %s NodeType: %s" %(self.nodeName, self.nameLen, self.nodeType) )

	
	@staticmethod
	def confirmType(nodeName):
		'''
		Determines which type of node it is transform, group, or shape.
		'''
		curType = cmds.objectType( nodeName )
		nodeId = 000
		if( curType == "mesh"):
			nodeId = 002 #"shape"
		elif( curType == "transform" ):  
			#and it doesn't have a shape node
			nodeId = 001 #"group"
			children = cmds.listRelatives(nodeName, c=True )
			shapeChild = False
			for child in children:
				if( cmds.objectType(child, isType="mesh") ):
					shapeChild = True
			
			if( shapeChild ):  
				#transform has a shape node
				nodeId = 000 #Transform	
			
		return nodeId

				
class Shape(Node):
	# It will be a leaf.  
	def __init__(self, nodeName):
		Node.__init__(self, nodeName)

	
class Transform(Node):
	# Its has a shape node acompaning it
	def __init__(self, nodeName):
		Node.__init__(self, nodeName)
		self.children = cmds.listRelatives( self.nodeName, c=True )
		self.numChildren = len( self.children )

	def printInfo(self):
		# Node.printInfo()
		print( "NodeName: %s NameLength: %s NodeType: %s" %(self.nodeName, self.nameLen, self.nodeType) )
		print( "NumOfChildren: %s Children: %s" %(self.numChildren, ", ".join(self.children)) )

		
class Group(Node):
	# If its a leaf and not a shape node then its a group
	def __init__(self, nodeName):
		Node.__init__(self, nodeName)
		self.children = cmds.listRelatives( self.nodeName, c=True )
		self.numChildren = len( self.children )

	def printInfo(self):
		# Node.printInfo()
		print( "Node Name: %s Name Length: %s Node Type: %s" %(self.nodeName, self.nameLen, self.nodeType) )
		print( "NumOfChildren: %s Children: %s" %(self.numChildren, ", ".join(self.children)) )


'''
How to use:

import hashTest
reload( hashTest)

# Create a tabel based on the first selected object. 
results = hashTest.HashTest(cmds.ls(sl=1)[0])

# Node base class has the main guts.
# There exists a static method to confirm if the node is a transform, group, or a shape
hashTest.Node.confirmType('a')

# nodes is a public member of the HashTest class, containing the names and order of the dataStructure.
results.nodes

# Each class will print its info out.
results.printInfo()


# info dictionary contains all the vita information for the node i.e its type, name, name length, etc...
# the __dict__ will show you all data contained in the instance.
results.info['group1'].__dict__

'''
