'''
RBA Checking Scripts 


import rba_check
reload(rba_check)
rba_check.gui()

'''

import maya.cmds as cmds
import pymel.core as pm
import math
print 'RBA Checking Scripts'


# Check naming

# Check rotation on joints.

# Verify Root Systems

# Check Lock and Hidden Channels
def check_lockAndHide(objects):
    '''
    Check to see if controls in the scene have their
    Channels locked and hidden.
    '''
    # Visibilty and scale should be locked and hidden.
    invalid = []
    attrs = ['sx', 'sy', 'sz', 'v']
    for obj in objects:
        for attr in attrs:
            keyable = cmds.getAttr('%s.%s' % (obj, attr), k=1) # This should be False
            locked = cmds.getAttr('%s.%s' % (obj, attr), l=1) # This should be True
            if keyable == True and locked == False:
                # This is invalid
                invalid.append(obj)
                break
    
    return invalid

def check_dupNames(objects):
    '''
    Check for duplicate names
    '''
    print 'dup'
 
def check_proper_names(objects):
    '''
    Check to see if given objects have proper naming conventions.
    '''
    print 'check'
    
def joint_rotations(objects):
    '''
    Check for rotation values.
    '''
    invalid = []
    attrs = ['rx', 'ry', 'rz']
    for obj in objects:
        for attr in attrs:
            rx = cmds.getAttr('%s.%s' % (obj, attr)) # This should be False
            ry = cmds.getAttr('%s.%s' % (obj, attr)) # This should be True
            rz = cmds.getAttr('%s.%s' % (obj, attr)) # This should be True
            
            if rx > math.fabs(0.0001) or ry > math.fabs(0.0001) or rz > math.fabs(0.0001):
                # This is invalid
                invalid.append(obj)
                break
    
    return invalid
    
def check_rotates(objects):
    '''
    Check to see if controls in the scene have their
    Channels locked and hidden.
    '''
    # Visibilty and scale should be locked and hidden.
    invalid = []
    attrs = ['rx', 'ry', 'rz']
    for obj in objects:
        for attr in attrs:
            rx = cmds.getAttr('%s.%s' % (obj, attr)) # This should be False
            ry = cmds.getAttr('%s.%s' % (obj, attr)) # This should be True
            rz = cmds.getAttr('%s.%s' % (obj, attr)) # This should be True
            
            if rx != 0 or ry != 0 or rz != 0:
                # This is invalid
                invalid.append(obj)
                break
    
    return invalid

def check_translates(objects):
    '''
    Check to see if controls in the scene have their
    Channels locked and hidden.
    '''
    # Visibilty and scale should be locked and hidden.
    invalid = []
    attrs = ['tx', 'ty', 'tz']
    for obj in objects:
        for attr in attrs:
            rx = cmds.getAttr('%s.%s' % (obj, attr)) # This should be False
            ry = cmds.getAttr('%s.%s' % (obj, attr)) # This should be True
            rz = cmds.getAttr('%s.%s' % (obj, attr)) # This should be True
            
            if rx != 0 or ry != 0 or rz != 0:
                # This is invalid
                invalid.append(obj)
                break
    
    return invalid

def check_channels(objects, attrs=['tx', 'ty', 'tz', 'rx', 'ry', 'rz']):
    '''
    Check to see if controls in the scene have their
    Channels locked and hidden.
    '''
    # Visibilty and scale should be locked and hidden.
    invalid = []
    for obj in objects:
        for attr in attrs:
            attr_val = cmds.getAttr('%s.%s' % (obj, attr)) # This should be False
            
            if attr_val != 0:
                # This is invalid
                invalid.append(obj)
                break
    
    return invalid

# inheritance
# super
# class Frame_Search_Widget(Frame_Widget)
class Frame_Widget():
    def __init__(self, name, objs, parent, width=200, scrollHeight=180, bg_color=[1,0,0]):
        self.width=width
        self.objs = objs
        self.main = cmds.frameLayout(label='%s - %s' % (name, len(objs)), width=width, cll=True, bgc=bg_color)
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
    frm1 = Frame_Widget('Lock and Hide - Invalid', check_lockAndHide(cmds.ls('*_icon')), main)
    frm2 = Frame_Widget('Freeze Transforms - Invalid', check_channels(cmds.ls('*_icon')), main)
    frm3 = Frame_Widget('Joint Rotations - Warning', joint_rotations(cmds.ls('*_bj')), main, bg_color=[.6, 0, 1])
    
    cmds.showWindow()