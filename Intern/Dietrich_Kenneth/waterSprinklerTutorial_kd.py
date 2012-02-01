import maya.cmds as cmds

# Creating emitter and particle object
emit = cmds.emitter(n='spray',) # Returns lists

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