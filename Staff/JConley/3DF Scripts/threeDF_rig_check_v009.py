'''
Author: Jennifer Conley
Date Modified: 1/11/12

How to run:
import threeDF_script
reload (threeDF_script)
threeDF_script.gui()

'''

import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import math

joint_naming = ['Custom', 'Good. ', 'Bad. ', 'Alright. ']
joint_rotates = ['Custom','Rotates not frozen. ', 'Some rotates not frozen. ', 'Good job. ']
grade_list1 = {'A':100, 'F':0}
grade_list2 = {'A':100, 'B':90, 'C':80, 'D':70, 'F':60}


class Widget_One():
    def __init__(self, objs, width=200):
        self.width=width
        self.objs = objs
        self.mainCol = cmds.columnLayout()
        self.dyna = cmds.scrollLayout()
        self.col = None
        self.gen_button()
        cmds.button(l='Reload', w=width, c=self.gen_button)


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


class Widget_Two():
    def __init__(self, comments, pf):
        self.grade = []      
        self.comments = comments
        self.pf = pf
        main = cmds.columnLayout()
        self.widget2_main = cmds.columnLayout()
        self.grade_buttons()
        cmds.rowColumnLayout(nc=2)
        cmds.text(l='Grade')
        self.grade_field = cmds.floatField(v=0.00)
        cmds.setParent(self.widget2_main)
        self.mainScroll = cmds.scrollField(ww=True)
        self.menu_item_comments()
        
    
    def grade_buttons(self, *args):
        '''
        Creates the widget display for the grading buttons 
        '''
        if self.pf == 1:
            cmds.columnLayout()
            cmds.rowColumnLayout(nc=2)
            for grade in sorted(grade_list1):
                cmds.button(l=grade, w=75, c=pm.Callback(self.add_grade, grade ))
                self.grade = grade_list1
            cmds.setParent(self.widget2_main)
        else:
            cmds.columnLayout()
            cmds.rowColumnLayout(nc=5)
            for grade in sorted(grade_list2):
                cmds.button(l=grade, w=40, c=pm.Callback(self.add_grade, grade))
                self.grade = grade_list2
            cmds.setParent(self.widget2_main)
            
      
    def menu_item_comments(self, *args):
        cmds.popupMenu(parent=self.mainScroll)
        for comment in self.comments:
            if comment == 'Custom':
                cmds.menuItem(l=comment, c=self.create_comment)
            else:
                cmds.menuItem(l=comment, c=pm.Callback(self.adding_text, comment))
           
    def adding_text(self, comment):
        cmds.scrollField(self.mainScroll, e=True, it=comment)
    
            
    def create_comment(self, *args):
        cmds.window('comment_win')
        cmds.columnLayout()
        cmds.text(l='Enter in new comment')
        self.new_comment_field = cmds.scrollField()
        add = cmds.button(l='Add', c=self.add_comment)
        cmds.showWindow('comment_win')
        
        
    def add_comment(self, *args):
        self.new_comment = cmds.scrollField(self.new_comment_field, q=True, tx=True)
        print self.comments
        self.comments.append(self.new_comment)
        cmds.deleteUI('comment_win')
        print self.comments
        gui()
        
        
    def add_grade(self, grade):
        cmds.floatField(self.grade_field, e=True, v=self.grade[grade])
        
    

    
class Main_Widget():
    def __init__(self, name, objs, comments, pf, bg_color=[1,0,0]):
        self.mainFrame = cmds.frameLayout(l='%s - %s' % (name, len(objs)), bgc=bg_color, cll=True)
        if not objs:
            cmds.frameLayout(self.mainFrame, e=1, cl=1, bgc=[0.5, 0.5, 0.5])
        rowCol = cmds.rowColumnLayout(nc=2, h=400)
        Widget_One(objs)
        cmds.setParent(rowCol)
        Widget_Two(comments, pf)
        cmds.setParent(self.mainFrame)

