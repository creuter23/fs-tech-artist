# Final exporter

class Vertex( object ):
	def __init__( self, vertex ):
		'''
		object.vtx[0]
		'''
		# entire name of the vector object.vtx[0]
		# self.name = vertex
		self.idNum = Vertex.getIDNum( vertex )
		self.pos = Vertex.getVtxPos( vertex )
		self.uv = Vertex.getUVCords( vertex ) 
		# self.normal = ??
		# Do I need to record a three normals?
	
	@staticmethod
	def getUVSets( vertex ):
		cmds.polyUVSet(vertex, query=True, allUVSets=True)
		
	@staticmethod
	def getUVs( vertex ):
		
		uvSets = Vertex.getUVSets(vertex)
		currUVSet = cmds.polyUVSet( vertex, q=True, currentUVSet=True )

		totalUVs = []
		for uvSet in uvSets:
			# Set uv to this current uvSet. 
			cmds.polyUVSet( vertex, currentUVSet=True, uvSet=uvSet ) 			
			
			uvMaps = Vertex.getUVMaps(vertex)
		
			# Convert to coords
			uvCoords = cmds.polyEditUV( uvMaps , q=True )
			totalUVs.append(uvCoords)
		
		cmds.polyUVset( vertex, currentUVSet=True, uvSet=currUVset)	
		# sets
		
	@staticmethod
	def getUVMaps( vertex ):
		uv = cmds.polyListComponentConversion( vertex, fv=True, tuv=True )
		uvAll = cmds.filterExpand( uv, expand=True, sm=35 )
		
		return uvAll
		
	@staticmethod
	def getIDNum( vertex ):
		'''
		Get the id number out of the vertex string
		'''
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
	
	@staticmethod
	def getUVCords( vertex ):
		'''
		Given the obj.vtx[0] it will return the uv coords for the current vertex
		'''
	
		return 0

'''
import maya.cmds as cmds

polyType = 'pCube1.f[0]'
shape = 'pCubeShape1'

faces = cmds.polyListComponentConversion( shape, tf=True )
allFaces = cmds.filterExpand( faces, sm=34, expand=True )
windingOrder = []
pos = []

# Getting UV Position
uvMap = cmds.polyListComponentConversion( 'pCube1.vtx[1]', fv=1, tuv=True )
uvAllMap = cmds.filterExpand( uvMap, sm=35 )
uvCoords = cmds.polyEditUV( uvAllMap, q=True )[:1]

# Getting the normal
polyNormalPerVertex -q -xyz $vtxFace
faceVtx = cmds.polyListComponentConversion( 'pCube1.vtx[3]', fv=1, tvf=1 )
allFaceVtx = cmds.filterExpand( faceVtx, sm=70 )
cmds.polyNormalPerVertex('pCube1.vtxFace[3][3]', q=True, xyz=True ) 

for face in allFaces:
    verts = cmds.polyListComponentConversion( face, ff=True, tv=True )
    allVerts = cmds.filterExpand( verts, sm=31, expand=True )
    print( "Face: %s Vertex: %s" %(face, allVerts))
    for vert in allVerts:    
        print( cmds.pointPosition( vert, w=True ) )
        pos.extend( cmds.pointPosition( vert, w=True) )
    windingOrder.extend( allVerts )

cmds.polyListComponentConversion( u'pCube1.f[0]', ff=True, tv=True )
# polyListComponentConversion converts shape to the bare differnt types verts, faces, uv, etc...
# filterExpand expands the compressed index system [*] to list every component. 

# from shape to vertex
# Gets all the vertex of the shape node
# [u'pCube1.vtx[*]']
vertex = cmds.polyListComponentConversion( shape, tv=True )

# Expand the vertex from the compressed format.
allVerts = cmds.filterExpand( vertex, sm=31, expand=True )

# Get the vertex by a selected face.
vertex = cmds.polyListComponentConversion( cmds.ls(sl=True), tv=True )
allVerts = cmds.filterExpand( vertex, sm=31, expand=True )

# It will expand everything.
allVerts = cmds.filterExpand( [u'pCube1.vtx[1]', u'pCube1.vtx[3:6]', u'pCube1.vtx[7]'], sm=31, expand=True )

# Winding order
faceVertex = cmds.polyListComponentConversion( cmds.ls(sl=True), fromFace=True, toVertexFace=True )
allFaceVertex = cmds.filterExpand( faceVertex, sm=70, expand=True )
for fv in allFaceVertex:
    vertex = cmds.polyListComponentConversion( fv, fromVertexFace=True, toVertex=True)
    print("faceVertex: %s vertex %s" %(fv, vertex))
    
"""
Observation
Component Conversion is returning the winding order.
[u'pCube1.vtx[3]', u'pCube1.vtx[5]', u'pCube1.vtx[7]']  # face 9
[u'pCube1.vtx[1]', u'pCube1.vtx[3]', u'pCube1.vtx[7]']  # face 8
"""

# returns the map uv [u'pCube1.map[*]']
# Most likely will have to be expanded
toUV = cmds.polyListComponentConversion( shape, tuv=True )

# total vertex in the shade node
numVerts = len(allVerts)

# Get all the faces and expand them
faces = cmds.polyListComponentConversion( shape, toFace=True )
allFaces = cmds.filterExpand( faces, sm=34 ,expand=True )
numOfFaces = len(allFaces)


# what is the difference between a poly face (selectionMask=34 ) and
#  a vertex face (selectionMask=70)
"""
----------------------- OTHER CODE --------------------
"""

cmds.filterExpand( polyType, sm=70, expand=True )

# winding order
cmds.filterExpand( "sm-70, expand=True )
vertexFace = "%s.vtxFace[%s][%s]" %(cmds.ls(sl=True)[0], 1, 3)
cmds.polyNormalPerVertex( vertexFace, q=1, xyz=1)

filterExpand


polyListComponentConversion 
'''
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
		

	# Static member class to obtain the winding order of a face.

