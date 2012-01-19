"""
Tobias Jereth Melville
Melville_Tobias_RBA_1201_finalToolSet.py
RBA 1201
Project 2: ToolSet

Description:
    Final toolset with functionality
How to run:

import Melville_Tobias_RBA_1201_finalToolSet
reload(Melville_Tobias_RBA_1201_finalToolSet)
Melville_Tobias_RBA_1201_finalToolSet.gui()
"""
import maya.cmds as cmds
print("Toolset Interface")


def gui():
    if(cmds.window('tjmToolSetMain',ex=True)):
        cmds.deleteUI('tjmToolSetMain', window=True)
    if(cmds.windowPref('tjmToolSetMain', ex=True, )):
        cmds.windowPref('tjmToolSetMain', r=True)
        
    cmds.window('tjmToolSetMain', t="RBA ToolSet", w=305, h=600, s=True, tlc=[107,58])
    cmds.scrollLayout(w=305)
    main = cmds.columnLayout(adjustableColumn=1)
    
    #Modeling
    global normalSize, borderEdgeSize
    cmds.frameLayout('Modeling',l='Modeling', cl=True, cll=True, width=275)
    cmds.columnLayout(adj=1)
    cmds.button(l='Normals',c=normals)
    normalSize=cmds.floatSliderGrp(min=0.0, max=1.0, s=0.01, f=True,dc=normalResize)
    cmds.button(l='Border Edges', c=borderEdge)
    borderEdgeSize=cmds.floatSliderGrp(min=1.0, max=10, s=0.5, f=True, dc=borderEdgeResize)
    cmds.separator( h=5, st='singleDash')
    cmds.text(l='Normals')
    cmds.button(l='Conform', c=conformNormals)
    cmds.button(l='Reverse',c=reverseNormals)
    cmds.button(l='Soften', c=softenNormals)
    cmds.button(l='Harden', c=hardenNormals)
    cmds.setParent(main)
    
    #Control Icons
    cmds.frameLayout('ControlIcons',l='Control Icons', cl=True, cll=True, width=275)
    cmds.columnLayout(adj=1)
    cmds.button(l='Circle', c=createCircle)
    cmds.button(l='Square', c=createSquare)
    cmds.button(l='Cube',c=createCube)
    cmds.button(l='Pointer', c=createPointer)
    cmds.button(l='COG', c=createCOG)
    
    cmds.rowColumnLayout(numberOfColumns=2, width=275)
    global colorIndexValue
    cmds.button(bgc=[1,0,0], c=colorRed, l='')
    cmds.button(bgc=[0,0,1], c=colorBlue, l='')
    cmds.button(bgc=[1,1,0], c=colorYellow, l='')
    cmds.button(bgc=[1,0,1], c=colorPurple, l='')
    cmds.setParent('..')
    cmds.rowColumnLayout(nc=1)
    colorIndexValue=cmds.colorIndexSliderGrp(l=' ', min=0, max=20, value=10,dc=applyColor)
    #cmds.button(l='Apply', c=applyColor)
    cmds.setParent(main)
    
    #Rigging
    global pointCheckBox, orientCheckBox, parentCheckBox
    cmds.frameLayout('Rigging',l='Rigging', cl=True, cll=True, width=275)
    cmds.columnLayout(adj=1)
    cmds.text(l='Constraints')
    pointCheckBox=cmds.checkBox( l='Offset')
    cmds.button(l='Point', c=constraintPoint)
    orientCheckBox=cmds.checkBox( l='Offset')
    cmds.button(l='Orient', c=constraintOrient)
    parentCheckBox=cmds.checkBox( l='Offset')
    cmds.button(l='Parent',c=constraintParent)
    cmds.button(l='Pole Vector', c=constraintPoleVector)
    cmds.separator( height=5, style='singleDash')
    cmds.setParent(main)
    
    #Attribute Creator
    global separatorText, intText, floatText
    cmds.frameLayout('AttributeCreator',l='Attribute Creator',cl=True,cll=True,width=275,)
    cmds.columnLayout(adj=1)
    cmds.rowColumnLayout(nc=2)
    cmds.button(l='Separator',c=createSeparator)
    separatorText=cmds.textField(ed=True)
    cmds.button(l='Int',c=createInt)
    intText=cmds.textField(ed=True)
    cmds.button(l='Float',c=createFloat)
    floatText=cmds.textField(ed=True)
    cmds.setParent('..')
    
    
    #Intermediate Attribute Creator WIP
    cmds.text(l='Custom Attribute', al='center')
    global attributeLongName, radioSelection, minValue, maxValue
    cmds.columnLayout('radioMenu',cal='left', w=275)
    attributeLongName=cmds.textFieldGrp(l='LongName',ed=True, w=250)
    radioSelection=cmds.radioButtonGrp(la2=['Integer', 'Float'], nrb=2,sl=1)
    minValue=cmds.floatFieldGrp(nf=1,l='Min',v1=0)
    maxValue=cmds.floatFieldGrp(nf=1,l='Max',v1=1)
    cmds.setParent('..')
    cmds.button(l='Create Attribute',c=createAttribute)
    cmds.setParent(main)
    
    
    #Clean-Up
    cmds.frameLayout('CleanUp',l='Clean Up', cl=True, cll=True, width=275)
    cmds.columnLayout(adj=1)
    cmds.text(l='Geo')
    cmds.separator( h=5, st='singleDash')
    cmds.button(l='Delete History', c=deleteHistory)
    cmds.button(l='Freeze Transforms', c=freezeTransforms)
    cmds.button(l='Center Pivot', c=centerPivot)
    
    cmds.showWindow('tjmToolSetMain')
    


