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
import maya.cmds as cmds

emit = cmds.emitter(n='spray',)
part = cmds.particle(n='droplets')
cmds.connectDynamic(part[0], em=emit[0])
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
I am guessing that the script will have to be turned into python for
the Current Render Type button as well.

#Current Render Type button script in Mel
addAttr -is true -ln "colorAccum" -at bool -dv false dropletsShape;
addAttr -is true -ln "useLighting" -at bool -dv false dropletsShape;
addAttr -is true -ln "pointSize" -at long -min 1 -max 60 -dv 2 dropletsShape;
addAttr -is true -ln "multiCount" -at long -min 1 -max 60 -dv 10 dropletsShape;
addAttr -is true -ln "multiRadius" -at "float" -min 0 -max 10 -dv 0.3 dropletsShape;
addAttr -is true -ln "normalDir" -at long -min 1 -max 3 -dv 2 dropletsShape;
'''
#Turn Color Accum off
cmds.setAttr('dropletsShape.colorAccum', 0)

#Didn't add in all of the attributes for multipoint, just what was directed in the tutorial
#Turn on Use Lighting
cmds.setAttr('dropletsShape.useLighting', True)

#Point Size to 1
cmds.setAttr('dropletsShape.pointSize', 1)