class ShapeNode():
	'''
	- Needs to have total number of vertex
	- Needs to be able to get flattened version of:
		- vertex Position
		- uv coords
		- winding order
			- Because we are working with triangles we know how to read the data for each of these.
			- Nothing special will be required to seperate the data
	'''

	def __init__(self):
		self.faces
		self.numFaces
		self.windingOrder
		self.pos
		# self.normals
		# self.sets
		# self.uvs
		# self.material
		
		
	def numberOfFaces(self):
		faces = cmds.polyListComponentConversion( shape, toFace=True )
		allFaces = cmds.filterExpand( faces, sm=34 ,expand=True )
		numOfFaces = len(allFaces)

	def toString(self):
		'''
		Faces
		Vert winding order
		Vert position
		'''
		
		
		
'''
# Check ou what this is being used for
# Regular Expression
def stripText( string unstriped ):
	pattern = r'[^\[]*$'
	# stripped = cmds.match
	# string $stripped = `match "[^\[]*$" $unstripped`;
	# $stripped = `match "[0-9]+" $stripped`;
'''

def faceOrder( face ):
	vertexOrder = []
	
	# Use polyListComponentConversion to get .vtxFace Components
	# vtxface will be a list
	vtxFace = cmds.polyListComponentConversion( fromFace=True, toVertexFace=face )
	
	vtxFace = cmds.filterExpand(vtxFace, sm=70, expand=True )
	
	for vf in vtxFace:
		# string $vertex[] = `polyListComponentConversion -fromVertexFace -toVert
		vertex = cmds.polyListComponentConversion( vf, fromVertexFace=True, toVertex=True)
		
		# stripText isn't completed yet.  Looks like he's removing the vtxFace text, keeping the range.
		vertexOrder.append( stripText( $vertex[0] ) )
		
	return vertexOrder
	
def getShapes( xform ):
	'''
	What does this function do?
	It looks like it returns the shape node of the passed in argument xform.
	'''
	shapes = []
	
	shapes.append( xform )
	
	if( "transform" == cmds.nodeType( xform ) ):
		# If given node is not a transform, assume it is a shape
		# and pass it through
		shapes = cmds.listRelatives(xform, shapes=True)
		
	return shapes
	
def getVFNormal( mesh, vert, face ):
	# object.vtxFace[0][0] 
	# This function returns the normal of the current vertex
	vertexFace = "%s.vtxFace[%s][%s]" %(mesh, vert, face)
	vertPos = cmds.polyNormalPerVertex( vertexFace, q=True, xyz=True )
	return vertPos	
	
def myGetNum( vertName ):
	# shape node
	shapeNodes = getShapes( vertName ) # List
	# Result: bob.vtx[0]
	vertListC = cmds.polyListComponentConversion( shapeNodes, tv=True ) # List
	# Result: bob.vtx[0] //	
	vertList = cmds.filterExpand( vertListC, sm=31 )  # sm=32 is Polygon Vertices
	# Result: 0 //
# stripText isn't fininshed yet.
	vertNumber = stripText( vertList[0] )  
	# // Result: -24.506507 -24.506507 24.506507 //
	
	vertPos = cmds.pointPosition( vertList[0], w=True )
	# // Result: bob.map[0] bob.map[8] //
	
	uvC = cmds.polyListComponentConversion( shapeNodes[0], tuv=True ) # List
	# // Result: bob.map[0] bob.map[8] //
	
	uvList = cmds.filterExpand( uvC, sm=35 )
	# // Result: 0.375 0 //

	uvPos = cmds.polyEditUV( uvList, q=True )
	
	# Convert postion of vert to a single string
	myVertPos = " ".join( [vertPos[0], vertPos[1], vertPos[2]] )
	# Convert position of vert to a single string
	myUVPos = " ".join( [uvPos[0], uvPos[1]] )
	
	# declare the rturn array and add items to it
	myReturn = []
	myReturn.append( myUVPos )
	myReturn.append( myVertPos )
	
	return myReturn
	
	

