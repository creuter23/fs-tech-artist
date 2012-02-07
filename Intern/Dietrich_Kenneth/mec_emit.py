'''
emit1 = my_emitter(cmds.ls(sl=True)[0], 'sprink11')
emit1 = my_emitter(cmds.ls(sl=True)[1], 'sprink22')
emit1 = my_emitter(cmds.ls(sl=True)[2], 'sprink33')
'''
# Standard Library
import random
# 3rd Party
import maya.cmds as cmds
# Custom

def my_emitter(object, emit_name, offset=[0, 0, 0], dx=0, dy=1, dz=0, rate=100, sp=0.17, spd=5):
    '''
    Creates my custom emitter
    '''
    cmds.select(cl=True)
    # Creating emitter and particle object
    emit = cmds.emitter(n='%s#' % emit_name, dx=dx, dy=dy, dz=dz, r=rate, sp=sp, spd=spd) # Returns lists
    # emit = cmds.emitter(dx=dx, dy=dy, dz=dz, r=rate, sp=sp, spd=spd) # Returns lists
        
    # Return List [particle, particleShape]
    part = cmds.particle(n=emit[0] + '_droplets')

    print emit_name, emit, part
    
    # Connecting particle to emitter
    cmds.connectDynamic(part[0], em=emit[0])
    
    # Emitting placement area
    # Catch objects position (Translate, rotate, and scale)
    trans = cmds.xform(object, q=1, a=True, ws=True, t=True)
    trans[0] = trans[0] + offset[0]
    trans[1] = trans[1] + offset[1]
    trans[2] = trans[2] + offset[2]
    print 'TransPos:', trans
    
    rot = cmds.xform(object, q=1, a=True, ws=True,ro=True)
    # move emitter to object
    cmds.xform(emit[0], a=True, ws=True, t=trans)
    cmds.xform(emit[0], a=True, ws=True, ro=rot)
    
    
    # Parenting emitter to hose. First selected object.
    # cmds.parent( emit[0], hose_objects[0] )
    cmds.parent( emit[0], object )
    
    part_attrs = {'depthSort':True, 'particleRenderType':0}
    
    for attr, value in part_attrs.items():
        cmds.setAttr('%s.%s' %(part[1], attr), value)
    
    return emit, part

# Research random.

def random_cube_emit(object, emit_name, sq=1, qt=1, dx=0, dy=1, dz=0, rate=100, sp=0.17, spd=5):
    # Get cube vita
    # Get the current position of the cube
    # cube_trans = cmds.xform(object, a=1, ws=1, t=True)
    cube_scale = cmds.xform(object, q=1, scale=True)
    # Cube dimensions
    cube_di = sq * .5

    # How many particles
    # Loop though how many quantity
    for i in xrange(qt):
        # Generate random range
        transX = random.uniform(-cube_di, cube_di) * cube_scale[0]
        transY = random.uniform(-cube_di, cube_di) * cube_scale[1]
        transZ = random.uniform(-cube_di, cube_di) * cube_scale[2]
        print cube_di, transX, transY, transZ
        
        emitA = my_emitter(object, emit_name, offset=[transX, transY, transZ], dx=0, dy=1, dz=0, rate=100, sp=0.17, spd=5)    
    
    # I need to create an expression

"""
import maya.mel as mel
line = '''
    sphere -n "%s";\n
    xform -t 0 1 0;''' % ('sphName')
mel.eval(line)

import mec_emit
reload(mec_emit)

selected = cmds.ls(sl=True)
mec_emit.random_cube_emit(selected[0], 'sprink')

emit1 = mec_emit.my_emitter(selected[0], 'sprink', offset=[0, 1, 0])

emit2 = mec_emit.my_emitter(selected[1], 'sprink')
emit3 = mec_emit.my_emitter(selected[2], 'sprink')

max_value = 10
# random_value = max_value * random.random()
obj1 = cmds.sphere()
cmds.xform(obj1[0], a=1, ws=1, t=[random.uniform(-max_value, max_value), random.uniform(-max_value, max_value), random.uniform(-max_value, max_value)])
'''
obj2 = cmds.sphere()
cmds.xform(obj2[0], a=1, ws=1, t=[])
obj3 = cmds.sphere()
cmds.xform(obj3[0], a=1, ws=1, t=[])
'''
emitA = mec_emit.my_emitter(obj1[0], 'sprink')
'''
emitB = mec_emit.my_emitter(obj2[0], 'sprink')
emitC = mec_emit.my_emitter(obj3[0], 'sprink')
'''
import random
random.randrange(0, 101, 3)
random.random()
"""