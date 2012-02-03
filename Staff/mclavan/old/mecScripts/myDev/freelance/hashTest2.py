'''
# import hashTest


How to run:

from freelance import hashTest
reload(hashTest)
order = hashTest.HashTest(cmds.ls(sl=1)[0])
order.printInfo()
order.printAll()

'''
import maya.cmds as cmds
import maya.mel as mel

mel.eval( 'python("import sys")' )


class Callback():
	_callData = None
	def __init__(self,func,*args,**kwargs):
		self.func = func
		self.args = args
		self.kwargs = kwargs
	
	def __call__(self, *args):
		Callback._callData = (self.func, self.args, self.kwargs)
		mel.eval('global proc py_%s(){python("sys.modules[\'%s\'].Callback._doCall()");}'%(self.func.__name__, __name__))
		try:
			mel.eval('py_%s()'%self.func.__name__)
		except RuntimeError:
			pass
		
		if isinstance(Callback._callData, Exception):
			raise Callback._callData
		return Callback._callData 
	
	@staticmethod
	def _doCall():
		(func, args, kwargs) = Callback._callData
		Callback._callData = func(*args, **kwargs)
		
		
class Vertex( object ):
	def __init__( self, vertex ):
		'''
		object.vtx[0]
		'''
		# entire name of the vector object.vtx[0]
		self.name = vertex
		self.idNum = Vertex.getIDNum( vertex )
		self.pos = Vertex.getVtxPos( vertex )
		self.uvs = Vertex.getAllUVsCoords( vertex ) 
		self.uvMaps = Vertex.getUVSets( vertex ) 
		self.normals = Vertex.getFaceNormals( vertex )
		# self.vtxFace, self.normals = Vertex.getFaceNormals( vertex )
		# Do I need to record a three normals?
	
	def printInfo(self):
		strNums = lambda x: [ str(num) for num in x ]
		
		line = "%s Vertex: %s ID: %s %s\n" %("-"*20, self.name, self.idNum, "-"*20)
		line += "Pos: %s\n" %", ".join(strNums(self.pos))
		line += "Normals: FacesVertex: %s\n" %(len(self.normals))
		'''
		for i, normal in enumerate(self.vtxFace):
			line += "FaceVertex: %s Normals: %s\n" %(normal, ", ".join(strNums(self.normals[i])))
		
		'''
		for key, normal in self.normals.items():
			line += "FaceVertex: %s Normals: %s\n" %(key, ", ".join(strNums(normal)))

		line += "NumUVsMaps: %s UVMaps: %s\n" %(len(self.uvs),", ".join(self.uvMaps))
		for i, uv in enumerate(self.uvs):
			line += "UVmap: %s UVs: %s\n%s\n" %(self.uvMaps[i], len(uv)/2 , ", ".join(strNums(uv)))
		print(line)
		
	@staticmethod
	def getFaceNormals( vertex ):
		# vertex normal name
		fvtx = cmds.polyListComponentConversion( vertex, fv=True, tvf=True )
		allFvtx = cmds.filterExpand( fvtx, expand=True, sm=70 )	
		
		# Face index
		vtxFaces = Vertex.getFaceVertexIndex(allFvtx)
		
		tempNormals = {}
		for i, curFvtx in enumerate(allFvtx):
			normalCoords = cmds.polyNormalPerVertex( curFvtx, q=True, xyz=True )
			curFace = vtxFaces[i]
			tempNormals[curFace] = normalCoords
		return tempNormals
		'''
		normals = []
		for i, curFvtx in enumerate(allFvtx):
			normalCoords = cmds.polyNormalPerVertex( curFvtx, q=True, xyz=True )
			curFace = vtxFaces[i]
			normals.append( normalCoords )		
		return vtxFaces, normals
		'''
		
	@staticmethod
	def getFaceVertexIndex(faceVtxs ):
		faces = []		
		for faceVtx in faceVtxs:
			pieces = faceVtx.split('[')
			face = int(pieces[-1][:-1])
			faces.append(face)
		return faces
		
	def getNormalCoords(self, faceID ):
		return self.normals[faceID]
		
	@staticmethod
	def getUVSets( vertex ):
		return cmds.polyUVSet(vertex, query=True, allUVSets=True)
		
	@staticmethod
	def getAllUVsCoords( vertex ):
		
		uvSets = Vertex.getUVSets(vertex)
		currUVSet = cmds.polyUVSet( vertex, q=True, currentUVSet=True )[0]

		totalUVs = []
		for uvSet in uvSets:
			# Set uv to this current uvSet. 
			cmds.polyUVSet( vertex, currentUVSet=True, uvSet=uvSet ) 			
			
			# getting a list of the coords
			uvCoords = Vertex.getCurrentCoords( vertex )
			totalUVs.append(uvCoords)
		
		# Returns the current set back to its orginal
		cmds.polyUVSet( vertex, currentUVSet=True, uvSet=currUVSet)	
		
		return totalUVs
		
	
	@staticmethod
	def getCurrentCoords( vertex ):
		uv = cmds.polyListComponentConversion( vertex, fv=True, tuv=True )
		uvAll = cmds.filterExpand( uv, expand=True, sm=35 )
		uvCoords = cmds.polyEditUV( uvAll , q=True )		
		return uvCoords
		
	@staticmethod
	def getCurrentUVMaps( vertex ):
		uv = cmds.polyListComponentConversion( vertex, fv=True, tuv=True )
		uvAll = cmds.filterExpand( uv, expand=True, sm=35 )
		
		return uvAll
		
	@staticmethod
	def getIDNum( vertex ):
		'''
		Get the id number out of the vertex string.
		Will take anything with the naming convention 'obj.vtx[0]'
		This method argument can be a list of vertex.
		
		returns a vertex id(int) or a list of vertex id(int) numbers.
		'''
		
		if(type(vertex) is list):
			idNums = []
			for vert in vertex:
				pieces = vert.split( "[" )
				idNum = pieces[-1][:-1]
				idNums.append(int(idNum))
			return idNums
				
		else:
			pieces = vertex.split( "[" )  # ['obj.vtx', '0]']
			idNum = pieces[-1][:-1]
			return int(idNum)

	# Couple of static member classes could be handy here.
	@staticmethod 
	def getVtxPos( vertex ):
		'''
		Given the obj.vtx[0] it will return the vertex current postion 
		'''		
		return cmds.pointPosition( vertex, w=True )
	
