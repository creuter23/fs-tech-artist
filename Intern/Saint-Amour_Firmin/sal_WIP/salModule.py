'''
* based on Tony's grading script

Author: Firmin Saint-Amour

Description: Module containing reusable pieces specifically for the shading and lighting scripts

'''

import maya.cmds as cmds
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
    def __init__(self, name, layout, updateField, fileRead,  control=''):
        # the label for the first row of radioButtonGrp also the name of the section
        self.name = name
        # the control that the first component will attach to
        self.control = control
        # updateField is the field in the totals section that the changeCommand of the grade field will update
        self.updateField = updateField
        # the  formLayout that components will be attached to
        self.layout = layout
        # the file the comments will be read from, this will be passed to the commentWidget object
        self.fileRead = fileRead
        # instancing the CommentWidget which has the commenting system built into it
        self.scrollField = CommentWidget(width = 200 , height = 150, fileName = self.fileRead)
    
    
    def radioCommand(self):
        # this command changes the grade based on the selected button
        if self.row01.getSelect() != 0 or self.row02.getSelect() != 0:
            self.intField.setBackgroundColor([0,1,0])
        
        if self.row01.getSelect() == 1:
            self.intField.setValue1(100)
            
            print 'is this working'
            
        if self.row01.getSelect() == 2:
            cmds.intFieldGrp( self.intField, edit = 1 , value1 = 89)
            if self.intField.getValue1() > 0 :
                self.totalCommand()
            
        if self.row01.getSelect() == 3:
            self.intField.setValue1(79)
            
        if self.row02.getSelect() == 1:
            self.intField.setValue1(72)
            
        if self.row02.getSelect() == 2:
            self.intField.setValue1(69)
            
    def totalCommand(self):
            print 'testing this out 123'
            value = self.intField.getValue1() 
            cmds.intFieldGrp(self.updateField , edit = 1 , value1 = value)
        
    def create(self):
        
        
         # this creates the actual GUI components
         #** returns the last component (the separator) so that the next group can be attached to it
        
        if self.control == '':
            # radioButtonGrp
            self.row01 = pm.radioButtonGrp( numberOfRadioButtons = 3, label = '%s' % self.name, labelArray3=['A+ -A', 'B+ -B', 'C+ -C'], onCommand = pm.Callback(self.radioCommand))
            self.row02 = pm.radioButtonGrp(  numberOfRadioButtons = 2, shareCollection = self.row01, label='', labelArray2=['D', 'F'], onCommand = pm.Callback(self.radioCommand))
            pm.formLayout( self.layout , edit=1, attachForm=[[self.row01, "top", 5], [self.row01, "left", 5]])
            pm.formLayout( self.layout , edit=1, attachForm=[self.row02, "left", 5, ], attachControl=[self.row02, "top", 5, self.row01])
            
            
            # intField for Grade
            self.intField = pm.intFieldGrp( numberOfFields = 1, label = 'Grade', changeCommand = pm.Callback(self.totalCommand), backgroundColor = [1,0,0])
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
            self.row01 = pm.radioButtonGrp( numberOfRadioButtons = 3, label = '%s' % self.name, labelArray3=['A+ -A', 'B+ -B', 'C+ -C'], onCommand = pm.Callback(self.radioCommand))
            self.row02 = pm.radioButtonGrp(  numberOfRadioButtons = 2, shareCollection = self.row01, label='', labelArray2=['D', 'F'], onCommand = pm.Callback(self.radioCommand))
            pm.formLayout( self.layout , edit=1, attachForm=[[self.row01, "top", 5], [self.row01, "left", 5]] , attachControl=[self.row01, "top", 5, self.control])
            pm.formLayout( self.layout , edit=1, attachForm=[self.row02, "left", 5, ], attachControl=[self.row02, "top", 5, self.row01])
            
            # intField for Grade
            self.intField = pm.intFieldGrp( numberOfFields = 1, label = 'Grade', cc = pm.Callback(self.totalCommand)
                                           , backgroundColor = [1,0,0])
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
        def __init__(self, width , height, fileName):
            self.width = width
            self.height = height
            self.fileName = fileName
            
            
        # creates the scrollField
        def create(self):
            self.scrollField = pm.scrollField( wordWrap = True , width = self.width , height = self.height , backgroundColor = [ 1 , 0 , 0 ])
            self.menus()
            
            return self.scrollField
        
        # creates the popUpMenu for the scrollField
        def menus(self):
            
            # popUpMenu
            self.popUp = pm.popupMenu( parent = self.scrollField )
            
            #opening the file
            self.commentFile = open(self.fileName, 'r')
            # reading
            self.comments =  commentFile.readlines()
            # closing
            self.commentFile.close()
            
            # the label is the first line
            # the actual comment is after the label
            # so the pattern is label, comment, label, comment, label, comment
            label = 0
            comment = 1
            
            while comment != len(self.comments):
                # menuItems for the popUpMenu
                pm.menuItem(label = self.comments[label], command = pm.Callback(self.insertText, self.comments[comment]))
                label += 2
                comment += 2
                
        
        def insertTest(self, comment):
            self.scrollField.insertText(self.comments[comment])

                
        
        # * need to test with txt files
        # * also create menu items based on text files

