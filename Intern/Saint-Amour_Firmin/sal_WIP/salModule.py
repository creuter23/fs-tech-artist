'''
# based on Tony's grading script

Author: Firmin Saint-Amour

Description: Module containing reusable pieces specifically for the shading and lighting scripts

'''


import pymel.core as pm


# Section class
# name = what will be displayed in that grading section
# layout = the formLayout that these GUI components will be attached to
# total = the function the function that will run through and add up all the grades 
#----------------------------------------------------------------------
# control = the control to attach the first component of the secion to
# **if nothing is given than the first component (radioButtonGrp) will attach to the parent (frameLayout)
# **the second instance must have a control or they will overlap cause i'm using a from layout they need to attach to each other

class Section():
    def __init__(self, name, layout, total, control=''):
        # the label for the first row of radioButtonGrp also the name of the section
        self.name = name
        # the control that the first component will attach to
        self.control = control
        # the function that will run through and update the final grade as changes happen    
        self.total = total
        # the * formLayout that things will be attached tp
        self.layout = layout
        # instancing the CommentWidget which has the commenting system built into it
        self.scrollField = CommentWidget(200 , 150)
        
    def radioCommand(self):
        # this command changes the grade based on the selected button
        
        if self.row01.getSelect() == 1:
            self.intField.setValue1(100)
            
        if self.row01.getSelect() == 2:
            self.intField.setValue1(89)
            
        if self.row01.getSelect() == 3:
            self.intField.setValue1(79)
            
        if self.row02.getSelect() == 1:
            self.intField.setValue1(72)
            
        if self.row02.getSelect() == 2:
            self.intField.setValue1(69)
        
    def create(self):
        
         # this creates the actual GUI components
         #** returns the last component (the separator) so that the next group can be attached to it
        
        if self.control == '':
            # radioButtonGrp
            self.row01 = pm.radioButtonGrp( numberOfRadioButtons = 3, label = '%s (45)' % self.name, labelArray3=['A+ -A', 'B+ -B', 'C+ -C'], onCommand = pm.Callback(self.radioCommand))
            self.row02 = pm.radioButtonGrp(  numberOfRadioButtons = 2, shareCollection = self.row01, label='', labelArray2=['D', 'F'], onCommand = pm.Callback(self.radioCommand))
            pm.formLayout( self.layout , edit=1, attachForm=[[self.row01, "top", 5], [self.row01, "left", 5]])
            pm.formLayout( self.layout , edit=1, attachForm=[self.row02, "left", 5, ], attachControl=[self.row02, "top", 5, self.row01])
            
            # intField for Grade
            self.intField = pm.intFieldGrp( numberOfFields = 1, label = 'Grade', changeCommand = self.total)
            self.comments = pm.text( label = 'comments')
            
            # comment scrollField
            scrollField = self.scrollField.create()
            self.separator = pm.separator( height=15, width=460, style='in' )
            
            # arranging components
            pm.formLayout( self.layout , edit=1, attachForm=[self.intField, "top", 5], attachControl=[self.intField, "top", 10, self.row02])
            pm.formLayout( self.layout , edit=1, attachForm=[scrollField, "left", 140], attachControl=[scrollField, "top", 10, self.intField])
            pm.formLayout( self.layout , edit=1, attachForm=[self.comments, "left", 60], attachControl=[self.comments, "top", 10, self.intField])
            pm.formLayout( self.layout , edit=1, attachForm=[self.separator, "left", 60], attachControl=[self.separator, "top", 10, scrollField])
        
            return self.separator
        
        else:
            # radioButtonGrp
            self.row01 = pm.radioButtonGrp( numberOfRadioButtons = 3, label = '%s (45)' % self.name, labelArray3=['A+ -A', 'B+ -B', 'C+ -C'], onCommand = pm.Callback(self.radioCommand))
            self.row02 = pm.radioButtonGrp(  numberOfRadioButtons = 2, shareCollection = self.row01, label='', labelArray2=['D', 'F'], onCommand = pm.Callback(self.radioCommand))
            pm.formLayout( self.layout , edit=1, attachForm=[[self.row01, "top", 5], [self.row01, "left", 5]] , attachControl=[self.row01, "top", 5, self.control])
            pm.formLayout( self.layout , edit=1, attachForm=[self.row02, "left", 5, ], attachControl=[self.row02, "top", 5, self.row01])
            
            # intField for Grade
            self.intField = pm.intFieldGrp( numberOfFields = 1, label = 'Grade', changeCommand = self.total)
            self.comments = pm.text( label = 'comments')
            
            # comment scrollField
            scrollField = self.scrollField.create()
            self.separator = pm.separator( height=15, width=460, style='in' )
            
            # arranging components
            pm.formLayout( self.layout , edit=1, attachForm=[self.intField, "top", 5], attachControl=[self.intField, "top", 10, self.row02])
            pm.formLayout( self.layout , edit=1, attachForm=[scrollField, "left", 140], attachControl=[scrollField, "top", 10, self.intField])
            pm.formLayout( self.layout , edit=1, attachForm=[self.comments, "left", 60], attachControl=[self.comments, "top", 10, self.intField])
            pm.formLayout( self.layout , edit=1, attachForm=[self.separator, "left", 60], attachControl=[self.separator, "top", 10, scrollField])
        
            return self.separator
        
    
    """
    def menu_item_comments(self, *args):
        '''
        Creates the menu items for the comment field
        '''
        self.rmc = cmds.popupMenu(parent=self.mainScroll)
        cmds.menuItem(l='Custom', c=self.create_comment)

                
        self.comments = open(file_name, 'r')
        comment_data = self.comments.readlines()
        self.comments.close()
        
        num_lines = len(comment_data)
        lable = 0
        x = 1
        
        while x < num_lines:
            cmds.menuItem(l=comment_data[lable], c=pm.Callback(self.adding_text, comment_data[x]))

            lable += 2
            x += 2

    """