'''
from freelance import hashTest
reload(hashTest)

selectedVtx = cmds.ls(sl=True)
totalVtx = cmds.filterExpand( selectedVtx, expand=True, sm=31 )
for vtx in totalVtx:
	tempVtx = hashTest.Vertex(vtx)
	tempVtx.printOut()


tempVtx1 = hashTest.Vertex('pCube2.vtx[0]')
tempVtx2.normals
tempVtx1.printOut()
tempVtx2 = hashTest.Vertex('pCube1.vtx[1]')
tempVtx2.printOut()
'''


		
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
			# print("Item: %s NodeName: %s" %(i, node))
			self.info[node].printInfo()
			print("-"*60)
			
	def printAll(self):
		# print out all the items of the list in order
		for i,node in enumerate(self.nodes):
			print("-"*60)
			# print("Item: %s NodeName: %s" %(i, node))
			self.info[node].printAll()
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
		'''
		Inherited from Node class
		self.nodeName 
		self.nameLen
		self.nodeType 	
		'''
		Node.__init__(self, nodeName)
		self.faces = Shape.getFaces(nodeName)
		self.numFaces = len(self.faces)
		self.windingOrder = Shape.getWindingOrder(self.nodeName)
		self.pos = Shape.getPositions(self.nodeName)
		# self.normals
		# self.sets
		# self.uvs
		# self.material

	

	@staticmethod
	def getPositions( shape ):
		'''
		Starting from index 0.  This function will return the positions of each vertex.
		'''
		# Getting all the vertex in the system.
		verts = cmds.polyListComponentConversion( shape, tv=1 )
		allVerts = cmds.filterExpand( verts, expand=True, sm=31 )
		
		positions = [ Vertex.getVtxPos(vert) for vert in allVerts ]
		return positions

	@staticmethod
	def getWindingOrder( shape ):
		
		# I need to get each face seperate
		# Lets go face zero up.
		faces = cmds.polyListComponentConversion( shape, tf=1 )
		allFaces = Shape.getFaces(shape)

		fullWindingOrder = []
		for face in allFaces:
			windingOrder = PolyFace.findWindingOrder(face)
			windingID =  Vertex.getIDNum(windingOrder)
			fullWindingOrder.extend( windingID )
			# print("Face: %s Order: %s" %(face, Vertex.getIDNum(windingOrder)))
		
		return fullWindingOrder
		
	@staticmethod
	def getFaces( shape ):
		faces = cmds.polyListComponentConversion( shape, tf=1 )
		allFaces = cmds.filterExpand( faces, expand=True, sm=34 )
		return allFaces	
	
	def printFull(self):
		# Lenght name type
		# winding order
		# position
		# normal
		# uv
		# texture & material		
		strNums = lambda x: [ str(num) for num in x ]		
		line = "%s nameLength: %s nodeName: %s nodeType: %s %s\n" %("-"*20, self.nameLen, self.nodeName, self.nodeType, "-"*20)
		line += "WindingOrder: %s\n" %" ".join( strNums(self.windingOrder))
		line += "Pos: "
		for pos in self.pos:
			line += " ".join( strNums(pos)) + " "
		print(line + "\n")
	
	def printInfo(self):
		# Lenght name type
		# winding order
		# position
		# normal
		# uv
		# texture & material
		strNums = lambda x: [ str(num) for num in x ]
		line = "%s %s %s %s\n" %(self.nameLen, self.nodeName, self.nodeType, self.numFaces)
		line += " ".join( strNums(self.windingOrder) ) + "\n"
		for pos in self.pos:
			line += " ".join( strNums(pos)) + " "
		print(line + "\n")
		
	def printAll(self):
		strNums = lambda x: [ str(num) for num in x ]
		line = "NameLength: %s NodeName: %s NodeType: %s Tris: %s\n" %(self.nameLen, self.nodeName, self.nodeType, self.numFaces)
  		line += "WindingOrder: %s\n" %" ".join(strNums(self.windingOrder))
		line += "Position: \n"
		for i, pos in enumerate(self.pos):
			if( (i+1) % 3 ):
				line += " ".join( strNums(pos)) + " "
			else:
				line += " ".join( strNums(pos)) + "\n"
		print(line + "\n")			
		