#Modeling -----------------------------

#Toggles the normals on and off
def normals(*args):
    if(cmds.polyOptions(q=True, dn=True)[0]):
        cmds.polyOptions(dn=False)
        print'Normals Off'
    else:
        cmds.polyOptions(dn=True)
        print'Normals On'

#Resizes the normals      
def normalResize(*args):
    normalResizer=cmds.floatSliderGrp(normalSize,q=True, v=True)
    cmds.polyOptions(sn=normalResizer)
    
#Toggles Border Edge    
def borderEdge(*args):
    if(cmds.polyOptions(q=True, db=True)[0]):
        cmds.polyOptions(db=False)
        print'Border Edges Off'
    else:
        cmds.polyOptions(db=True)
        print'Border Edges On'
    
#Resizes the border edge    
def borderEdgeResize(*args):
    borderEdgeResizer=cmds.floatSliderGrp(borderEdgeSize, q=True, v=True)
    cmds.polyOptions(sb=borderEdgeResizer)
    
#Reverses the selected normals    
def reverseNormals(*args):
    cmds.polyNormal(nm=3)
    print'Reversing Normal(s)'
    
#Conforms the selected normals   
def conformNormals(*args):
    cmds.polyNormal(nm=2)
    print'Conforming Normals'
    
#Soften normal values setting the angle to 180
def softenNormals(*args):
    cmds.polySoftEdge(a=180, ch=True)
    print 'Soften Normals Edges'
    
#Hardens normal values setting the angle to 0    
def hardenNormals(*args):
    cmds.polySoftEdge(a=0, ch=True)
    print 'Harden Normals Edges'

#Control Icons ------------------------
#Creats a nurb circle
def createCircle(*args):
    cmds.circle(nr=(0,1,0),s=8,r=2)
    print 'Created a Nurbs Circle'

#Creates a CV Curve Square    
def createSquare(*args):
    cmds.curve(d=1,p=[(0.5,0,0.5), (-0.5,0,0.5), 
    (-0.5,0,-0.5),(0.5,0,-0.5),(0.5,0,0.5)],
    k=[0,1,2,3,4],per=True)
    cmds.scale(2.458224,2.459224,2.459224,r=True)
    cmds.select(cl=True)
    print 'Created a Nurbs Square'

