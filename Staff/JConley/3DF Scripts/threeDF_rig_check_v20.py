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
import xlrd
import xlwt
import xlutils
import math
import com_wid

#from xlutils.copy import copy



bw=500
frame = 465
sw=200


class Widget_One():
    def __init__(self, objs, width=200):
        # Creates the 'invalid object' list portion of the tool for each section
        
        self.width=width
        self.objs = objs
        self.mainCol = cmds.columnLayout(w=self.width)
        self.dyna = cmds.scrollLayout()
        self.col = None
        self.gen_button()
        
        
    def reload_button(self, *args):
        # Creates a reload button which will reset the 'invalid object' list
        
        if self.col != None:
            cmds.deleteUI(self.col)
            self.gen_button()


    def gen_button(self, *args):
        # Generates clickable buttons for each invalid object found during testing
        
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
        cmds.columnLayout(co=['left', 50])
        cmds.button(l='Reload', w=75, c=self.reload_button)
            
        
    def select_obj(self, obj):
        # Selected object in the tool becomes the selected object inside of the Maya scene
        
        cmds.select(obj, r=1)
        
        
    def remove_object(self, obj):
        # Allows for objects to be removed from the 'invalid object' list
        
        remove_num = self.objsList.index(obj)
        cmds.deleteUI(self.rowCol[remove_num])
        self.rowCol.remove(self.rowCol[remove_num])
        self.objsList.remove(self.objsList[remove_num])


class Widget_Two():
    def __init__(self, objs, comment_file):
        # Creates the grading and comment portion of the tool for each section
        self.file_name = comment_file
        self.grade = []
        self.obj_len = len(objs)

        main = cmds.columnLayout()
        cmds.rowColumnLayout(nc=2, h=25, cw=[(1,110),(2,110)])
        cmds.text(l='Grade')
        
        # Sets the intField value based on the number of invalid objects        
        if self.obj_len == 0:
            self.grade_field = cmds.intField(v=100)
        else:
            self.grade_field = cmds.intField(v=0)
            
        cmds.setParent(main)
        com_wid.Comment_Widget(self.file_name)

        
    def post_summery(self, *args):
        # Posts comments to the summery tab
        self.query_comments = cmds.scrollField(self.mainScroll, q=True, tx=True)
        cmds.scrollField(summery_scroll, e=True, it=self.query_comments + '\n')


class Main_Widget():
    def __init__(self, name, objs, comment_file, bg_color=[1,0,0]):      
        
        self.mainFrame = cmds.frameLayout(l='%s %s Invalid' % (name, len(objs)), bgc=bg_color, cll=True, w=frame)
        if not objs:
            cmds.frameLayout(self.mainFrame, e=1, cl=1, bgc=[0.5, 0.5, 0.5], w=frame)
        rowCol = cmds.rowColumnLayout(nc=2)
        self.list_widget = Widget_One(objs)
        cmds.setParent(rowCol)
        self.grade_widget = Widget_Two(objs, comment_file)
        cmds.setParent(self.mainFrame)
        