class PolyFace( object ):
	def __init__( self, face ):
		'''
		This class will contain 3 Vertex Class (triangle) and the winding order
		'''
		self.name = face
		self.vertex = []
		self._getVertex()
		
		self.numOfVertex = len(vertex)
		self.windingOrder = PolyFace.findWindingOrder(self.name)
		self.vertexCoords = []
		# This will be acording to the face we're currently recording.
		# self.normal
		# http://xyz2.net/mel/mel.005.htm
	'''	
	def findNormal(self, vertex, face ):
		faceVtx = cmds.polyListComponentConversion( 'pCube1.vtx[3]', fv=1, tvf=1 )
		allFaceVtx = cmds.filterExpand( faceVtx, sm=70 )
		cmds.polyNormalPerVertex('pCube1.vtxFace[3][3]', q=True, xyz=True ) 
	'''
	
	def _getVertex( self ):
		verts = cmds.cmds.polyListComponentConversion( self.name, ff=1, tv=1 )
		allVerts = cmds.filterExpand( verts, sm=31, expand=True )
		for vtx in allVerts:
			self.vertex.append( Vertex(vtx) )
	
	@staticmethod
	def getNumOfVertex(face):
		vertex = cmds.polyListComponentConversion( face, tv=True )
		allVerts = cmds.filterExpand( vertex, sm=31, expand=True )
		return len(allVerts)

	@staticmethod
	def findWindingOrder(face):
		# Converts faces into verts (the are return in the proper winding order
		vertex = cmds.polyListComponentConversion( face, tv=True )
		# if any of the verts of compressed into ranges the will be expanded.
		allVerts = cmds.filterExpand( vertex, sm=31, expand=True )
		return allVerts

	def getWindingOrder(self):
		return self.windingOrder
		
			
	def toString(self):
		'''
		# Tris
		# Winding Worder
		# pos
		# 12
		# 0 0 0 1 1 1 2 2 2 etc
		# 0.5 0.5 0.5 etc
		Postion of vertex by its winding order print out in a flat string.
		# Ready for an exporter.
		'''
		info = str(self.numOfVertex)
		
		
		
			
		return vertPos