def gui():
    '''
    Creats the gui
    '''
    bw=500
    sw=200
    
    win = 'win3DFGrade'
    if (cmds.window(win, ex=True)):
        cmds.deleteUI(win)
    if (cmds.windowPref(win, ex=True)):
        cmds.windowPref(win, r=1)        
    
    cmds.window(win, w=bw, h=400)
    
    
    '''
    Main section of tool
    Displays scene name with button for opening new scene files
    '''    
    top_main = cmds.columnLayout(w=500)
    cmds.rowColumnLayout(w=500, nc=3)
    cmds.text(l='Scene Name', w=133)
    cmds.textField(w=133)
    cmds.button(l='Open Scene', w=133, c=open_scene)
    cmds.setParent(top_main)
    
    '''
    Dislays grading options such as professionalism and late turnin decutions
    '''    
    cmds.rowColumnLayout(w=500, nc=6)
    cmds.text('Professional', w=66)
    cmds.floatField(v=0.00, w=66)
    cmds.text('Late Turnin', w=66)
    cmds.floatField(v=0.00, w=66)
    cmds.text('Total Grade', w=66)
    cmds.floatField(v=0.00, w=66)
    cmds.setParent(top_main)
    
    '''
    Creats Export button
    '''    
    cmds.button(l='Export')
    cmds.setParent(top_main)
    
    '''
    Subsection of tool
    '''
    cmds.columnLayout()
    cmds.scrollLayout()
    bottom_main = cmds.columnLayout()
    
    '''    
    Creates the 'Joint' grading sections
    '''
    cmds.frameLayout(l='Joints', cll=True, w=bw)
    joint_col = cmds.columnLayout()
    main_widget1 = Main_Widget('Joint Naming - Invalid', check_joint_naming(cmds.ls(typ='joint')), joint_naming, pf=0)
    


    cmds.setParent(joint_col)    
    main_widget2 = Main_Widget('Joint Rotations - Invalid', check_joint_rotates(cmds.ls(typ='joint')), joint_rotates, pf=1)
    cmds.setParent(joint_col)
    main_widget3 = Main_Widget('Joint Translates - Warning', check_joint_translates(cmds.ls(typ='joint')), joint_naming, pf=0)
    cmds.setParent(joint_col)    
    #main_widget4 = Main_Widget('Joint Orientaiton - Invalid', check_joint_orient(cmds.ls(typ='joint')), joint_naming, pf=0)
    cmds.setParent(bottom_main)
    
    '''
    Creates the 'Curve' grading sections
    '''
    cmds.frameLayout(l='Curves', cll=True)
    curve_col = cmds.columnLayout()
    main_widget5 = Main_Widget('Curve Naming - Invalid', check_curve_naming(cmds.ls(typ='nurbsCurve')), joint_naming, pf=1)
    cmds.setParent(curve_col) 
    main_widget6 = Main_Widget('Curve Transforms - Invalid', check_transforms(cmds.ls(typ='nurbsCurve')), joint_rotates, pf=1)
    cmds.setParent(curve_col) 
    main_widget7 = Main_Widget('Curve History - Invalid', check_curve_hist(cmds.ls(typ='nurbsCurve')), joint_rotates, pf=1)
    cmds.setParent(bottom_main)
    
    '''    
    Creates the 'Geometry' grading sections
    '''
    cmds.frameLayout(l='Geometry', cll=True)
    geo_col = cmds.columnLayout()
    main_widget8 = Main_Widget('Geo Naming - Invalid', check_geo_naming(cmds.ls(typ='mesh')), joint_naming, pf=0)
    cmds.setParent(geo_col)
    main_widget9 = Main_Widget('Geo Transforms - Invalid', check_transforms(cmds.ls(typ='mesh')), joint_naming, pf=0)
    cmds.setParent(geo_col)
    main_widget10 = Main_Widget('Geo History - Invalid', check_geo_hist(cmds.ls(typ='mesh')), joint_naming, pf=0)    
    cmds.setParent(bottom_main)
    

    
    cmds.showWindow(win)
    
    
    
def open_scene(*args):
    '''    
    Function to open a new scene file and reload the tool
    '''
    mel.eval('OpenScene;')
    import threeDF_script
    threeDF_script.gui()
    
    
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
                invalid.append(obj)
                break
    
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
                invalid.append(obj)
                break
    
    return invalid

def check_curve_naming(objects):
    '''
    Check to make sure all controls are named.
    '''
    
    invalid = []
    
    cmds.select(objects)
    curve_list = cmds.pickWalk(d='up')    
    
    for obj in curve_list:
        if obj.find('nurbs') != -1:
            invalid.append(obj)
    
   
    return invalid


def check_transforms(objects):
    '''
    Check joints to insure they have no rotation values.
    '''
    
    invalid = []
    cmds.select(objects)
    new_objects = cmds.pickWalk(d='up')
    t_r_xform = ['t', 'r']
    scale_xform = 's'
    axis = ['x', 'y', 'z']
    

    for obj in new_objects:
        #check translates rotates and scales
        for trans in t_r_xform:
            #check each axis
            for ax in axis:
                trans_rot = cmds.getAttr('%s.%s%s' % (obj, trans, ax))
                
                if trans_rot != 0:
                    invalid.append(obj)
                    break
                
            for ax in axis:
                scale = cmds.getAttr('%s.%s%s' % (obj, scale_xform, ax))
                
                if scale != 1:
                    invalid.append(obj)
                    break
          
    return invalid


def check_curve_hist(objects):
    '''
    Check so see if controls have construction history on them.
    '''
    
    invalid = []

    cmds.select(objects)
    curve_list = cmds.pickWalk(d='up')

    for each in curve_list:
        hist = cmds.listHistory(each)
        if len(hist) > 1:
            invalid.append(each)
        
    return invalid


def check_geo_naming(objects):
    '''
    Check to make sure all controls are named.
    '''
    
    invalid = []
    
    cmds.select(objects)
    curve_list = cmds.pickWalk(d='up')    
    
    for obj in curve_list:
        if obj.find('poly') != -1:
            invalid.append(obj)
    
   
    return invalid


def check_geo_hist(objects):
    '''
    Checks to make sure all geometry is named.
    '''
    
    invalid = []
    
    cmds.select(objects)
    geo_list = cmds.pickWalk(d='up')

    for each in geo_list:
        hist = cmds.listHistory(each)
        if len(hist) > 3:
            invalid.append(each)
  
    return invalid
  