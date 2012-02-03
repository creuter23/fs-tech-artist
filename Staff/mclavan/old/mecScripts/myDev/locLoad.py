import maya.cmds as cmds
myFile = open( r"E:\000004.xyz", "r")

i = 0
while( i < 100000 ):
	tempLine = myFile.readline()
	positions = [ float(tempLine.split()[0]), float(tempLine.split()[1]), float(tempLine.split()[2]) ]
	i = i + 1	
	# print( "Line %i: X: %s Y: %s Z:%s" %(i, tempLine.split()[0], tempLine.split()[1], tempLine.split()[2]) )
	cmds.spaceLocator( p=positions, name="loc_%i" %i )
	cmds.xform( a=True, scale=[0.01, 0.01, 0.01] )
	cmds.setAttr( ".localScaleX", 0.01 )
	cmds.setAttr( ".localScaleY", 0.01 )
	cmds.setAttr( ".localScaleZ", 0.01 )

cmds.group( cmds.ls("loc_*"), n="points" )
myFile.close()

