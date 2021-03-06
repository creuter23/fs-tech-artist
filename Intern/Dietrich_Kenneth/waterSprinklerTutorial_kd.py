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
#When activating the Current Render Type button, make sure the code is part[1],
#this is the particleShape node that will need to be selected when editing attrs and not [0]
#[0] is the particle.
cmds.addAttr(part[1], internalSet=True, ln="colorAccum", at="bool", dv=False )
cmds.addAttr(part[1], internalSet=True, ln="useLighting", at="bool", dv=False )
cmds.addAttr(part[1], internalSet=True, ln="pointSize", at="long", min=1, max=60, dv=2 )
cmds.addAttr(part[1], internalSet=True, ln="multiCount", at="long", min=1, max=60, dv=10 )
cmds.addAttr(part[1], internalSet=True, ln="multiRadius", at="float", min=0, max=10, dv=0.3 )
cmds.addAttr(part[1], internalSet=True, ln="normalDir", at="long", min=1, max=3, dv=2 )

part_attrs = {'colorAccum':False, 'useLighting':True, 'particleRenderType':0,}

for attr, value in part_attrs.items():
    cmds.setAttr('%s.%s' %(part[1], attr), value)

#Adding fields
#This code selects the particles so the gravity field can be added
cmds.select(part)
drop_grav = cmds.gravity(part, m=15, dy=-1)
cmds.connectDynamic(part, f='gravityField1')

#Reselect Particles to add in the radial field
cmds.select(part)
radial_drop = cmds.radial(part, m=0.010)
cmds.connectDynamic(part, f=radial_drop[0])

#Create Partilce Mist from the Particle Tool
mist_part_1 = cmds.particle(n='mist', c=0)
mist_part_2 = cmds.particle(n='mist1', c=0)
cmds.select(mist_part_1[0])
cmds.connectDynamic(mist_part_1[0], em=emit[0])
cmds.select(mist_part_2[0])
cmds.connectDynamic(mist_part_2[0], em=emit[0])

#Add gravityField1 and radialField1 to mist and mist1 through dynamicRelationship editor
cmds.select(mist_part_1[0])
cmds.connectDynamic(mist_part_1[0], f='gravityField1')
cmds.connectDynamic(mist_part_1[0], f='radialField1')
cmds.select(mist_part_2[0])
cmds.connectDynamic(mist_part_2[0], f='gravityField1')
cmds.connectDynamic(mist_part_2[0], f='radialField1')

#Add color (rgbPP) to the particles.
cmds.select(part)

cmds.addAttr(part[1], internalSet=True, ln="colorRed", dv=0.0, at="double", keyable=True )

cmds.addAttr(part[1], internalSet=True, ln="colorGreen", dv=0.0, at="double", keyable=True )

cmds.addAttr(part[1], internalSet=True, ln="colorBlue", dv=0.0, at="double", keyable=True )


part_rgbPO_attrs = {'colorRed':True, 'colorGreen':True, 'colorBlue':True, 'particleRenderType':0,}

for attr, value in part_rgbPO_attrs.items():
    cmds.setAttr('%s.%s' %(part[1], attr), value)

#Change the color to blue with the rgbPO attr
part_rgbPO_attrs = {'colorRed':0.2, 'colorGreen':0.5, 'colorBlue':1.0, 'particleRenderType':0,}

for attr, value in part_rgbPO_attrs.items():
    cmds.setAttr('%s.%s' %(part[1], attr), value)
    
#Add and change the rgbPO color of the mist particles
cmds.select(mist_part_1)

cmds.addAttr(mist_part_1[1], internalSet=True, ln="colorRed", dv=0.0, at="double", keyable=True )

cmds.addAttr(mist_part_1[1], internalSet=True, ln="colorGreen", dv=0.0, at="double", keyable=True )

cmds.addAttr(mist_part_1[1], internalSet=True, ln="colorBlue", dv=0.0, at="double", keyable=True )


part_rgbPO_attrs = {'colorRed':True, 'colorGreen':True, 'colorBlue':True, 'particleRenderType':0,}

for attr, value in part_rgbPO_attrs.items():
    cmds.setAttr('%s.%s' %(mist_part_1[1], attr), value)

#Change the color to blue with the rgbPO attr
part_rgbPO_attrs = {'colorRed':0.2, 'colorGreen':0.5, 'colorBlue':1.0, 'particleRenderType':0,}

for attr, value in part_rgbPO_attrs.items():
    cmds.setAttr('%s.%s' %(mist_part_1[1], attr), value)
    
#Add and change the rgbPO color of the mist1 particles
cmds.select(mist_part_2)

cmds.addAttr(mist_part_2[1], internalSet=True, ln="colorRed", dv=0.0, at="double", keyable=True )

cmds.addAttr(mist_part_2[1], internalSet=True, ln="colorGreen", dv=0.0, at="double", keyable=True )

cmds.addAttr(mist_part_2[1], internalSet=True, ln="colorBlue", dv=0.0, at="double", keyable=True )


part_rgbPO_attrs = {'colorRed':True, 'colorGreen':True, 'colorBlue':True, 'particleRenderType':0,}

for attr, value in part_rgbPO_attrs.items():
    cmds.setAttr('%s.%s' %(mist_part_2[1], attr), value)

#Change the color to blue with the rgbPO attr
part_rgbPO_attrs = {'colorRed':0.2, 'colorGreen':0.5, 'colorBlue':1.0, 'particleRenderType':0,}

for attr, value in part_rgbPO_attrs.items():
    cmds.setAttr('%s.%s' %(mist_part_2[1], attr), value)

#Change the Lifespan of droplets particles
part_lifespan_attrs = {'lifespanMode':3}

for attr, value in part_lifespan_attrs.items():
    cmds.setAttr('%s.%s' %(part[1], attr), value)

