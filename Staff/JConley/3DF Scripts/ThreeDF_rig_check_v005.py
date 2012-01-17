'''ThreeDF Rig Checking Scripts 


import ThreeDF_rig_check
reload(ThreeDF_rig_check)
ThreeDF_rig_check.gui()

'''

import maya.cmds as cmds
import pymel.core as pm
import math
print '3DF Rig Checking Scripts'

# inheritance
# super
# class Frame_Search_Widget(Frame_Widget)
class Frame_Widget():
    def __init__(self, name, objs, parent, width=200, scrollHeight=180, bg_color=[1,0,0]):
        self.width=width
        self.objs = objs
        self.main = cmds.frameLayout(label='%s - %s' % (name, len(objs)), width=width, cll=True, cl=1, bgc=bg_color)
        if not objs:
            cmds.frameLayout(self.main, e=1, cl=1, bgc=[0.5, 0.5, 0.5])
        self.dyna = cmds.scrollLayout(h=scrollHeight)
        self.col = None
        self.gen_button()
        cmds.button(l='Reload', w=width, c=self.gen_button, parent=self.main)
        cmds.setParent(parent)
    
    def gen_button(self, *args):
        if self.col != None:
            cmds.deleteUI(self.col)
        self.col = cmds.columnLayout(co=['both', 5], parent=self.dyna)
        # Loop through given objects.
        for obj in self.objs:
            cmds.nodeIconButton( p=self.col, w=self.width - 40, style='iconAndTextHorizontal', image1='cone.png', label=obj, c=pm.Callback(self.select_obj, obj) )
            # cmds.nodeIconButton( style='iconAndTextHorizontal', command='cmds.spotLight()', image1='spotlight.png', label='Spot Light' )
        
        
    def select_obj(self, obj):
        cmds.select(obj, r=1)

def gui():
    cmds.window()
    # main = cmds.rowColumnLayout(nc=2, cw=[[1, 200], [2,200]])
    main = cmds.columnLayout()
    frm1 = Frame_Widget('Joint Naming - Invalid', check_joint_naming(cmds.ls(typ='joint')), main)
    frm2 = Frame_Widget('Joint Rotations - Invalid', check_joint_rotates(cmds.ls(typ='joint')), main)
    frm3 = Frame_Widget('Joint Translates - Warning', check_joint_translates(cmds.ls(typ='joint')), main, bg_color=[1, 1, 0])
    #frm4 = Frame_Widget('Joint Orientaiton - Invalid', check_joint_orient(cmds.ls(typ='joint')), main)
    
    
    frm5 = Frame_Widget('Curve Naming - Invalid', check_curve_naming(cmds.ls('*nurbs*')), main)
    frm6 = Frame_Widget('Curve Transforms - Invalid', check_curve_transforms(cmds.ls(typ='nurbsCurve')), main)
    frm7 = Frame_Widget('Curve History - Invalid', check_curve_hist(cmds.ls(typ='nurbsCurve')), main)
    
    frm8 = Frame_Widget('Geo Naming- Invalid', check_geo_naming(cmds.ls('*polySurface*')), main)
    #frm9 = Frame_Widget('Geo Transforms - Invalid', check_geo_transforms(cmds.ls(typ='nurbsCurve')), main)
    #frm10 = Frame_Widget('Geo History - Invalid', check_geo_hist(cmds.ls(typ='nurbsCurve')), main)    
    
    cmds.showWindow()
    



def check_joint_naming(objects):
    '''
    Check to make sure all joints are named.
    '''
    
    invalid = []
    numCheck = len(objects)
    for obj in objects:
        num = 0
        while numCheck > num:
            if obj == ('%s%s' % ('joint', num)):
                invalid.append(obj)
                break
            else:
                num += 1
    
    return invalid


def check_joint_orient(objects):
    '''
    Check to insure X is doing down the bone chain.
    '''
    
    invalid = []
    for obj in objects:
        'check orientation'
        'if invalid append to invalid list'
        #invalid.append(obj)
        #break
    
    return invalid


def check_joint_translates(objects):
    '''
    Child joints should only have translation values in X.
    '''
    
    invalid = []
    attrs = ['ty', 'tz']
    for obj in objects:
        for attr in attrs:
            ty = cmds.getAttr('%s.%s' % (obj, attr)) # This should be True
            tz = cmds.getAttr('%s.%s' % (obj, attr)) # This should be True
            
            if ty > math.fabs(.0001) or tz > math.fabs(.0001):
                # This is invalid
                invalid.append(obj)
                break
    
    return invalid


def check_joint_rotates(objects):
    '''
    Check joints to insure they have no rotation values.
    '''
    
    invalid = []
    attrs = ['rx', 'ry', 'rz']
    for obj in objects:
        for attr in attrs:
            rx = cmds.getAttr('%s.%s' % (obj, attr)) # This should be False
            ry = cmds.getAttr('%s.%s' % (obj, attr)) # This should be True
            rz = cmds.getAttr('%s.%s' % (obj, attr)) # This should be True
            
            if rx > math.fabs(.0001) or ry > math.fabs(.0001) or rz > math.fabs(.0001):
                # This is invalid
                invalid.append(obj)
                break
    
    return invalid



def check_curve_naming(objects):
    '''
    Check to make sure all controls are named.
    '''
    
    invalid = []

    shapes = cmds.filterExpand(objects, sm=9)
    cmds.select(shapes)
    new_list = cmds.pickWalk(d='up')
    for obj in new_list:
        invalid.append(obj)
    
    return invalid


def check_curve_transforms(objects):
    '''
    Check joints to insure they have no rotation values.
    '''
    
    invalid = []
    cmds.select(objects)
    new_objects = cmds.pickWalk(d='up')
    transforms = ['t', 'r', 's']
    axis = ['x', 'y', 'z']   

    for obj in new_objects:
        #check translates rotates and scales
        for trans in transforms:
            #check each axis
            for ax in axis:
                attribute = cmds.getAttr('%s.%s%s' % (obj, trans, ax))
                
                if attribute != 0:
                    invalid.append(obj)
                    break
          
    return invalid


def check_curve_hist(objects):
    '''
    Check so see if controls have construction history on them.
    '''
    
    invalid = []
    
    shapes = cmds.filterExpand(objects, sm=9)
    cmds.select(shapes)
    new_list = cmds.pickWalk(d='up')
    print new_list
    hist = []


        
    return invalid
        #check history
        #if it has history append to invalid list
    
def check_geo_naming(objects):
    '''
    Checks to make sure all geometry is named.
    '''
    
    invalid = []
    
    geo = cmds.filterExpand(objects, sm=12)

    #for obj in geo:
     #   invalid.append(obj)
    
    return invalid
        






