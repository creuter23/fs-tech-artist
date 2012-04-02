'''
* based on Tony's grading script

Author: Firmin Saint-Amour

Description: Module containing reusable pieces specifically for the shading and lighting scripts

'''
from PIL import Image # this read metadata from images
# maya commmands
import maya.cmds as cmds
# pymel
import pymel.core as pm
# os module
import os
# pickle
import shelve
'''
import xlrd
import xlwt
import openpyxl
'''


# the gradign section for each script
class Section():
    '''
    this creates the grading section for the SAL scripts
    it uses the comment widget class as the commenting system
    '''
    
    def __init__(self, name, layout, updateField, fileRead, updateCommand, control=''):
        # the label for the first row of radioButtonGrp also the name of the section
        self.name = name
        # this the outside command that this section will call to update the total grade section
        self.updateCommand = updateCommand
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
        
        self.number = 0
    
    def write(self, name, format, size1, size2):
        
        self.newLayout = pm.columnLayout(adjustableColumn= True)
        self.nameInfo = pm.text( label= name)
        self.formatInfo = pm.text( label= format)
        self.sizeInfo = pm.text('size%s' % self.number, label= '%s X %s' % (size1, size2))
        
        
        
        if self.number <= 0 :
            pm.formLayout( self.layout , edit=1, attachForm=[self.newLayout, "left", 60], attachControl=[self.newLayout, "top", 10, self.scrollField])
            
        else:
            pm.formLayout( self.layout , edit=1, attachForm=[self.newLayout, "left", 60], attachControl=[self.newLayout, "top", 10, 'size%s' % self.number])
            
        self.number += 1
            
    def radioCommand(self):
        # this command changes the grade based on the selected button
        if self.row01.getSelect() != 0 or self.row02.getSelect() != 0:
            self.intField.setBackgroundColor([0,1,0])
        
        if self.row01.getSelect() == 1:
            self.intField.setValue1(100)
            self.totalCommand()
            self.updateCommand.updateTotal()
            
        if self.row01.getSelect() == 2:
            self.intField.setValue1(89)
            self.totalCommand()
            self.updateCommand.updateTotal()
            
        if self.row01.getSelect() == 3:
            self.intField.setValue1(79)
            self.totalCommand()
            self.updateCommand.updateTotal()
            
        if self.row02.getSelect() == 1:
            self.intField.setValue1(72)
            self.totalCommand()
            self.updateCommand.updateTotal()
            
        if self.row02.getSelect() == 2:
            self.intField.setValue1(69)
            self.totalCommand()
            self.updateCommand.updateTotal()
            
    def totalCommand(self):
            value = self.intField.getValue1() 
            self.updateField.setValue1(value)
        
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
      
      
class Pro(Section):
   
    number = 0
    
    def write(self, name, format, size1, size2):
        
        self.newLayout = pm.columnLayout(adjustableColumn= True)
        self.nameInfo = pm.text( label= name)
        self.formatInfo = pm.text( label= format)
        self.sizeInfo = pm.text('size%s' % number, label= '%s X %s' % (size1, size2))
        
        
        
        if self.number <= 0 :
            pm.formLayout( self.layout , edit=1, attachForm=[self.newLayout, "left", 60], attachControl=[self.newLayout, "top", 10, self.scrollField])
            
        else:
            pm.formLayout( self.layout , edit=1, attachForm=[self.newLayout, "left", 60], attachControl=[self.newLayout, "top", 10, 'size%s' % number])
            
       
class Radio_Collection():
    """
    this class creates the radio buttons for each grading section
    takes one arguement , field = field to update in a different section of the script, type= pymel object intFieldGrp
    
    """
    def __init__(self, field):
        '''
        radioCollection
        '''
        self.field = field
        
    def create(self):
        layout = pm.columnLayout(width= 90, adjustableColumn= False)
        self.radioCollection = pm.radioCollection()
        self.aField = pm.radioButton( label='A+ to A-', onCommand= pm.Callback(self.update, 100)  )
        self.bField = pm.radioButton( label='B+ to B-', onCommand= pm.Callback(self.update, 89)  )
        self.cField = pm.radioButton( label='C+ to C-', onCommand= pm.Callback(self.update, 79)  )
        self.dField = pm.radioButton( label='D', onCommand= pm.Callback(self.update, 72)  )
        self.fField = pm.radioButton( label='f', onCommand= pm.Callback(self.update, 69)  )
        pm.rowColumnLayout(nc=2, columnWidth= ([1,35], [2,55])) # total width 85
        pm.text( label= 'Grade', width= 35)
        self.gradeField = pm.intField(changeCommand= self.output, width= 35 )
        
        return layout
        
        
    def update(self, value):
        self.gradeField.setValue(value)
        self.field.setValue1(self.gradeField.getValue())
        
    def output(self):
        self.field.setValue1(self.gradeField.getValue())
        
    def queryGrade(self):
        return self.gradeField
        
