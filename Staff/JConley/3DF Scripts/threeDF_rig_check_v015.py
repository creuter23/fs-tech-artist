'''
Author: Jennifer Conley
Date Modified: 1/13/12

How to run:
import threeDF_script
reload (threeDF_script)
threeDF_script.gui()

'''

import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import math
import com_wid

file_name = 'file_submission.txt'


class Widget_One():
    def __init__(self, objs, width=200):
        self.width=width
        self.objs = objs
        self.mainCol = cmds.columnLayout(w=self.width)
        self.dyna = cmds.scrollLayout()
        self.col = None
        self.gen_button()
        
        
    def reload_button(self, *args):
        if self.col != None:
            cmds.deleteUI(self.col)
            self.gen_button()


    def gen_button(self, *args):
        self.rowCol = []
        self.objsList = []
        self.col = cmds.columnLayout(w=self.width-10, p=self.dyna)
        col = cmds.columnLayout()
        for obj in self.objs:
            new_rowCol = cmds.rowColumnLayout(nc=2, cw=[150, 10], cs=[2,10])
            cmds.nodeIconButton(w=300, style='iconAndTextHorizontal', image1='cone.png', label=obj, c=pm.Callback(self.select_obj, obj) )
            cmds.checkBox(l=' ', w=10, onc=pm.Callback(self.remove_object, obj))
            cmds.setParent(col)
            self.rowCol.append(new_rowCol)
            self.objsList.append(obj)
        cmds.button(l='Reload', c=self.reload_button, p=self.col)
            
        
    def select_obj(self, obj):
        cmds.select(obj, r=1)
        
        
    def remove_object(self, obj):
        remove_num = self.objsList.index(obj)
        cmds.deleteUI(self.rowCol[remove_num])
        self.rowCol.remove(self.rowCol[remove_num])
        self.objsList.remove(self.objsList[remove_num])

        
        


class Widget_Two():
    def __init__(self, objs, comment_file, pf):
        self.grade = []
        self.comment_file = comment_file
        self.pf = pf
        self.obj_len = len(objs)
        main = cmds.columnLayout()
        self.widget2_main = cmds.columnLayout()
        self.grade_buttons()
        cmds.rowColumnLayout(nc=2)
        cmds.text(l='Grade')
        if self.obj_len < 5:
            self.grade_field = cmds.intField(v=100)
        else:
            self.grade_field = cmds.intField(v=0)
            
        cmds.setParent(self.widget2_main)
        
        com_wid.Comment_Widget()

        #self.mainScroll = cmds.scrollField(ww=True, cc=self.post_summery)
        #self.menu_item_comments()

        
    def post_summery(self, *args):
        '''
        Posts comments to the summery tab
        '''
        
        self.query_comments = cmds.scrollField(self.mainScroll, q=True, tx=True)
        
        cmds.scrollField(summery_scroll, e=True, it=self.query_comments + '\n')
        print self.query_comments
    
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
                cmds.button(l=grade, w=40, c=pm.Callback(self.add_grade, grade ))
                self.grade = grade_list2
            cmds.setParent(self.widget2_main)
            
            
            
    def add_grade(self, grade):
        cmds.intField(self.grade_field, e=True, v=self.grade[grade])
            
      
           
    def adding_text(self, comment):
        '''
        Adds comments to the scrollField
        '''
        
        cmds.scrollField(self.mainScroll, e=True, it=comment)
    
            
    def create_comment(self, *args):
        '''
        Creats the gui for the 'Custom' comment window
        '''
        
        global win_name
        win_name = 'comment_win'
        
        if (cmds.window(win_name, ex=True)):
            cmds.deleteUI(win_name)
        if (cmds.windowPref(win_name, ex=True)):
            cmds.windowPref(win_name, r=1)
            
        cmds.window(win_name)
        cmds.columnLayout()
        cmds.rowColumnLayout(nc=2)
        cmds.text(l='Comment Lable')
        self.new_lableField = cmds.textField()
        cmds.setParent('..')
        cmds.text(l='Enter in new comment')
        self.new_comment_field = cmds.scrollField()
        add = cmds.button(l='Add', c=self.add_comment)
        cmds.showWindow(win_name)
        
        
    def add_comment(self, *args):
        '''
        Adds the newly created lable and comment to the comment file.
        '''
        
        self.new_lable = cmds.textField(self.new_lableField, q=True, tx=True)
        self.new_comment = cmds.scrollField(self.new_comment_field, q=True, tx=True)
        
        comment_file = open(file_name, 'a')
        comment_file.write(self.new_lable + '\n')
        comment_file.write(self.new_comment + '\n')
        comment_file.close()
        
        cmds.deleteUI(win_name)
        gui()
        

