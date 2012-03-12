'''
import ikfk
reload(ikfk)
ikfk.gui()


'''

import maya.cmds as cmds
import maya.mel as mel

import fsaIconModule as fsaI
import fsaGeneralModule as fsaG

ikfkwindow='IKFKwindow'

def gui():
    global jointField, suffixField,newBJ, newFK, newIK, Suffix, chain

    if(cmds.window(ikfkwindow, ex=1)):
        cmds.deleteUI(ikfkwindow)
        
    if(cmds.windowPref(ikfkwindow, ex=1)):
        cmds.windowPref(ikfkwindow, remove=1)

    cmds.window(ikfkwindow, title="IK / FK", sizeable=1, mnb=1, width=250, bgc=[.5, .5, .5])
    cmds.columnLayout("mainlayout", adjustableColumn=1)
    cmds.columnLayout( adjustableColumn=True)
    
    cmds.setParent("mainlayout")
    cmds.text(label='Joint Chain')
    jointField=cmds.textFieldButtonGrp( text='Joint', buttonLabel='<<<', bc=loadObject, ed=0 )
    cmds.text(label='Suffix for Bind Joints')
    suffixField=cmds.textField(text='_bj')
    
    cmds.button(label='Make IK/FK', command=ikfkFunction)

    cmds.showWindow()
    
def loadObject(*args):
    x=cmds.ls(sl=1)[0]
    cmds.textFieldButtonGrp(jointField, edit=1, text=x)
    
def ikfkFunction(*args):
    chain=cmds.textFieldButtonGrp(jointField, q=1, text=1)
    Suffix=cmds.textField(suffixField, q=1, text=1)
    cmds.select(chain)
    bj=cmds.ls(sl=1)
    # dulpicating orginal for IK?FK chains
    fk=cmds.duplicate(bj, rr=1, rc=1) # need to rename
    ik=cmds.duplicate(bj, rr=1, rc=1) # need to rename
    
    # grouping objects
    cmds.group(bj, ik, fk, n='%s_mainPad' % bj[0])
    
    
    
    cmds.select(bj, hi=1)
    bjList=cmds.ls(selection=1)
    
    cmds.select(fk, hi=1)
    fkList=cmds.ls(selection=1)
    
    cmds.select(ik, hi=1)
    ikList=cmds.ls(selection=1)
    # adding Suffixes
    newBJ=fsaG.suffixFunction(List= bjList, suffix= '%s' % Suffix)
    
    # renaming the duplicate fk joints based on the orgianl joints 
    fkList=fsaG.renameListFunction(fkList, bjList)
    
    # adding _ FK to fk joints
    newFK=fsaG.suffixFunction(List=fkList, suffix='_FK')
    
    # renaming the duplicated ik joints based on the original joints
    ikList=fsaG.renameListFunction(ikList, bjList)
    
    # adding _IK to the ik joints
    newIK=fsaG.suffixFunction(List=ikList, suffix='_IK')
    
    # using blender nodes to control the binding joints instead of orient costraints
    node001=fsaG.blendR(name='%s_node' % newBJ[0], fk=newFK[0], ik=newIK[0], child=newBJ[0])
    node002=fsaG.blendR(name='%s_node' % newBJ[1], fk=newFK[1], ik=newIK[1], child=newBJ[1])
    
    # getting rid of the underscores / storing newnames in variables in order to name icons properly
    switchName=newBJ[0].replace('%s' % Suffix, '')
    
    # other variables, newFK[0]=root joint, newFK[1]= elbow Joint, newFK[2]= end Joint,samw for iks
    
    fkRoot= newFK[0]
    fkMid=newFK[1]
    
    ikRoot= newIK[0]
    ikMid=newIK[1]
    ikEnd=newIK[2]


    
    # creates an icon that will hold the ik/fk switch
    switch=fsaI.SwitchIKFK(name='%sSwitch_icon' % switchName, position=newBJ[2], size=.5)
    
    # locking and hiding unneeded attrs
    
    # creates two setRange nodes to niterpolate between the blender nodes, 0 is IK FK is 10
    fsaG.switchNode(name='%s_node01' % switchName, driver=switch, child=node001 )
    fsaG.switchNode(name='%s_nod02' % switchName, driver=switch, child=node002 )
    
    # creating fk icons
    fk01=fsaI.circleV(name='%s_icon' % fkRoot, position=fkRoot)
    fk02=fsaI.circleV(name='%s_icon' % fkMid, position=fkMid)
    # padding fk icons
    pad01=fsaI.orientpad(fk01,fkRoot )
    pad02=fsaI.orientpad(fk02,fkMid)
    # parenting fk icons
    cmds.parent(pad02, fk01[0])
    # creating ikHandle
    ikHandle=cmds.ikHandle(n='%s_IK' % ikRoot,sol='ikRPsolver',s='sticky',  sj=ikRoot, ee=ikEnd )
    
    # ik icons
    ikIcon=fsaI.cube(name='%s_icon' % ikRoot, position=ikEnd, size=.75)
    ikPV=fsaI.plusV(name='%sPV_icon' % ikRoot,position=ikMid, size=.25)
    pvline=fsaI.pvLine(name='%sPV_line' % ikRoot, icon=ikPV, joint=newBJ[1])
    
    # parent ikHandle
    cmds.parentConstraint(ikIcon, ikHandle[0], mo=1)
    
    #pole vector constraint
    cmds.poleVectorConstraint(ikPV, ikHandle[0], weight=True)
    
    # grouping ik icons
    
    ikIcons=cmds.group(pvline, ikPV, ikIcon, n='%sicons_pad' % ikRoot)
    
    # cleaning up / locking and hiding attrs
    
    fsaG.lockandhideALL(switch)
    
    # fk icons
    fk001=fk01[0].split(',')
    fk002=fk02[0].split(',')
    fsaG.lockandhideT(fk001[0])
    fsaG.lockandhideS(fk001[0])
    fsaG.lockandhideV(fk001[0])
    fsaG.lockandhideT(fk002[0])
    fsaG.lockandhideS(fk002[0])
    fsaG.lockandhideV(fk002[0])
    
    
    # ik icons
    fsaG.lockandhideR(ikIcon)
    fsaG.lockandhideS(ikIcon)
    fsaG.lockandhideV(ikIcon)
    fsaG.lockandhideR(ikPV)
    fsaG.lockandhideS(ikPV)
    fsaG.lockandhideV(ikPV)
    
    fsaG.visSwitch(name='%sVis' % switch, icon = switch, fk = pad01, ik = ikIcons)
    
    '''
    clean up naming of icons and other things
    '''