# creates the summary section that has all the final grades and the output button
class UpperSection():
    def __init__(self):
        self.columnLayout = pm.columnLayout( adjustableColumn=True )
        self.layout = pm.formLayout()
       
    
    def updateTotal(self):
        self.totalField.setValue1(self.antiField.getValue1() * self.antiField.getValue2() + self.compField.getValue1() * self.compField.getValue2() +
                                 self.proField.getValue1() * self.proField.getValue2() - self.lateField.getValue1())
        if self.antiField.getValue2() + self.compField.getValue2() + self.proField.getValue2() != 100:
            self.warning.setLabel('Error : Total Weighting Must Equal 100')
            self.warning.setBackgroundColor([1,0,0])
        else:
            self.warning.setLabel('')
            self.warning.setBackgroundColor([.5,.5,.5])
    
    def create(self):
       
        self.checkBox = pm.checkBox(label = 'Modify Weighting', onCommand = pm.Callback(self.editFields), offCommand = pm.Callback(self.editFields) )
        self.antiField = pm.intFieldGrp( numberOfFields=2, label='Antialias/Noise Quality', extraLabel = 'Weight %' , value2 = 45 , enable1 = False ,
                                        enable2 = False,  changeCommand=pm.Callback(self.updateTotal))
        self.compField = pm.intFieldGrp( numberOfFields=2, label='Composition/Focal Length', extraLabel = 'Weight %' , value2 = 45 , enable1 = False ,
                                        enable2 = False ,changeCommand=pm.Callback(self.updateTotal))
        self.proField = pm.intFieldGrp( numberOfFields=2, label='Professionalism', extraLabel = 'Weight %' ,value2 = 10 ,enable1 = False ,
                                       enable2 = False, changeCommand=pm.Callback(self.updateTotal))
        self.lateField = pm.intFieldGrp( numberOfFields=1, label='Late Deduction' , changeCommand=pm.Callback(self.updateTotal))
        self.totalField = pm.intFieldGrp( numberOfFields=1, label='Total Grade',enable1 = False, changeCommand=pm.Callback(self.updateTotal))
    
        pm.formLayout( self.layout, edit=1, attachForm=[[self.checkBox, "left", 140], [self.checkBox, "top", 5]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.antiField ,"top", 40, self.checkBox], [self.antiField, "right", 10, self.checkBox]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.compField ,"top", 40, self.antiField], [self.compField, "right", 10, self.antiField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.proField ,"top", 40, self.compField], [self.proField, "right", 10, self.compField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.lateField ,"top", 40, self.proField], [self.lateField, "left", 0, self.proField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.totalField ,"top", 40, self.lateField], [self.totalField, "left", 0, self.lateField]])
        
        pm.setParent(self.columnLayout)
        pm.text(label = '')
        self.warning = pm.text(label='')
        pm.text(label = '')
        pm.button( label = 'Output Grade and Comment' )
        
        self.compList = [self.antiField, self.compField, self.proField]
        
        return self.compList
        
        
    def editFields(self):
        if self.checkBox.getValue() != 0:
            self.antiField.setEnable2(True)
            self.compField.setEnable2(True)
            self.proField.setEnable2(True)
        
        else :
            self.antiField.setEnable2(False)
            self.compField.setEnable2(False)
            self.proField.setEnable2(False)
        
        
