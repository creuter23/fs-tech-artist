emitter -pos 0 0 0 -type omni  -name "emit1#" -r 100 -sro 0 -nuv 0 -cye none -cyi 1
    -spd 1 -srn 0 -nsp 1 -tsp 0 -mxd 0 -mnd 0 -dx 1 -dy 0 -dz 0 -sp 0 ;
// Result: emit11 // 
particle;
// Result: particle1 particleShape1 // 
connectDynamic -em emit11 particle1;
// Result: particleShape1 // 


import maya.cmds as cmds
# cye=none???
myEmitter_name = 'myEmit'
myParticle_name = 'par1'
emit_obj = cmds.emitter(name=myEmitter_name, pos=[0, 0, 0], type='omni', r=100, sro=0, nuv=0, cye='none', spd=1, srn=0,
             nsp=1, tsp=0, mnd=0, dx=1, dy=0, dz=0, sp=0)

part_obj = cmds.particle(name=myParticle_name)

cmds.connectDynamic(part_obj[0], em=emit_obj[0])

# Create emitters
def create_emit(myEmitter_name, current_rate=100):
    emit_obj = cmds.emitter(name=myEmitter_name, pos=[0, 0, 0], type='omni', r=current_rate, sro=0, nuv=0, cye='none', spd=1, srn=0,
             nsp=1, tsp=0, mnd=0, dx=1, dy=0, dz=0, sp=0)

    part_obj = cmds.particle(name=emit_obj[0] + '_part')
    
    cmds.connectDynamic(part_obj[0], em=emit_obj[0])
    return [emit_obj[0], part_obj[0], part_obj[1]]

emit1 = create_emit('myEmit1', 1000)
cmds.setAttr(emit1[0] + '.rate', 10000)
emit2 = create_emit('myEmit2')
cmds.setAttr(emit1[0] + '.rate', 1000)
emit3 = create_emit('myEmit3')
cmds.setAttr(emit1[0] + '.rate', 100)
emit4 = create_emit('myEmit4')
cmds.setAttr(emit1[0] + '.rate', 10)
emit5 = create_emit('myEmit5')

# Changing settings
# getattr and setattr
# setAttr "myEmit4.rate" 1000;
# getAttr "myEmit4.rate" 1000;
# getAttr "objectName.attributeName"
cmds.setAttr('myEmit4.rate', 1000)

# xform command
# ls
#    cmds.ls(sl=True)