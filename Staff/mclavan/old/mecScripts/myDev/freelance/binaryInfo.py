import maya.cmds as cmds
import struct

'''
f = file(filePath ,'wb')
bindata = strBin("pSphere1")
f.write(bindata)

bindata = strBin("bodyGeo")
f.write(bindata)
f.close()

f = file(filePath ,'rb')
strInfo = strBinRead(f)
strInfo2 = strBinRead(f)
f.close()
'''


'''
f = file(filePath ,'wb')
bindata = strBin("Hello")
f.write(bindata)
f.close()
'''

'''
Creating translates 
# Writing
trans = cmds.xform( q=True, t=True )
# 3f is for three float values
binInfo = struct.pack( '3f', trans[0], trans[1], trans[2] )

f = file(filePath ,'wb')
f.write(binInfo)
f.close()

# Reading
f = file(filePath ,'rb')
# 4 bytes for a 32bit value, so x,y,&z == 12
binInfo = f.read(12)
f.close()
binVal = struct.unpack( '3f', binInfo )

'''
# getFileNames( cmds.ls(sl=True)[0] )
'''
It works but some error checking needs to be done.
1) What if there are no files assosicated with the material
- listConnections returns None if it doesn't make a match.
- Placed an if statement to check.  If None is passed then the function will return []

'''

def getFileNames( shapeNode ):
	
	# Get the shaderGrp
	sg = shape2SG( shapeNode )
	# Get the material
	mat = getSG2Mat( sg )
	# Get the files
	files = mat2File( mat )

	print( "SG: %s MAT: %s Files: %s" %(sg, mat, " ".join(files)))
	return files



def shape2SG( shapeNode ):
	sgs = cmds.ls( type="shadingEngine" )
	connSG = None
	for sg in sgs:
		results = cmds.sets( shapeNode, isMember=sg)
		if( results ):
			connSG = sg
			
	return connSG
	
# shape2SG( cmds.ls(sl=True)[0] )

def mat2File( materialName ):
	# gets the file nodes from the selected material.
	fileNodes = cmds.listConnections(materialName,  t='file' )
	print(fileNodes)
	fileNames = []
	if( fileNodes ):
		for fileNode in fileNodes:
			fileName = cmds.getAttr( "%s.fileTextureName" %fileNode)
			fileNames.append(fileName)
	
	return fileNames

# mat2File( cmds.ls(sl=True )[0] )


def getSG2Mat( shaderGrp ):
	conns = cmds.listConnections( shaderGrp,  s=True )
	forbidden = ['lightLinker', 'materialInfo', 'transform', 'partition', 'renderPartition'] 
	material = None
	for conn in conns:
		nType = cmds.nodeType(conn)
		# print(nType )
		
		if( nType not in forbidden ):
			# print("Match: %s NodeName: %s" %(nType, conn))
			material = conn
		
	return material


# getSG2Mat( cmds.ls(sl=True)[0] )


def str2Bin(strVal):
	'''
	Converts string to binary (doesn't include name length with), return struct pack
	'''
	strLen = len(strVal)
	
	fmt = '%ss' %strLen
	binData = struct.pack(fmt, strVal)
	return binData	

def strLen2Bin( strVal ):
	'''
	Converts nameLen and string into binary, returns struct pack
	'''
	strLen = len(strVal)
	
	fmt = 'i%ss' %strLen
	binData = struct.pack(fmt, strLen, strVal)
	return binData

def flt2Bin( val ):
	'''
	Convert single float to binary returns struct pack
	'''

	binData = struct.pack('f', val)
	return binData		

def flt32Bin( vals ):
	'''
	Convert vector to binary returns struct pack
	'''
	binData = struct.pack('3f', vals[0], vals[1], vals[2])
	return binData

'''
f = file(filePath ,'rb')
strInfo = strBinRead(f)
f.close()
'''
def strBinWrite( fileStream, strVal ):
	binaryInfo = strBin( strVal )
	fileStream.write( binaryInfo )
	
	
	
def strBinRead( fileStream ):
	'''
	Takes the filesteam and reads out the proper data.
	'''
	
	strPrime = fileStream.read(4)
	# print("Stream: %s " %strPrime )
	strLen = struct.unpack('i', strPrime)[0]
	print("strLen: %s" %(strLen))

	strData = fileStream.read(strLen)
	print(strData)
	strInfo = struct.unpack('%ss' %strLen, strData )
	
	return strInfo[0]