# commenting system based on Jen's Com_Widget
class CommentWidget():
        def __init__(self, width , height):
            self.width = width
            self.height = height
            
        # creates the scrollField
        def create(self):
            self.scrollField = pm.scrollField( wordWrap = True , width = self.width , height = self.height )
            self.menus()
            
            return self.scrollField
        
        # creates the popUpMenu for the scrollField
        def menus(self):
            print 'is this working'
            # popUpMenu
            self.popUp = pm.popupMenu( parent = self.scrollField )
            # menuItems for the popUpMenu
            pm.menuItem( label = 'testing this')
        
        
        # * need to test with txt files
        # * also create menu items based on text files

# creates the summary section that has all the final grades and the output button
class UpperSection():
    def __init__(self):
        self.columnLayout = pm.columnLayout( adjustableColumn=True )
        self.layout = pm.formLayout()
    
    def updateTotal(self):
        pm.select(cl=1)
    
    def create(self):
        print 'i guess so'
        
        self.antiField = pm.intFieldGrp( numberOfFields=1, label='Antialias/Noise Quality', changeCommand=self.updateTotal)
        self.compField = pm.intFieldGrp( numberOfFields=1, label='Composition/Focal Length', changeCommand=self.updateTotal)
        self.proField = pm.intFieldGrp( numberOfFields=1, label='Professionalism', changeCommand=self.updateTotal)
        self.lateField = pm.intFieldGrp( numberOfFields=1, label='Late Deduction', changeCommand=self.updateTotal)
        self.totalField = pm.intFieldGrp( numberOfFields=1, label='Total Grade', changeCommand=self.updateTotal)
    
        print 'booya'
        pm.formLayout( self.layout, edit=1, attachForm=[[self.antiField, "left", 40], [self.antiField, "top", 5]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.compField ,"top", 35, self.antiField], [self.compField, "right", 0, self.antiField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.proField ,"top", 35, self.compField], [self.proField, "right", 0, self.compField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.lateField ,"top", 35, self.proField], [self.lateField, "right", 0, self.proField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.totalField ,"top", 35, self.lateField], [self.totalField, "right", 0, self.lateField]])
        
        pm.setParent(self.columnLayout)
        pm.button( label = 'Output Grade and Comment' )
        
        
        