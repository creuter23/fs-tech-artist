
# Generate the curve and catch the name
curve -d 1 -p 1 0 11 -p -1 0 11 -p -1 0 -1 -p 1 0 -1 -p 1 0 11 -k 0 -k 1 -k 2 -k 3 -k 4 ;

circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -ch 1;

# parent

# set the limits
# Should move in those axis.
transformLimits -tx 0 0 -etx 1 1 nurbsCircle1;
transformLimits -ty 0 0 -ety 1 1 nurbsCircle1;

# z limited
transformLimits -tz 0 10 -etz 1 1 nurbsCircle1;

# Lock and Hide unused attributes.
cmds.setAttr( ".rx", locked=True )

setAttr -lock true -keyable false -channelBox false "nurbsCircle1.rx";
setAttr -lock true -keyable false -channelBox false "nurbsCircle1.ry";
setAttr -lock true -keyable false -channelBox false "nurbsCircle1.rz";

cmds.setAttr( "object.attr", lock=True, keyable=False, channelBox=False )


# Setting up reference on shape node
setAttr "curveShape1.overrideEnabled" 1;
setAttr curveShape1.overrideDisplayType 2;


# Getting the shape node and appling reference.
selected = cmds.ls(sl=True)[0] #First Item
shapes = cmds.listRelatives(selected, shapes=True )
for shape in shapes:
	cmds.setAttr( shape + ".overrideEnabled", 1)
	cmds.setAttr( shape + ".overrideDisplayType", 2)

	
# Putting all the pieces together

def faceCurve( iconName ):
	# Create the curves
	# curve -d 1 -p 1 0 11 -p -1 0 11 -p -1 0 -1 -p 1 0 -1 -p 1 0 11 -k 0 -k 1 -k 2 -k 3 -k 4 ;
	pad = cmds.curve( name=iconName +"_grp", d=1, p=[[1, 0, 11], [-1, 0, 11], [-1, 0, -1], [1, 0, -1], [1, 0, 11]], k=[0,1,2,3,4])
	# circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -ch 1;
	iconName = cmds.circle(name=iconName, c=[0,0,0], nr=[0,1,0], sw=360, r=1, d=3, ut=0, tol=0.01, s=8, ch=1 )

	# Limit the transforms
	# transformLimits -tz 0 10 -etz 1 1 nurbsCircle1;
	cmds.transformLimits( iconName[0], tz=[0,10], etz=[1,1] )
	
	# Lock and Hide Attributes
	# setAttr -lock true -keyable false -channelBox false "nurbsCircle1.rz";
	# cmds.setAttr( "object.attr", lock=True, keyable=False, channelBox=False )
	# cmds.setAttr( iconName[0] + ".tx", lock=True, keyable=False, channelBox=False )

	attrs = ["tx", "ty", "rx", "ry", "rz", "sx", "sy", "sz"]
	for attr in attrs:
		cmds.setAttr( iconName[0] + "." + attr, lock=True, keyable=False, channelBox=False )
		
	# Parent 
	cmds.parent( iconName[0], pad )
	

def refCurve():
	selected = cmds.ls(sl=True) #First Item
	for sel in selected:
		shapes = cmds.listRelatives(sel, shapes=True )
		for shape in shapes:
			cmds.setAttr( shape + ".overrideEnabled", 1)
			cmds.setAttr( shape + ".overrideDisplayType", 2)	
