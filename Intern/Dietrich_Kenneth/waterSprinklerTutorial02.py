'''
#this is the particle emitter code in Maya layed out and explained
emitter
    #postion
    -pos 0 0 0

    #type
    -type direction

    #name
    -name "waterSprinklerEmitter01#"

    #rate
    -r 100

    #scaleRateByObjectSize
    -sro 0

    #needParentUV
    -nuv 0

    #cycleEmission
    -cye none

    #cycleInterval
    -cyi 1

    #speed
    -spd 1

    #speedRandom
    -srn 0

    #normalSpeed
    -nsp 1

    #tangentSpeed
    -tsp 0

    #maxDistance
    -mxd 0

    #minDistance
    -mnd 0

    #directionX
    -dx 1

    #directionY
    -dy 0

    #directionZ
    -dz 0

    #spread
    -sp 0 ;
'''
#Turn the Particle Emitter Creation Mel into Python
#Make the objects name into hose so the emitter can properly parent
#Then just run the script and everything shall be made and put together
import maya.cmds as cmds

emit = cmds.emitter(n='spray',)
part = cmds.particle(n='droplets')
cmds.select('droplets')
cmds.connectDynamic(part[0], em=emit[0])
cmds.select('hose')
selected = cmds.ls(sl=True)[0]
cmds.parent( 'spray', selected )


#To turn Depth Sort on the particles
cmds.setAttr(part[1] + '.depthSort', True)
attrName = 'depthSort'
cmds.setAttr('%s.depthSort' %(part[1]), True)
#For some reason the script editor will not work with these below
#along with all of the script at once, but they will individualy.
#Turn particle shape into Multipoints... selected list is 0
cmds.setAttr('dropletsShape.particleRenderType', 0)

'''
addAttr -is true -ln "colorAccum" -at bool -dv false dropletsShape;
addAttr -is true -ln "useLighting" -at bool -dv false dropletsShape;
addAttr -is true -ln "pointSize" -at long -min 1 -max 60 -dv 2 dropletsShape;
addAttr -is true -ln "multiCount" -at long -min 1 -max 60 -dv 10 dropletsShape;
addAttr -is true -ln "multiRadius" -at "float" -min 0 -max 10 -dv 0.3 dropletsShape;
addAttr -is true -ln "normalDir" -at long -min 1 -max 3 -dv 2 dropletsShape;

cmds.addAttr(internalSet= True, ln='colorAccum', at='bool', dv=False, dropletsShape)
cmds.addAttr(internalSet= True, ln='useLighting', at='bool', dv=False, dropletsShape)
cmds.addAttr(internalSet= True, ln='pointSize', at='bool', dv=False, dropletsShape)
cmds.addAttr(internalSet= True, ln='multiCount', at='bool', dv=False, dropletsShape)
cmds.addAttr(internalSet= True, ln='multiRadius', at='bool', dv=False, dropletsShape)
cmds.addAttr(internalSet= True, ln='normalDir', at='bool', dv=False, dropletsShape)


#Turn Color Accum off
cmds.setAttr('dropletsShape.colorAccum', 0)

#Didn't add in all of the attributes for multipoint, just what was directed in the tutorial
#Turn on Use Lighting
cmds.setAttr('dropletsShape.useLighting', True)

#Point Size to 1
cmds.setAttr('dropletsShape.pointSize', 1)
'''

#Adding Fields
'''
gravity -pos 0 0 0 -m 9.8 -att 0 -dx 0 -dy -1 -dz 0  -mxd -1  -vsh none -vex 0 -vof 0 0 0 -vsw 360 -tsr 0.5 ;
// gravityField1 //
#Select particles before adding in fields
'''
cmds.select('droplets')
cmds.gravity('droplets', m=15, dy=-1)
cmds.connectDynamic('droplets', f='gravityField1')
#Reselect Particles
cmds.select('droplets')
cmds.radial('droplets', m=0.010)
cmds.connectDynamic('droplets', f='radialField1')

#Create Partilce Mist from the Particle Tool
cmds.particle(n='mist', c=0)
cmds.particle(n='mist1', c=0)
cmds.select('mist')
cmds.connectDynamic('mist', em=emit[0])
cmds.select('mist1')
cmds.connectDynamic('mist1', em=emit[0])

#Add gravityField1 and radialField1 to mist and mist1 through dynamicRelationship editor
cmds.select('mist')
cmds.connectDynamic('mist', f='gravityField1')
cmds.connectDynamic('mist', f='radialField1')
cmds.select('mist1')
cmds.connectDynamic('mist1', f='gravityField1')
cmds.connectDynamic('mist1', f='radialField1')