def gui():
    # Creats the gui
    global summery_scroll

    # Checks to make sure window does not exist and has no pre-existing preferences
    win = 'win3DFGrade'
    if (cmds.window(win, ex=True)):
        cmds.deleteUI(win)
    if (cmds.windowPref(win, ex=True)):
        cmds.windowPref(win, r=1)
        
    # Creates the window for the grading tool    
    cmds.window(win, w=bw, h=400)
    
    # Main section of tool
    # Displays scene name with button for opening new scene files
    
    top_main = cmds.columnLayout(w=500)
    cmds.rowColumnLayout(w=500, nc=3)
    cmds.text(l='Scene Name', w=133)
    cmds.textField(w=133, tx=(cmds.file(q=True, sn=True)))
    cmds.button(l='Open Scene', w=133, c=open_scene)
    cmds.setParent(top_main)
    
    # Dislays grading options such as professionalism and late turnin decutions  
    cmds.rowColumnLayout(w=500, nc=6)
    cmds.text('Professional', w=66)
    cmds.floatField(v=0.00, w=66)
    cmds.text('Late Turnin', w=66)
    cmds.floatField(v=0.00, w=66)
    cmds.text('Total Grade', w=66)
    cmds.floatField(v=0.00, w=66)
    cmds.setParent(top_main)
    
    # Creates Export button
    cmds.columnLayout(w=bw, cat=['left', 200])
    cmds.button(l='Export', w= 100, c=export_button)
    cmds.setParent(top_main)
    
    # Subsection of tool
    #Dictates which grading tool is being used (modeling, animation, rigging, etc.)
    cmds.columnLayout()
    form = cmds.formLayout()
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

    tab1 = cmds.columnLayout()
    cmds.text(l='Summary Section')
    summery_scroll = cmds.scrollField(ww=True)
    cmds.setParent('..')
    
   
    # Creates the 'Joint' grading sections
    tab3 = cmds.columnLayout()
    cmds.scrollLayout(w=491)
    main = cmds.columnLayout()
    joint_frame = cmds.frameLayout('Joints        ', cll=True, w=frame)
    joint_col = cmds.columnLayout()
    joint_widget1 = Main_Widget('Joint Naming        ', check_joint_naming(cmds.ls(typ='joint')), '/Users/critnkitten/Library/Preferences/Autodesk/maya/scripts/3DF_Rig_Comments/joint_naming.txt')
    cmds.setParent(joint_col)    
    joint_widget2 = Main_Widget('Joint Rotations     ', check_joint_rotates(cmds.ls(typ='joint')), '/Users/critnkitten/Library/Preferences/Autodesk/maya/scripts/3DF_Rig_Comments/joint_transforms.txt')
    cmds.setParent(joint_col)
    joint_widget3 = Main_Widget('Joint Translates    ', check_joint_translates(cmds.ls(typ='joint')), '/Users/critnkitten/Library/Preferences/Autodesk/maya/scripts/3DF_Rig_Comments/joint_transforms.txt')
    cmds.setParent(joint_col)
    
    joint_widgets = [joint_widget1, joint_widget2, joint_widget3]
    
    #main_widget4 = Main_Widget('Joint Orientaiton - Invalid', check_joint_orient(cmds.ls(typ='joint')), joint_naming, pf=0)
    
    
    cmds.setParent(main)    

    # Creates the 'Curve' grading sections
    curve_frame = cmds.frameLayout(l='Curves      ', cll=True, w=frame)
    curve_col = cmds.columnLayout()
    curve_widget1 = Main_Widget('Curve Naming        ', check_curve_naming(cmds.ls(typ='nurbsCurve')), '/Users/critnkitten/Library/Preferences/Autodesk/maya/scripts/3DF_Rig_Comments/curve_naming.txt')
    cmds.setParent(curve_col) 
    curve_widget2 = Main_Widget('Curve Transforms    ', check_transforms(cmds.ls(typ='nurbsCurve')), '/Users/critnkitten/Library/Preferences/Autodesk/maya/scripts/3DF_Rig_Comments/curve_transforms.txt')
    cmds.setParent(curve_col) 
    curve_widget3 = Main_Widget('Curve History       ', check_curve_hist(cmds.ls(typ='nurbsCurve')), '/Users/critnkitten/Library/Preferences/Autodesk/maya/scripts/3DF_Rig_Comments/curve_history.txt')
    cmds.setParent(main)
    
    curve_widgets = [curve_widget1, curve_widget2, curve_widget3]

    # Creates the 'Geometry' grading sections
    geo_frame = cmds.frameLayout(l='Geometry  ', cll=True, w=frame)
    geo_col = cmds.columnLayout()
    geo_widget1 = Main_Widget('Geo Naming          ', check_geo_naming(cmds.ls(typ='mesh')), '/Users/critnkitten/Library/Preferences/Autodesk/maya/scripts/3DF_Rig_Comments/geo_naming.txt')
    cmds.setParent(geo_col)
    geo_widget2 = Main_Widget('Geo Transforms      ', check_transforms(cmds.ls(typ='mesh')), '/Users/critnkitten/Library/Preferences/Autodesk/maya/scripts/3DF_Rig_Comments/geo_transforms.txt')
    cmds.setParent(geo_col)
    geo_widget3 = Main_Widget('Geo History         ', check_geo_hist(cmds.ls(typ='mesh')), '/Users/critnkitten/Library/Preferences/Autodesk/maya/scripts/3DF_Rig_Comments/geo_history.txt')    
    cmds.setParent(main)
    
    geo_widgets = [geo_widget1, geo_widget2, geo_widget3]
   
    cmds.tabLayout(tabs, edit=True, tabLabel=[(tab1, 'Summary'), (tab3, 'Grading')])
    
    widget_list = []
    widget_list = joint_widgets + curve_widgets + geo_widgets
    
    indiv_widgets = [joint_widgets, curve_widgets, geo_widgets]
    frame_list = [joint_frame, curve_frame, geo_frame]

    for each in widget_list:
        indiv_grade = cmds.intField(each.grade_widget.grade_field, q=True, v=True)
        name = cmds.frameLayout(each.mainFrame, q=True, l=True)
        cmds.frameLayout(each.mainFrame, e=True, l='%s   -   %s' % (name, indiv_grade))
    
    y = 0
    global xcel_val
    xcel_val = []
    
    for each in frame_list:
        name = cmds.frameLayout(each, q=True, l=True)
        grades_per_section = 0
        xcel = 0
        x = 0
        for obj in indiv_widgets[y]:
            grade_query = cmds.intField(obj.grade_widget.grade_field, q=True, v=True)
            grades_per_section += grade_query
            x += 1
            if grade_query == 100:
                xcel += 1
        xcel_val.append(xcel)
        section_grade = grades_per_section / x
        cmds.frameLayout(each, e=True, l='%s %s' % (name, xcel))
        y += 1

  


    
    cmds.showWindow()
    
def export_button(*args):
    # Exporting grades into .xls document
    
    
    """    
    file_name = '/Users/critnkitten/Desktop/test.xls'
    
    excel_book = xlrd.open_workbook(file_name)
    wb = copy(excel_book)
    
    #xlwt.Formula example
    #link = xlwt.Formula('HYPERLINK("%s";"View Details")' % url)
    
    cell_form = xlwt.Formula("A1*B1")
    
    wb.get_sheet(0).write(0, 2, cell_form)
    
    wb.save('/Users/critnkitten/Desktop/test.xls')
    """
    
    
       
    file_name = '/Users/critnkitten/Desktop/3DF_LocalGrading_Template.xls'
    
    excel_book = xlrd.open_workbook(file_name, formatting_info=1) 
    wb = copy(excel_book)
    print 'opening excel book'
    row_num = 5
    col_num = 35
    col_form = []
    for each in xcel_val:
        wb.get_sheet(4).write(row_num, col_num, each)
        col_form.append(col_num)
        col_num += 1
        
        
    cell_form = xlwt.Formula("((AJ6*10)+(AK6*8)+(AL6*8)+(AM6*8)+(AN6*8)+(AO6))")
    # end cell formula "((AJ6*10)+(AK6*8)+(AL6*8)+(AM6*8)+(AN6*8)+(AO6))"
    wb.get_sheet(4).write(row_num, 41, cell_form)
    
    print 'saving excel book'    
    wb.save('/Users/critnkitten/Desktop/3DF_LocalGrading_Template.xls')



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

  