class Checker_Options():
    def __init__(self, fileName):
        self.fileName = fileName
        print 'checker initialized'
        
    def create(self):
        self.mainLayout = pm.columnLayout(adjustableColumn = True)
        #pm.rowColumnLayout(numberOfColumns=2, columnWidth= ([1,40], [2,200]))
        self.name = pm.textFieldGrp( label='Name', changeCommand= pm.Callback(self.writeOut), columnWidth2= (40,140))
        self.format = pm.textFieldGrp( label= 'Format', changeCommand= pm.Callback(self.writeOut), columnWidth2= (40,140))
        self.size = pm.intFieldGrp( label= 'Size', numberOfFields= 2, value1= 720, value2= 486, changeCommand= pm.Callback(self.writeOut),columnWidth3= (40,70,70) )
        
    def writeOut(self):
        dirPath = os.path.dirname(__file__)
        #self.fileName = 'proj01_start'
        fullPath = os.path.join(dirPath, self.fileName)
        
        startFileOutput = shelve.open('%s' % fullPath , 'n')
        startFileOutput['name'] = ('%s' % self.name.getText())
        startFileOutput['format'] = ('%s' % self.format.getText().upper())
        startFileOutput['value1'] = ('%s' % self.size.getValue1())
        startFileOutput['value2'] = ('%s' % self.size.getValue2())
        startFileOutput.sync()
        print startFileOutput['name']
        print startFileOutput['format']
        print startFileOutput['value1']
        startFileOutput.close()
        
    def preFill(self):
        dirPath = os.path.dirname(__file__)
        #self.fileName = 'proj01_start.db'
        fullPath = os.path.join(dirPath, '%s.db' % (self.fileName))
        
        if os.path.exists("%s" % fullPath):
            startFile = shelve.open('%s' % fullPath, 'r')
            print startFile
            print (startFile['name'])
            self.name.setText(str(startFile['name']))
            self.format.setText(str(startFile['format']))
            self.size.setValue1(int(startFile['value1']))
            self.size.setValue2(int(startFile['value2']))
            startFile.close()
        
class Checker_Info():
    def __init__(self):
        print "stuff testing 123"
        
    def create(self):    
        self.layout = pm.columnLayout(width= 300, adjustableColumn= False)
        
        return self.layout
    
    def update(self,name, format, size):
        #self.scroll.insertText(name)
        #self.scroll.insertText(format)
        #self.scroll.insertText('%s X %s' % (size[0], size[1]))
        
        pm.setParent(self.layout)
        self.name = pm.text( label= '%s' % (name))
        self.format = pm.text( label= '%s' % (format))
        self.size = pm.text( label= '%s X %s' % (size[0], size[1]))
        
        return self.layout
        
        
class Checker():
    def __init__(self, fileName):
        self.fileName = fileName
        
        self.main = pm.columnLayout(adjustableColumn= True)
        self.frame = pm.frameLayout(label = 'checker', cll = True, cl = False, borderStyle = 'etchedIn', width = 480)
        self.layout = pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,180], [2,10], [3,290]))
        
        pm.text(label='Check')
        pm.text( label= '')
        pm.text(label='result')
        pm.text(label= '')
        pm.text( label= '')
        pm.text(label= '')
        
    def create(self):
        
        self.check = Checker_Options(self.fileName)
        self.check.create()
        self.check.preFill()
        pm.setParent(self.layout)
        pm.text(label= '')
        
        #pm.text(label='')
        self.feedback = Checker_Info()
        self.feedback.create()
        
    def update(self, objList):
        
        
        for obj in objList:
            print obj
            image = Image.open('%s' % (obj))
            format = image.format
            size = image.size
            name = os.path.basename('%s' % (obj))
            self.feedback.update(name, format, size)
        
        
        

