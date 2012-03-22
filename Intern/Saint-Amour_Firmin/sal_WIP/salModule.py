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
        # instancing the CommentWidget which has the commenting system built into it / create() creates it 
        self.scrollField = CommentWidget(width = 200 , height = 150, fileName = self.fileRead).create()
    
    
    def radioCommand(self):
        # this command changes the grade based on the selected button
        if self.row01.getSelect() != 0 or self.row02.getSelect() != 0:
            self.intField.setBackgroundColor([0,1,0])
        
        if self.row01.getSelect() == 1:
            self.intField.setValue1(100)
            self.totalCommand()
            
            
        if self.row01.getSelect() == 2:
            self.intField.setValue1(89)
            self.totalCommand()
            
        if self.row01.getSelect() == 3:
            self.intField.setValue1(79)
            self.totalCommand()
            
        if self.row02.getSelect() == 1:
            self.intField.setValue1(72)
            self.totalCommand()
            
        if self.row02.getSelect() == 2:
            self.intField.setValue1(69)
            self.totalCommand()
            
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
            #scrollField = self.scrollField.create()
            self.separator = pm.separator( height=15, width=460, style='in' )
            
            # arranging components
            pm.formLayout( self.layout , edit=1, attachForm=[self.intField, "top", 5], attachControl=[self.intField, "top", 10, self.row02])
            pm.formLayout( self.layout , edit=1, attachForm=[self.scrollField, "left", 140], attachControl=[self.scrollField, "top", 10, self.intField])
            pm.formLayout( self.layout , edit=1, attachForm=[self.comments, "left", 60], attachControl=[self.comments, "top", 10, self.intField])
            pm.formLayout( self.layout , edit=1, attachForm=[self.separator, "left", 60], attachControl=[self.separator, "top", 10, self.scrollField])
        
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
            #scrollField = self.scrollField.create()
            self.separator = pm.separator( height=15, width=460, style='in' )
            
            # arranging components
            pm.formLayout( self.layout , edit=1, attachForm=[self.intField, "top", 5], attachControl=[self.intField, "top", 10, self.row02])
            pm.formLayout( self.layout , edit=1, attachForm=[self.scrollField, "left", 140], attachControl=[self.scrollField, "top", 10, self.intField])
            pm.formLayout( self.layout , edit=1, attachForm=[self.comments, "left", 60], attachControl=[self.comments, "top", 10, self.intField])
            pm.formLayout( self.layout , edit=1, attachForm=[self.separator, "left", 60], attachControl=[self.separator, "top", 10, self.scrollField])
        
            return self.separator
        
    def query(self):
        # this will get the comments from the scrollFields
        text = self.scrollField.getText()
        
        return text
        
        
    
 
# commenting system based on Jen's Comment_Widget
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
            self.comments =  self.commentFile.readlines()
            # closing
            self.commentFile.close()
            
            # the label is the first line
            # the actual comment is after the label
            # so the pattern is label, comment, label, comment, label, comment
           
            label = 0
            
            comment = 1
            
            while comment != len(self.comments):
                # menuItems for the popUpMenu
                write = self.comments[comment]
                pm.menuItem(label = self.comments[label], command = pm.Callback(self.insertText,  write))
                
                
                label += 2
                comment += 2
            
            pm.menuItem( label = 'Clear' , command = pm.Callback(self.clear))
            pm.menuItem( label = 'Custom' , command = pm.Callback(self.custom))
        
                
        
        def insertText(self, comment):
            
            self.scrollField.insertText(comment)
            
            self.scrollField.setBackgroundColor([1,1,0])
            
        def clear(self):
            
            self.scrollField.setText('')
            self.scrollField.setBackgroundColor([1,0,0])
            
        def custom(self):
            
          
            self.customWin = 'customWindow'
            
            if (pm.window(self.customWin, ex=True)):
                pm.deleteUI(self.customWin)
            if (pm.windowPref(self.customWin, ex=True)):
                pm.windowPref(self.customWin, remove = True)
                
            myWin = pm.window(self.customWin, title = 'CUSTOM', width = 200, height = 150)
            pm.columnLayout(adjustableColumn=True)
            
            
            pm.text(l='Enter custom comment')
            self.customComment = pm.scrollField(width = 200, height= 150)
            pm.button(label='create', command=pm.Callback(self.addCustom))
            myWin.show()
            
        def addCustom(self):
            
            self.scrollField.insertText(self.customComment.getText())
            
            self.scrollField.setBackgroundColor([0,1,0])
            
            pm.deleteUI(self.customWin)
            
            return 

                
        
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
        
class Images():
    def __init__(self):
        pm.textFieldButtonGrp( text='', buttonLabel='Load Image', bc=a, ed=0 )
        
