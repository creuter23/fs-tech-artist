'''
trying to create a module with enough 'stuff'
for an IK / FK autothingymagig
'''

import maya.cmds as cmds
import maya.mel as mel




# performs a search and replace for a list of objects
# first arguement= list, second arguement= what to search for, third arguement= what tot replace with
def replaceFunction(List=[], old='', new=''):
    # function to replace names
    #cmds.rename(name, newname)
    j=0
    x=len(List)
    
    while j != x:
        new=List[j].split('|')
        newname=new[-1].replace(old, new)
        cmds.rename(new[-1], newname)
        j=j+1
        return newname
    

# adds a suffix for every object in the given list
def suffixFunction(List=[], suffix=''):
    # function to replace names
    #cmds.rename(name, newname)
    j=0
    x=len(List)
    newList=[]
    
    while j != x:
        new=List[j].split('|')
        newname=new[-1]+ suffix
        i=cmds.rename(new[-1], newname)
        newList.append(i)
        j=j+1
    
    return newList



# renames a list based on another list both list should be equal
# example rename duplicated joints to have the same has their parent after their parents have been renamed so the bind, ik, fk joints have the same base name
def renameListFunction(List=[], name=[]):
    # function to replace names
    #cmds.rename(name, newname)
    j=0
    x=len(List)
    newList=[]
    
    while j != x:
        new=List[j].split('|')
        newname=name[j].split('|')
      
        i=cmds.rename(new[-1], newname[-1])
        newList.append(i)
        j=j+1
    
    return newList
        
        
    
        

# creates a blender node  recieves 4 args
# name = name of the node
# fk= fist input, ik= second input, child = what the output will go to
# side note When Blender is 1, the Output is set to Color 1. When Blender is 0, Output is set to Color 2.
# so when blender is one fk is control and when 0 ik is in control

# rotations
def blendR(name, fk, ik, child):
    cmds.shadingNode( 'blendColors', n=name, au=True)
    cmds.connectAttr( '%s.rotate' % fk , '%s.color1' % name)
    cmds.connectAttr( '%s.rotate' % ik , '%s.color2' % name)
    cmds.connectAttr('%s.output' % name, '%s.rotate' % child)
    cmds.setAttr('%s.blender' % name, 0)
    return name
    
# translations
def blendT(name, fk, ik, child):
    cmds.shadingNode( 'blendColors', n=name, au=True)
    cmds.connectAttr( '%s.translate' % fk , '%s.color1' % name)
    cmds.connectAttr( '%s.translate' % ik , '%s.color2' % name)
    cmds.connectAttr('%s.output' % name, '%s.translate' % child)
    cmds.setAttr('%s.blender' % name, 0)
    return name

# scalations
def blendS(name, fk, ik, child):
    cmds.shadingNode( 'blendColors', n=name, au=True)
    cmds.connectAttr( '%s.scale' % fk , '%s.color1' % name)
    cmds.connectAttr( '%s.scale' % ik , '%s.color2' % name)
    cmds.connectAttr('%s.output' % name, '%s.scale' % child)
    cmds.setAttr('%s.blender' % name, 0)
    return name

# creates a setRange node to control the interpolation of the Blender node ^^^^
# receives name, driver, child
# name= name of the node, driver= the icon which will drive the swith(icon must have and attribute name IK_FK) child= blender node
def switchNode(name, driver, child ):
    cmds.shadingNode( 'setRange', n=name, au=True)
    cmds.setAttr('%s.oldMinX' % name, 0)
    cmds.setAttr('%s.oldMaxX' % name, 10)
    cmds.setAttr('%s.minX' % name, 0)
    cmds.setAttr('%s.maxX' % name, 1)
    cmds.connectAttr('%s.IK_FK' % driver , '%s.valueX' % name)
    cmds.connectAttr('%s.outValueX' % name, '%s.blender' % child)
    return name

# lock and hide Rotates
def lockandhideR(object):
    cmds.setAttr("%s.rx" % object, lock=True, keyable=False, channelBox=False)
    cmds.setAttr("%s.ry" % object, lock=True, keyable=False, channelBox=False)
    cmds.setAttr("%s.rz" % object, lock=True, keyable=False, channelBox=False)
    
# lock and hide Translates
def lockandhideT(object):
    cmds.setAttr("%s.tx" % object, lock=True, keyable=False, channelBox=False)
    cmds.setAttr("%s.ty" % object, lock=True, keyable=False, channelBox=False)
    cmds.setAttr("%s.tz" % object, lock=True, keyable=False, channelBox=False)

# lock and hide Scales    
def lockandhideS(object):
    cmds.setAttr("%s.sx" % object, lock=True, keyable=False, channelBox=False)
    cmds.setAttr("%s.sy" % object, lock=True, keyable=False, channelBox=False)
    cmds.setAttr("%s.sz" % object, lock=True, keyable=False, channelBox=False)

# lock and hide All
def lockandhideALL(object):
    cmds.setAttr("%s.tx" % object, lock=True, keyable=False, channelBox=False)
    cmds.setAttr("%s.ty" % object, lock=True, keyable=False, channelBox=False)
    cmds.setAttr("%s.tz" % object, lock=True, keyable=False, channelBox=False)
    
    cmds.setAttr("%s.rx" % object, lock=True, keyable=False, channelBox=False)
    cmds.setAttr("%s.ry" % object, lock=True, keyable=False, channelBox=False)
    cmds.setAttr("%s.rz" % object, lock=True, keyable=False, channelBox=False)
    
    cmds.setAttr("%s.sx" % object, lock=True, keyable=False, channelBox=False)
    cmds.setAttr("%s.sy" % object, lock=True, keyable=False, channelBox=False)
    cmds.setAttr("%s.sz" % object, lock=True, keyable=False, channelBox=False)
    
    cmds.setAttr("%s.visibility" % object, lock=True, keyable=False, channelBox=False)

# lock and hide Viz
def lockandhideV(object):
    cmds.setAttr("%s.visibility" % object, lock=True, keyable=False, channelBox=False)
    

# viz switch
# creates a condition node to control the visibility of ik/fk icons
# name= name of the node
# icon= driver icon which has an attribute specificaly named IK_FK
# fk= group with all fk icons
# ik= group with all ik icons
def visSwitch(name, icon, fk, ik):
    node=cmds.shadingNode( 'condition', n='%s_node' % name, au=True)
    cmds.connectAttr('%s.IK_FK'% icon,'%s.firstTerm' % node )
    cmds.setAttr('%s.operation' % node, 3 ) 
    cmds.setAttr('%s.secondTerm' % node, 5)
    cmds.setAttr('%s.colorIfTrueG' % node, 1)
    cmds.setAttr('%s.colorIfFalseG' % node, 0)
    cmds.setAttr('%s.colorIfTrueR' % node, 0)
    cmds.setAttr('%s.colorIfFalseR' % node, 1)
    cmds.connectAttr('%s.outColor.outColorR' % node,'%s.visibility' % ik)
    cmds.connectAttr('%s.outColor.outColorG' % node,'%s.visibility'% fk)
    
    

    
    
    
    


        
    
    