#Creates a CV Curve Cube
def createCube(*args):
    cmds.curve(d=1, p=[ (0.5, 0.126219, -0.5), (0.5, 0.126219, 0.5) ,(0.5, 1.126219, 0.5), (0.5, 1.126219, -0.5),
                       (0.5, 0.126219, -0.5) ,(-0.5, 0.126219, -0.5) ,(-0.5, 1.126219, -0.5) ,(0.5, 1.126219, -0.5),
                       (-0.5, 1.126219, -0.5) ,(-0.5, 1.126219, 0.5) ,(-0.5, 0.126219, 0.5) ,(-0.5, 0.126219, -0.5),
                       (-0.5, 1.126219, -0.5), (-0.5, 1.126219, 0.5) ,(0.5, 1.126219, 0.5) ,(0.5, 0.126219, 0.5),
                       (-0.5, 0.126219, 0.5)], k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
    cmds.CenterPivot()
    cmds.select(cl=True)

    print 'Created a Solid Nurbs Cube'
#Creates a Pointer    
def createPointer(*args):
    cmds.circle(nr=(0,1,0),s=8,r=2)
    cmds.move(0,0,3.740932,'.cv[5]', r=True)
    cmds.scale(0.523749,1,1,'.cv[4]','.cv[6]', p=(0,0,1.567223),r=True)
    cmds.scale(0.786803,1,1,'.cv[3]','.cv[7]',p=(0,0,0), r=True)
    cmds.scale(0.382332, 0.382332, 0.382332, r=True)
    cmds.select(cl=True)
    print 'Created a Nurbs Pointer'
    
#Creates a Center of Gravity    
def createCOG(*args):
    cmds.circle(nr=(0,1,0),s=16, r=2)
    cmds.scale(0.177161, 0.177161, 0.177161,'.cv[15]','.cv[13]','.cv[11]','.cv[9]','.cv[7]',
                '.cv[5]','.cv[3]','.cv[1]',r=True)
    cmds.scale(1.848257, 1.848257, 1.848257, r=True)
    cmds.select(cl=True)
    print 'Created a COG'
#Sets the selected nurbs Display Override Color to selected color from the color slider   
def applyColor(*args):
    colorIndex = cmds.colorIndexSliderGrp(colorIndexValue,q=True,value=True)
    selected = cmds.ls(sl=True)
    for sel in selected:
        cmds.setAttr(sel+".overrideEnabled",1)
        #the colorIndex-1 sets up so that the color value is taken correct
        cmds.setAttr(sel+".overrideColor",colorIndex-1)
    
#Sets the selected nurbss Display Override Color to Red
def colorRed(*args):
    selected = cmds.ls(sl=True)
    for sel in selected:
        print sel
        cmds.setAttr(sel + ".overrideEnabled",1)
        cmds.setAttr(sel + ".overrideColor",13)
        print'Color set to Red'

#Sets the selected nurbs Display Override Color to Blue        
def colorBlue(*args):
    selected = cmds.ls(sl=True)
    for sel in selected:
        print sel
        cmds.setAttr(sel + ".overrideEnabled",1)
        cmds.setAttr(sel + ".overrideColor",6)
    print 'Color set to Blue'

#Sets the selected nurbs Display Override Color to Yellow   
def colorYellow(*args):
    selected = cmds.ls(sl=True)
    for sel in selected:
        print sel
        cmds.setAttr(sel + ".overrideEnabled",1)
        cmds.setAttr(sel + ".overrideColor",17)
    print'Color set to Yellow'

#Sets the selected nurbs Display Override Color to Purple
def colorPurple(*args):
    selected = cmds.ls(sl=True)
    for sel in selected:
        print sel
        cmds.setAttr(sel + ".overrideEnabled",1)
        cmds.setAttr(sel + ".overrideColor",9)
    print'Color Set to Purple'
#Rigging ------------------------
#Constrains a point to another object
def constraintPoint(*args):
    pointCheckBoxInquiry=cmds.checkBox(pointCheckBox,q=True,v=True)
    cmds.pointConstraint(w=1.0, mo=pointCheckBoxInquiry)
    print 'Constrain Point'

#Constrains orients of joints to roots
def constraintOrient(*args):
    orientCheckBoxInquiry=cmds.checkBox(orientCheckBox,q=True,v=True)
    cmds.orientConstraint(w=1.0, mo=orientCheckBoxInquiry)
    print 'Constrain Orient'

#Constrains objects to a parent
def constraintParent(*args):
    parentCheckBoxInquiry=cmds.checkBox(parentCheckBox,q=True,v=True)
    cmds.ParentConstraint(w=1.0, mo=parentCheckBoxInquiry)
    print 'Constrain Parent'

#Constrains a nurb to an IKHandle with a IKRPSolver    
def constraintPoleVector(*args):
    cmds.poleVectorConstraint(w=1.0)
    print 'Constrain Pole Vector'
    
#Attribute Creator---------------------

#Creates an enum attribute with the name from the text field above
def createSeparator(*args):
    separatorName=cmds.textField(separatorText, q=True, tx=True)
    selected=cmds.ls(sl=True)
    for sel in selected:
        cmds.addAttr(sel, ln=separatorName, at='enum',en='-------------------------------------------')
        cmds.setAttr(sel + '.' + separatorName, e=True,keyable=True)
    print'create Separator'
    
#Creates an integer attribute with the name from the text field above
def createInt(*args):
    intName=cmds.textField(intText,q=True,tx=True)
    selected=cmds.ls(sl=True)
    for sel in selected:
        cmds.addAttr(sel,ln=intName,at='long', min=-10,max=10)
        cmds.setAttr(sel + '.' + intName,e=True,keyable=True)
    print'create Int'

#Creates a float attribute with the name from the text field above
def createFloat(*args):
    floatName=cmds.textField(floatText,q=True,tx=True)
    selected=cmds.ls(sl=True)
    for sel in selected:
        cmds.addAttr(sel,ln=floatName,at='double',min=-10.0,max=10.0)
        cmds.setAttr(sel + '.' + floatName, e=True, keyable=True)
    print'create Float'

#Intermediate Attribute Creator WIP
def createAttribute_gui(*args):
    longName=cmds.textFieldGrp(attributeLongName,q=True,tx=True)
    minValueSetting=cmds.floatFieldGrp(minValue,q=True,v1=True)
    maxValueSetting=cmds.floatFieldGrp(maxValue,q=True,v1=True)
    radioSelected=cmds.radioButtonGrp(radioSelection,q=True, sl=True)
    radioSelect='double'
    
    if(radioSelected ==1):
        radioSelect='long'
        minValueSetting = int(minValueSetting)
        maxValueSetting = int(maxValueSetting)
   
    selected=cmds.ls(sl=True)
    createAttribute(selected, longName, radioSelection, minValueSettings, maxValueSetting, 0)
    '''
    for sel in selected:
        cmds.addAttr(sel,ln=longName, at=radioSelect,min=minValueSetting, max=maxValueSetting, dv=0, k=1)
        # cmds.setAttr(sel + '.' + longName, e=True, keyable=True,)
        print'Creates an Attribute'
    '''

def createAttribute(objs, long_name, attr_type='double', min=-10, max=10, dv=0):
    for obj in objects:
        cmds.addAttr(obj,ln=long_name, at=attr_type, min=min, max=max, dv=dv, k=1)

def create_fingers_gui(*args):
    print 'Fingers Created'
    selected = cmds.ls(sl=True)
    createFinger(selected)
    
def createFinger(objs):
    fingers = ['index_curl', 'middle_curl', 'ring_curl', 'pinky_curl', 'thumb_curl']
    for obj in objs:
        # Overall Separator
        
        # Creating finger attributes
        for finger in fingers:
            createAttribute(obj, finger)
#Clean Up ------------------------------
#Deletes history of the selected object
def deleteHistory(*args):
    #cmds.DeleteHistory()
    cmds.delete(ch=True)
    print 'History Deleted'

#Freezes the Transforms of the selected object
def freezeTransforms(*args):
    cmds.makeIdentity(t=True,r=True,s=True,a=True)
    print 'Tranforms Frozen'
    
#Centers the Pivot of the selected object
def centerPivot(*args):
    #cmds.CenterPivot()
    cmds.xform(ztp=True)
    print 'Pivot Centered'
    