class Grading_Section():
    '''
    this creates the grading section which uses the Radio_Collection and Comment_Widget classes
    name = name of section
    field = field to update
    fileName = text file to read from
    '''
    
    
    # grading section
    def __init__(self, name, field, fileName):
        self.name = name
        self.field = field
        self.file = fileName
        self.main = pm.columnLayout(adjustableColumn= True)
        self.frame = pm.frameLayout(label = self.name, cll = True, cl = False, borderStyle = 'etchedIn', width = 480)
        self.layout = pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,90], [2,10], [3,380]))
        #pm.setParent(self.layout)
        
        
        self.grading = pm.text(label='grading')
        pm.text( label= '')
        self.comments = pm.text(label='comments')
        pm.text(label= '')
        pm.text( label= '')
        pm.text(label= '')
        
        
        
        
        
    def create(self):
        
        self.grades = radioCollection(self.field)
        radio = self.grades.create()
        
        
        pm.setParent(self.layout)
        pm.text( label= '')
        self.scrollField = CommentWidget(width= 300, height= 120, fileName= self.file).create()
       
        
    def getText(self):
        self.scrollField.getText()
               
# commenting system based on Jen's Comment_Widget
class CommentWidget():
    '''
    this creates the scrollFields section and the commenting system
    '''
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
        self.commentFile = open('%s' % str(self.fileName), 'r')
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
            
        myWin = pm.window(self.customWin, title = 'CUSTOM', width = 200, height = 150, backgroundColor=[.68,.68,.68])
        pm.columnLayout(adjustableColumn=True)
        pm.text(l='Enter label')
        self.customLabel = pm.textField(editable = True)
        pm.text(l='Enter custom comment')
        self.customComment = pm.scrollField(width = 200, height= 150)
        self.customFeedback = pm.text(label = '')
        pm.rowColumnLayout(nc = 2, cw= ([1,100], [2,100]))  # nc = number of rows
        pm.button(label='create', command=pm.Callback(self.addCustom))
        pm.button(label='add' , command=pm.Callback(self.saveComment))
        myWin.show()
        
    
    def addCustom(self):
        
        self.scrollField.insertText(self.customComment.getText())
        
        self.scrollField.setBackgroundColor([0,1,0])
        
        # deleting the window
        pm.deleteUI(self.customWin)
       
    # this will add the comment to the selected file 
    def saveComment(self):
        self.customFeedback.setLabel('%s added to file' % self.customLabel.getText())
        self.writeFile = open(self.fileName , 'a')
        print self.customLabel.getText()
        self.writeFile.write(self.customLabel.getText() + '\n')
        print self.customComment.getText()
        self.writeFile.write(self.customComment.getText() + '\n')
        self.writeFile.close()
        self.menus()
            