'''

# Getting the current uvSet
currUVSet = cmds.polyUVSet( 'pCubeShape1', q=True, currentUVSet=True )[0]

indices = cmds.polyUVSet('pCubeShape1', query=True, allUVSetsIndices=True)
numSets = len(indices)

print("Number of UVSets: %s" %numSets)
# Starting with how many uvs there are print out the uv's
for i in range( numSets ):
    # Does the setname need to be recorded?
    # Set uv to this current uvSet. 
    setName = cmds.getAttr( "pCubeShape1.uvSet[%s].uvSetName" %i )
    cmds.polyUVSet( 'pCubeShape1', currentUVSet=True, uvSet=setName )   
    # How many uvs are there
    uvs = cmds.polyListComponentConversion( 'pCubeShape1', tuv=True )
    allUVs = cmds.filterExpand( uvs, sm=35 , expand=True )
    
    uvCoords = cmds.polyEditUV( allUVs, q=True )
    # What are the uv's coords (not ordered)

    print("UVSetName: %s UVNum: %s" %(setName, len(allUVs)))
    print(allUVs)
    print(uvCoords)

# Change the uvSet back to the orginal
cmds.polyUVSet( 'pCubeShape1', currentUVSet=True, uvSet=currUVSet )
'''
# How many uvSets
# Find each uvSet
# Get the material name (and the string length)
# how many textures
# name of the texture

# number of how many uvsets
# after the Num of UVsets then the same format as the normals
# Material
# name and material
# name of the texture and 
# length of the string 8bits 256
# material name, how many textures, texture names

# Each time its a string length of the string and then the string.

# enum attr name ShaderMaterial go on the 

class Transform(Node):
	# Its has a shape node acompaning it
	def __init__(self, nodeName):
		Node.__init__(self, nodeName)
		self.children = cmds.listRelatives( self.nodeName, c=True )
		self.numChildren = None
		if( self.children ):
			self.numChildren = len( self.children )
		self.pos = self._getPos()

	def _getPos(self):
		return cmds.xform( self.nodeName, q=True, ws=True, piv=True)[0:3]
		
	def printAll(self):
		strNums = lambda x: [ str(num) for num in x ]	
		line = "NameLength: %s NodeName: %s NodeType: %s\n" %(self.nameLen, self.nodeName, self.nodeType)
		line += "Position: %s\n" %(" ".join(strNums(self.pos)))
		print(line)
		
		# print( "NumOfChildren: %s Children: %s" %(self.numChildren, ", ".join(self.children)) )
		# print( "Position: %s" %(" ".join(self.pos)) )
		
	def printInfo(self):
		strNums = lambda x: [ str(num) for num in x ]	
		line = "%s %s %s\n" %(self.nameLen, self.nodeName, self.nodeType)
		line += " ".join(strNums(self.pos)) + "\n"
		
		print(line)
		
class Group(Node):
	# If its a leaf and not a shape node then its a group
	def __init__(self, nodeName):
		Node.__init__(self, nodeName)
		self.children = cmds.listRelatives( self.nodeName, c=True )
		self.numChildren = None
		if( self.children ):
			self.numChildren = len( self.children )
		self.pos = self._getPos()

	def _getPos(self):
		return cmds.xform( self.nodeName, q=True, ws=True, piv=True)[0:3]
		
	def printAll(self):
		strNums = lambda x: [ str(num) for num in x ]	
		line = "NameLength: %s NodeName: %s NodeType: %s\n" %(self.nameLen, self.nodeName, self.nodeType)
		line += "Position: %s\n" %(" ".join(strNums(self.pos)))
		print(line)
		'''
		print( "NameLength: %s NodeName: %s NodeType: %s" %(self.nodeName, self.nameLen, self.nodeType) )
		print( "NumOfChildren: %s Children: %s" %(self.numChildren, ", ".join(self.children)) )
		print( "Position: %s" %(" ".join(self.pos)) )
		'''
	def printInfo(self):
		strNums = lambda x: [ str(num) for num in x ]			
		line = "%s %s %s\n" %(self.nameLen, self.nodeName, self.nodeType)
		line += " ".join(strNums(self.pos)) + "\n"
		print(line)
		

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
