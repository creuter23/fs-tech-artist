'''
* based on Tony's grading script

Author: Firmin Saint-Amour

Description: Module containing reusable pieces specifically for the shading and lighting scripts

'''

import maya.cmds as cmds
import pymel.core as pm
import os


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
            pm.menuItem( label = 'Clear' , command = pm.Callback(self.clear))
            pm.menuItem( label = 'Custom' , command = pm.Callback(self.custom))
            while comment < len(self.comments):
                # menuItems for the popUpMenu
                write = self.comments[comment]
                pm.menuItem(label = self.comments[label], command = pm.Callback(self.insertText,  write))
                label += 2
                comment += 2
            
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
            pm.text(l='Enter label')
            self.customLabel = pm.textField(editable = True)
            pm.text(l='Enter custom comment')
            self.customComment = pm.scrollField(width = 200, height= 150)
            self.customFeedback = pm.text(label = '')
            pm.rowColumnLayout(nc = 2)  # nc = number of rows
            pm.button(label='create', command=pm.Callback(self.addCustom))
            pm.button(label='add' , command=pm.Callback(self.saveComment))
            myWin.show()
            
        
        def addCustom(self):
            
            self.scrollField.insertText(self.customComment.getText())
            
            self.scrollField.setBackgroundColor([0,1,0])
            
            # deleting the window
            pm.deleteUI(self.customWin)
            
        def saveComment(self):
            self.newLabel = self.customLabel.getText()
            self.newComment = self.customComment.getText()
            self.writeFile = open(self.fileName , 'a')
            self.writeFile.write(self.newLabel + '\n')
            self.writeFile.write(self.newComment + '\n')
            self.writeFile.close()
            self.customFeedback.setLabel('%s added to file' % self.newLabel)
            self.menus()
            
        
        
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
    '''
    this class will create the upper section for the SAL grading scripts
    that section opens the images
    '''
    def __init__(self):
        self.mainLayout = pm.columnLayout(adjustableColumn = True)
        pm.button(label = 'new fields', command = pm.Callback(self.createFields))
        self.openButtons = pm.radioButtonGrp(numberOfRadioButtons = 2 , columnAlign = [ 1 , 'center' ],label = ' Choose Program ', label1 = 'Preview',label2 = 'Photoshop')
        pm.button(label = 'open images', command = pm.Callback(self.openImage))
        pm.button(label = 'open reference', command = pm.Callback(self.openReference))
        self.layout = pm.rowColumnLayout(nc=2 , cw =[(1, 400) ,(2, 80)])
        # self.num is a number, which will be used to give unique names to the dynamically created fields
        self.num = 1
        # the list of the paths for the images
        self.imageList = []
        # this list will have the base name of all the images
        self.nameList = []
        
    def createFields(self):
        
        pm.setParent(self.layout)
        self.textField = pm.textFieldButtonGrp( 'text%s' % self.num , text='image to load', width = 450, buttonLabel='<<<', bc=pm.Callback(self.addImage, 'text%s' % self.num  ), ed=0 )
        self.button = pm.button('button%s' % self.num , label = 'X', command = pm.Callback(self.delete, 'text%s' % self.num,'button%s' % self.num ))
        self.num += 1
    
    def delete(self, obj1, obj2):
        pm.deleteUI(obj1)
        pm.deleteUI(obj2)
    
    def addImage(self, field):
        self.file = pm.fileDialog()
        self.newFile = os.path.basename(self.file)
        pm.textFieldButtonGrp('%s' % field, edit = True, text = '%s' % self.newFile )
        self.imageList.append(self.file)
        self.nameList.append(self.newFile)
        
    def openReference(self):
        self.ref = pm.fileDialog()
        if self.openButtons.getSelect() == 2:
            pm.util.shellOutput(r"open -a Adobe\ Photoshop\ CS4 %s " % self.ref)
            
        if self.openButtons.getSelect() == 1:
            pm.util.shellOutput(r"open  %s " % self.ref)
            
    def openImage(self):
        # this will open the images from the fields
        # the 'pm.util.shellOutput(r"open -a Adobe\ Photoshop\ CS4 %s " % self.path)' will not take a list only a series of strings with blank space in between
        # the while loop will create a new string with all the file paths in the 'self.imageList' list
        # it also adds a blank space between each path in the list
        x = 0
        self.blank = ' '
        self.path = ''
        
        while x < len(self.imageList):
            self.path+= str(self.imageList[x]) + str(self.blank)
            x += 1
        
        # this will check to see which program to open the images with
        if self.openButtons.getSelect() == 2:
            pm.util.shellOutput(r"open -a Adobe\ Photoshop\ CS4 %s " % self.path)
            
        if self.openButtons.getSelect() == 1:
            pm.util.shellOutput(r"open  %s " % self.path)
            
        print self.queryNames()
            
    
    # this is just a way of getting all the names as a long string to use when outputting    
    def queryNames(self):
        x = 0
        self.blankSpace = ','
        self.name = ''
        while x < len(self.nameList):
            self.name += str(self.nameList[x]) + str(self.blankSpace)
            x += 1
        return self.name
    
    # this give access to the path so the output function can create the comment file in the right place
    def queryPath(self, index = 0):
        path = self.imageList[index]
        
        return path
            
        
          
        