# the total grade section for each Script
class UpperSection():
    '''
    creates the summary section that has all the final grades and the output button
    '''
    def __init__(self):
        self.columnLayout = pm.columnLayout( adjustableColumn=True , width= 480 )
        self.layout = pm.formLayout()
    
    # command for the radioButtons that connect  to the late deduction field
    def radioUpdate(self):
        if self.radioButtons.getSelect() == 1:
            self.lateField.setValue1(10)
            self.updateTotal()
            
        if self.radioButtons.getSelect() == 2:
            self.lateField.setValue1(20)
            self.updateTotal()
            
        if self.radioButtons.getSelect() == 3:
            self.lateField.setValue1(30)
            self.updateTotal() 
    
    # this updates the fields and does some calculations
    def updateTotal(self):
        self.totalField.setValue1(self.antiField.getValue1() / float(100) * self.antiField.getValue2() + self.compField.getValue1() /  float(100) * self.compField.getValue2() +
                                 self.proField.getValue1() /  float(100)  * self.proField.getValue2() - self.lateField.getValue1())
        if self.antiField.getValue2() + self.compField.getValue2() + self.proField.getValue2() != 100:
            self.warning.setLabel('Error : Total Weighting Must Equal 100')
            self.warning.setBackgroundColor([1,0,0])
            self.color01.setBackgroundColor([1,0,0])
            self.color02.setBackgroundColor([1,0,0])
            print self.antiField.getValue2() + self.compField.getValue2() + self.proField.getValue2()
        else:
            self.warning.setLabel('')
            self.warning.setBackgroundColor([.68,.68,.68])
            self.color01.setBackgroundColor([.68,.68,.68])
            self.color02.setBackgroundColor([.68,.68,.68])
    
    def create(self):
       
        self.checkBox = pm.checkBox(label = 'Modify Weighting', ann= 'check to change the weighting of each section',onCommand = pm.Callback(self.editFields), offCommand = pm.Callback(self.editFields) )
        self.antiField = pm.intFieldGrp( numberOfFields=2, label='Antialias/Noise Quality', extraLabel = 'Weight %' , value2 = 45 , enable1 = False ,
                                        enable2 = False,  changeCommand=pm.Callback(self.updateTotal))
        self.compField = pm.intFieldGrp( numberOfFields=2, label='Composition/Focal Length', extraLabel = 'Weight %' , value2 = 45 , enable1 = False ,
                                        enable2 = False ,changeCommand=pm.Callback(self.updateTotal))
        self.proField = pm.intFieldGrp( numberOfFields=2, label='Professionalism', extraLabel = 'Weight %' ,value2 = 10 ,enable1 = False ,
                                       enable2 = False, changeCommand=pm.Callback(self.updateTotal))
        self.lateField = pm.intFieldGrp( numberOfFields=1, label='Late Deduction' , changeCommand=pm.Callback(self.updateTotal))
        self.totalField = pm.intFieldGrp( numberOfFields=1, label='Total Grade',enable1 = False, changeCommand=pm.Callback(self.updateTotal))
        self.radioButtons = pm.radioButtonGrp(columnWidth3 = [60,60,60] , width = 480, numberOfRadioButtons = 3, labelArray3 = ['1 day', '2 days', '3 days'], onCommand = pm.Callback(self.radioUpdate))
        
        # attaching the controls
        pm.formLayout( self.layout, edit=1, attachForm=[[self.checkBox, "left", 140], [self.checkBox, "top", 5]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.antiField ,"top", 40, self.checkBox], [self.antiField, "right", 10, self.checkBox]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.compField ,"top", 40, self.antiField], [self.compField, "right", 10, self.antiField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.proField ,"top", 40, self.compField], [self.proField, "right", 10, self.compField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.lateField ,"top", 40, self.proField], [self.lateField, "left", 0, self.proField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.totalField ,"top", 40, self.lateField], [self.totalField, "left", 0, self.lateField]])
        pm.formLayout( self.layout , edit=1, attachOppositeControl=[[self.radioButtons, "top", 40, self.proField],[self.radioButtons, "left", 250, self.proField]]) 
       
        pm.setParent(self.columnLayout)
        self.color01 = pm.text(label = '')
        self.warning = pm.text(label='')
        self.color02 = pm.text(label = '')
        #pm.button( label = 'Output Grade and Comment' , width = 480)
        return None 
        
    
        
    # this allows the percentage to be changed    
    def editFields(self):
        if self.checkBox.getValue() != 0:
            self.antiField.setEnable2(True)
            self.compField.setEnable2(True)
            self.proField.setEnable2(True)
        
        else :
            self.antiField.setEnable2(False)
            self.compField.setEnable2(False)
            self.proField.setEnable2(False)

   # this section will give access to the different fields so another section of the script can update them or getThem()
    def queryAnti(self):
        print self.antiField.getValue1()
        return self.antiField
    
    def queryComp(self):
        print self.compField.getValue1()
        return self.compField
    
    def queryPro(self):
        print self.proField.getValue1()
        return self.proField
    
    def queryLate(self):
        print self.lateField.getValue1()
        return self.lateField
    
    def queryTotal(self):
        print self.totalField.getValue1()
        return self.totalField
        