class Main_Widget():
    def __init__(self, name, objs, comments, pf, bg_color=[1,0,0]):
        self.mainFrame = cmds.frameLayout(l='%s - %s' % (name, len(objs)), bgc=bg_color, cll=True, w=500)
        if not objs:
            cmds.frameLayout(self.mainFrame, e=1, cl=1, bgc=[0.5, 0.5, 0.5], w=500)
        rowCol = cmds.rowColumnLayout(nc=2)
        self.list_widget = Widget_One(objs)
        cmds.setParent(rowCol)
        self.grade_widget = Widget_Two(objs, comments, pf)
        cmds.setParent(self.mainFrame)
        

def gui():
    '''
    Creats the gui
    '''
    global summery_scroll
    
    file_name = '/Users/critnkitten/Desktop/file_submission.txt'
    
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
    cmds.textField(w=133, tx=(cmds.file(q=True, sn=True)))
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
    cmds.columnLayout(w=bw, cat=['left', 200])
    cmds.button(l='Export', w= 100, c=excel_export)
    cmds.setParent(top_main)
    
    
    
    
    '''
    Subsection of tool
    '''
    cmds.columnLayout(w=500)
    form = cmds.formLayout()
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

    tab1 = cmds.columnLayout()
    cmds.text(l='Summary Section')
    summery_scroll = cmds.scrollField(ww=True)
    cmds.setParent('..')
    
    '''    
    Creates the 'Joint' grading sections
    '''
    
    tab3 = cmds.columnLayout()
    cmds.scrollLayout()
    main = cmds.columnLayout()
    joint_frame = cmds.frameLayout('Joints', cll=True, w=bw-10)
    joint_col = cmds.columnLayout()
    main_widget1 = Main_Widget('Joint Naming - Invalid', check_joint_naming(cmds.ls(typ='joint')), 'file_submission', pf=1)
    cmds.setParent(joint_col)    
    main_widget2 = Main_Widget('Joint Rotations - Invalid', check_joint_rotates(cmds.ls(typ='joint')), 'file_submission', pf=1)
    cmds.setParent(joint_col)
    main_widget3 = Main_Widget('Joint Translates - Warning', check_joint_translates(cmds.ls(typ='joint')), 'file_submission', pf=1)
    cmds.setParent(joint_col)    
    #main_widget4 = Main_Widget('Joint Orientaiton - Invalid', check_joint_orient(cmds.ls(typ='joint')), joint_naming, pf=0)
    cmds.setParent(main)    


    
    '''
    Creates the 'Curve' grading sections
    '''

    cmds.frameLayout(l='Curves', cll=True, w=bw-10)
    curve_col = cmds.columnLayout()
    main_widget5 = Main_Widget('Curve Naming - Invalid', check_curve_naming(cmds.ls(typ='nurbsCurve')), joint_naming, pf=1)
    cmds.setParent(curve_col) 
    main_widget6 = Main_Widget('Curve Transforms - Invalid', check_transforms(cmds.ls(typ='nurbsCurve')), joint_rotates, pf=1)
    cmds.setParent(curve_col) 
    main_widget7 = Main_Widget('Curve History - Invalid', check_curve_hist(cmds.ls(typ='nurbsCurve')), joint_rotates, pf=1)
    cmds.setParent(main)

    
    '''    
    Creates the 'Geometry' grading sections
    '''

    cmds.frameLayout(l='Geometry', cll=True, w=bw-10)
    geo_col = cmds.columnLayout()
    main_widget8 = Main_Widget('Geo Naming - Invalid', check_geo_naming(cmds.ls(typ='mesh')), joint_naming, pf=1)
    cmds.setParent(geo_col)
    main_widget9 = Main_Widget('Geo Transforms - Invalid', check_transforms(cmds.ls(typ='mesh')), joint_naming, pf=1)
    cmds.setParent(geo_col)
    main_widget10 = Main_Widget('Geo History - Invalid', check_geo_hist(cmds.ls(typ='mesh')), joint_naming, pf=1)    
    cmds.setParent(main)
   
    
    cmds.tabLayout(tabs, edit=True, tabLabel=[(tab1, 'Summary'), (tab3, 'Grading')])
    
    
    cmds.showWindow(win)
    
    
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

def open_scene(*args):
    '''    
    Function to open a new scene file and reload the tool
    '''
    mel.eval('OpenScene;')
    import threeDF_script
    threeDF_script.gui()



def excel_export(*args):
    print 'Will export grades into specified excel document'
    
  