import maya.cmds as cmds

# Creating emitter and particle object
emit = cmds.emitter(n='spray', dx=0, dy=1, dz=0, r=100, sp=0.17, spd=5) # Returns lists

# Return List [particle, particleShape]
part = cmds.particle(n='droplets')

# Connecting particle to emitter
cmds.connectDynamic(part[0], em=emit[0])

# Selecting object in scene
hose_objects = cmds.ls(sl=True)

# Parenting emitter to hose. First selected object.
cmds.parent( emit[0], hose_objects[0] )

part_attrs = {'depthSort':True, 'particleRenderType':0}

for attr, value in part_attrs.items():
    cmds.setAttr('%s.%s' %(part[1], attr), value)
   
#The code for Current Render Type button inside the particleShape
#ln=longName, at=attributeType, dv=defaultValue, min=minValue, max=maxValue
#When activating the Current Render Type button, make sure the code is part[1], and not [0]:
#[0] is the emitter.
cmds.addAttr(part[1], internalSet=True, ln="colorAccum", at="bool", dv=False )
cmds.addAttr(part[1], internalSet=True, ln="useLighting", at="bool", dv=False )
cmds.addAttr(part[1], internalSet=True, ln="pointSize", at="long", min=1, max=60, dv=2 )
cmds.addAttr(part[1], internalSet=True, ln="multiCount", at="long", min=1, max=60, dv=10 )
cmds.addAttr(part[1], internalSet=True, ln="multiRadius", at="float", min=0, max=10, dv=0.3 )
cmds.addAttr(part[1], internalSet=True, ln="normalDir", at="long", min=1, max=3, dv=2 )

part_attrs = {'colorAccum':False, 'useLighting':True, 'particleRenderType':0,}

for attr, value in part_attrs.items():
    cmds.setAttr('%s.%s' %(part[1], attr), value)