# the open images (file info) for each script
class Images():
    '''
    this class will create the upper section for the SAL grading scripts
    that section opens the images
    '''
    def __init__(self, update):
        
        self.update = update
        
        
        #------------------
        self.mainLayout = pm.columnLayout(adjustableColumn = True)
        pm.button(label = 'new image', ann = 'press to add as many images aa you want' , command = pm.Callback(self.createFields))
        self.openButtons = pm.radioButtonGrp(numberOfRadioButtons = 2 , columnAlign = [ 1 , 'center' ],label = ' Choose Program ', label1 = 'Preview',label2 = 'Photoshop')
        pm.button(label = 'open images', ann = 'this will open images with the selected programs', command = pm.Callback(self.openImage))
        pm.button(label = 'open reference', ann= 'this will only open a reference (with the selected program)', command = pm.Callback(self.openReference))
        pm.text(label= '')
        self.layout = pm.rowColumnLayout(nc=2 , cw =([1, 430], [2, 50]))
        
        # self.num is a number, which will be used to give unique names to the dynamically created fields
        self.num = 1
        # the list of the paths for the images
        self.imageList = []
        # this list will have the base name of all the images
        self.nameList = []
        
    def createFields(self):
        pm.setParent(self.layout)
        self.textField = pm.textFieldButtonGrp( 'text%s' % self.num , text='image to load', width = 430, buttonLabel='<<<', bc=pm.Callback(self.addImage, 'text%s' % self.num  ), ed=0 )
        self.button = pm.button('button%s' % self.num ,width = 50, label = 'X', command = pm.Callback(self.delete, 'text%s' % self.num,'button%s' % self.num ))
        self.num += 1
    
    def delete(self, text, button):
        # this section will remove the item associated with that UI from the two list
        # first it removes from the pathList then the nameList
        # it finds the 'string' in self.nameList and gets the index #
        # uses that # to remove the object at that index in the imageList
        toRemove = pm.textFieldButtonGrp(text, query= True, text= True)
        if toRemove in self.nameList:
            nameIndex = self.nameList.index(toRemove)
            print nameIndex
            print self.imageList[nameIndex]
            self.imageList.remove(self.imageList[nameIndex])
            self.nameList.remove(toRemove)
        # this will delete the UI elements
        pm.deleteUI(text)
        pm.deleteUI(button)
    
    def addImage(self, field):
        self.file = pm.fileDialog2(dialogStyle= 2, fileMode= 1)
        print self.file[0]
        self.newFile = os.path.basename(self.file[0])
        pm.textFieldButtonGrp('%s' % field, edit = True, text = '%s' % self.newFile )
        self.imageList.append(self.file[0])
        self.nameList.append(self.newFile)
        
        
        
    def openReference(self):
        self.ref = pm.fileDialog()
        if self.openButtons.getSelect() == 2:
            pm.util.shellOutput(r"open -a Adobe\ Photoshop\ CS5.1 %s " % self.ref)
            
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
            
        print self.queryNamesString()
        
        print self.update
        
        self.update.update(self.imageList)
        
    # this is just a way of getting all the names as a long string to use when outputting    
    def queryNamesString(self):
        x = 0
        self.blankSpace = ','
        self.name = ''
        while x < len(self.nameList):
            self.name += str(self.nameList[x]) + str(self.blankSpace)
            x += 1
        return self.name
    
    def queryNamesList(self):
        print self.nameList
        return self.nameList
    
    # this give access to the path so the output function can create the comment file in the right place
    def queryPath(self, index = 0):
        path = self.imageList[index]
        
        return path

        
# the first section
class Start():
    # starting class temp
    '''
    stuff
    
    '''
    def __init__(self):
        self.stuff = 'testing this out'
        print self.stuff
        print 'booya'
        print 'kasha'
        
    def create(self):
        self.mainLayout = pm.columnLayout(adjustableColumn = True)
        self.name = pm.textFieldGrp( label='Name', changeCommand= pm.Callback(self.writeOut),columnWidth2= (40,140))
        self.format = pm.textFieldGrp( label= 'Format', changeCommand= pm.Callback(self.writeOut), columnWidth2= (40,140))
        self.size = pm.intFieldGrp( label= 'Size', numberOfFields= 2, value1= 720, value2= 486, changeCommand= pm.Callback(self.writeOut),columnWidth3= (40,40,40) )
       
    def writeOut(self):
        dirPath = os.path.dirname(__file__)
        fileName = 'proj01_start'
        fullPath = os.path.join(dirPath, fileName)
        
        startFileOutput = shelve.open('%s' % fullPath , 'n')
        startFileOutput['name'] = ('%s' % self.name.getText())
        startFileOutput['format'] = ('%s' % self.format.getText().upper())
        startFileOutput['value1'] = ('%s' % self.size.getValue1())
        startFileOutput['value2'] = ('%s' % self.size.getValue2())
        
        startFileOutput.sync()
        
        print startFileOutput['name']
        print startFileOutput['format']
        print startFileOutput['value1']
        
        
        startFileOutput.close()
        
        #print self.name.getText(), self.format.getText().upper(), self.size.getValue1(), self.size.getValue2()
    
    def preFill(self):
        dirPath = os.path.dirname(__file__)
        fileName = 'proj01_start.db'
        fullPath = os.path.join(dirPath, fileName)
        
        if os.path.exists("%s" % fullPath):
            
            
            
            startFile = shelve.open('%s' % fullPath, 'r')
            
            print startFile
            
            print (startFile['name'])
            
            self.name.setText(str(startFile['name']))
            self.format.setText(str(startFile['format']))
            self.size.setValue1(int(startFile['value1']))
            self.size.setValue2(int(startFile['value2']))
            
            startFile.close()
        
        
    
    def queryName(self):
        return self.name
    
    def queryFormat(self):
        return self.format
    
    def querySize(self):
        return self.size
    
    
        
        
        
        
        




        