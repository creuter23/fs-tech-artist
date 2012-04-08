'''
* based on Tony's grading script

Author: Firmin Saint-Amour

Description: Module containing reusable pieces specifically for the shading
and lighting scripts

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

# radioCollection
class Radio_Collection():
    """
    this class creates the radio buttons for each grading section
    takes one arguement , field = field to update in a different section of the script, type= pymel object intFieldGrp
    
    field = which field to update
    toUpdate = the class instance that will be update (the UpperSection class)
    
    
    """
    def __init__(self, field, toUpdate):
        '''
        radioCollection
        '''
        self.field = field
        self.toUpdate = toUpdate
        
    def create(self):
        layout = pm.columnLayout(width= 90, adjustableColumn= False)
        self.radioCollection = pm.radioCollection()
        self.aField = pm.radioButton( label='A+ to A-', onCommand= pm.Callback(self.update, 100)  )
        self.bField = pm.radioButton( label='B+ to B-', onCommand= pm.Callback(self.update, 89)  )
        self.cField = pm.radioButton( label='C+ to C-', onCommand= pm.Callback(self.update, 79)  )
        self.dField = pm.radioButton( label='D', onCommand= pm.Callback(self.update, 72)  )
        self.fField = pm.radioButton( label='F', onCommand= pm.Callback(self.update, 69)  )
        pm.rowColumnLayout(nc=2, columnWidth= ([1,35], [2,55])) # total width 85
        pm.text( label= 'Grade', width= 35)
        self.gradeField = pm.intField(changeCommand= pm.Callback(self.output), width= 35 )
        
        return layout
        
        
    def update(self, value):
        self.gradeField.setValue(value)
        self.field.setValue1(self.gradeField.getValue())
        self.toUpdate.updateTotal()
        
    def output(self):
        value = self.gradeField.getValue()
        self.field.setValue1(value)
        self.toUpdate.updateTotal()
        
    def queryGrade(self):
        return self.gradeField
   
class Radio_Collection02(Radio_Collection):
    """
    this is based on Radio_Collection
    the only difference
    is this is in reverse
    A = 0
    F = 100
    because it will be used for deduction
    so A would mean 0 deduction
    """
    def create(self):
        layout = pm.columnLayout(width= 90, adjustableColumn= False)
        self.radioCollection = pm.radioCollection()
        self.aField = pm.radioButton( label='A+ to A-', onCommand= pm.Callback(self.update, 0)  )
        self.bField = pm.radioButton( label='B+ to B-', onCommand= pm.Callback(self.update, 25)  )
        self.cField = pm.radioButton( label='C+ to C-', onCommand= pm.Callback(self.update, 50)  )
        self.dField = pm.radioButton( label='D', onCommand= pm.Callback(self.update, 75)  )
        self.fField = pm.radioButton( label='F', onCommand= pm.Callback(self.update, 100)  )
        pm.rowColumnLayout(nc=2, columnWidth= ([1,35], [2,55])) # total width 85
        pm.text( label= 'Grade', width= 35)
        self.gradeField = pm.intField(changeCommand= pm.Callback(self.output), width= 35 )
        
        return layout
  
# checker options       
class Checker_Options():
    """
    this will create the section that will hold all the fields for the checker
    class
    
    fileName = the file that it will read when the script runs, so ir remembers
    what was in the fields teh last time
    
    """
    def __init__(self, fileName):
        self.fileName = fileName
        #print 'checker_options'
        
    def create(self):
        '''
        creates the gui components
        '''
        self.mainLayout = pm.columnLayout(adjustableColumn = True, width= 180)
        #pm.rowColumnLayout(numberOfColumns=2, columnWidth= ([1,40], [2,200]))
        self.name = pm.textFieldGrp( label='Name', changeCommand= pm.Callback(self.writeOut), columnWidth2= (40,140))
        self.format = pm.textFieldGrp( label= 'Format', changeCommand= pm.Callback(self.writeOut), columnWidth2= (40,140))
        self.size = pm.intFieldGrp( label= 'Size', numberOfFields= 2, value1= 720, value2= 486, changeCommand= pm.Callback(self.writeOut),columnWidth3= (40,70,70) )
        
    def writeOut(self):
        '''
        this will right out to the file so it remembers next time
        '''
        
        startFileOutput = shelve.open('%s' % self.fileName , 'n')
        startFileOutput['name'] = ('%s' % self.name.getText())
        startFileOutput['format'] = ('%s' % self.format.getText().upper())
        startFileOutput['value1'] = ('%s' % self.size.getValue1())
        startFileOutput['value2'] = ('%s' % self.size.getValue2())
        startFileOutput.sync()
       
        #print self.fileName
        #print startFileOutput['name'], startFileOutput['format'], startFileOutput['value1'], startFileOutput['value2']
        startFileOutput.close()
        
    def preFill(self):
        '''
        this will preFill the fields when the script runs
        '''
        # checking if the file exist 
        if os.path.exists("%s" % (self.fileName)):
            startFile = shelve.open('%s' % (self.fileName), 'r')
            #print startFile
            #print (startFile['name'])
            self.name.setText(str(startFile['name']))
            self.format.setText(str(startFile['format']))
            self.size.setValue1(int(startFile['value1']))
            self.size.setValue2(int(startFile['value2']))
            startFile.close()
            
    
    # these next functions return references of the fields so other classes
    # can access them / make changes
    def queryName(self):
        name = self.name
        return name
        
    def queryFormat(self):
        format = self.format
        return format
        
    def querySize(self):
        size = self.size
        return size
          
# checker info        
class Checker_Info():
    '''
    this will create the second have of the checker
    which is a scrollField
    the scroll field will keep a log of all the images that where opened
    
    '''
    def __init__(self):
        print "checker_info"
        
    # this creates the gui components
    # returns the scrollField so it can be placed
    def create(self):    
        self.scroll = pm.scrollField(width= 250, wordWrap= True)
        self.popup = pm.popupMenu(parent = self.scroll)
        pm.menuItem( label = 'Clear' , command = pm.Callback(self.clear))
        
        return self.scroll
    
    def clear(self):
        # this will clear the scrollField of any existing text
        self.scroll.setText('')
        
    
    def update(self,name, format, size):
        '''
        # this will update the 'log'(scroll field) 
        # takes the name of an image, the format, and the size
        '''
        self.scroll.insertText('%s\r\n' % name)
        self.scroll.insertText('%s\r\n' % format)
        self.scroll.insertText('%s X %s\r\n' % (size[0], size[1]))
        self.scroll.insertText('-----------\r\n')
               
# professionalism checker        
class Checker():
    """
    this combines the classes: Checker_Options and Checker_Info
    to create the checker section for each project
    # fileName = the start file used by the Checker_Info class
    
    """
    def __init__(self, fileName):
        self.fileName = fileName
        
        self.main = pm.columnLayout(adjustableColumn= True)
        self.frame = pm.frameLayout(label = 'checker', cll = True, cl = False, borderStyle = 'etchedIn', width = 480)
        self.layout = pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,185], [2,10], [3,270]))
        
        pm.text(label='Check')
        pm.text( label= '')
        pm.text(label='Image Log (recently opened)')
        pm.text(label= '')
        pm.text( label= '')
        pm.text(label= '')
        
    # creating the GUI components
    # returns none
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
        '''
        # this will update the 'log'(scroll field) from Checker_Info
        # takes a list of images (direct path to the image)
        '''
        # clearing the 'log' from it's previous use
        self.feedback.clear()
        
        for obj in objList:
            print obj
            image = Image.open('%s' % (obj))
            format = image.format
            size = image.size
            name = os.path.basename('%s' % (obj))
            self.feedback.update(name, format, size)
            
    
    # theses next methods will return references to the various components
    # so other classes/objects can have access & get data
    def queryName(self):
        #name = self.check.queryName()
        return self.check.queryName()
        
    def queryFormat(self):
        #format = self.check.queryFormat()
        return self.check.queryFormat()
        
    def querySize(self):
        size = self.check.querySize()
        return size
        
# grading section        
class Grading_Section():
    """
    this class combines the Radio_Collection and Comment_Widget classes
    to create the Grading_Section class
    
    name = the label for the section 
    field = field to update
    fileName = text file to read from
    toUpdate = which class instance 's update function will be invoked by the radioButtons
    or the integer (grade field) fields
    
    """
    # grading section
    def __init__(self, name, field, fileName, toUpdate):
        self.toUpdate = toUpdate
        self.name = name
        self.field = field
        self.file = fileName
        self.main = pm.columnLayout(adjustableColumn= True)
        self.frame = pm.frameLayout(label = self.name, cll = True, cl = False, borderStyle = 'etchedIn', width = 480)
        self.layout = pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,95], [2,10], [3,355]))
        #pm.setParent(self.layout)
        
        self.grading = pm.text(label='grading')
        pm.text( label= '')
        self.comments = pm.text(label='comments')
        pm.text(label= '')
        pm.text( label= '')
        pm.text(label= '')
        
    def create(self):
        '''
        creating the components
        '''
        
        self.grades = Radio_Collection(self.field, self.toUpdate)
        radio = self.grades.create()
        
        pm.setParent(self.layout)
        pm.text( label= '')
        self.scrollField = CommentWidget(width= 280, height= 120, fileName= self.file).create()
       
    def query(self):
        '''
        returns the text from the scroll fields, so the output function
        can use it
        '''
        return self.scrollField.getText()

class Grading_Section02(Grading_Section):
    '''
    this one uses Radio_Collection02 which is in reverse
    A = 0
    F = 100
    because it will be used for deductions
    '''
    def create(self):
        '''
        creating the components
        '''
        
        self.grades = Radio_Collection02(self.field, self.toUpdate)
        radio = self.grades.create()
        
        pm.setParent(self.layout)
        pm.text( label= '')
        self.scrollField = CommentWidget(width= 280, height= 120, fileName= self.file).create()
       
# grading section specifically for Professionliasm
# uses the Checker Class
class Grading_Prof():
    """
    grading section one-off specifically made for the professionalism section
    it will add the Checker class to itself. and work with it
    """
    def __init__(self, name, field, fileName, fileStart, toUpdate):
        self.toUpdate = toUpdate
        self.name = name
        self.field = field
        self.file = fileName
        self.fileStart = fileStart
        #self.objList = objList
        self.main = pm.columnLayout(adjustableColumn= True)
        self.frame = pm.frameLayout(label = self.name, cll = True, cl = False, borderStyle = 'etchedIn', width = 480)
        self.layout = pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,90], [2,10], [3,360]))
        #pm.setParent(self.layout)
        
        self.grading = pm.text(label='grading')
        pm.text( label= '')
        self.comments = pm.text(label='comments')
        pm.text(label= '')
        pm.text( label= '')
        pm.text(label= '')
        
    def create(self):
        # this will end up on the right
        self.grades = Radio_Collection(self.field, self.toUpdate)
        radio = self.grades.create()
        # setting parent so they dont end up under the Radio_Collection UIs
        
        pm.setParent(self.layout) 
        pm.text( label= '') # creating this for spacing also there are 3 rows
        self.scrollField = CommentWidget(width= 280, height= 120, fileName= self.file).create()
        pm.setParent(self.frame)
        
        self.checker = Checker(self.fileStart)
        self.checker.create()
        
        
    
    def update(self, objList):
        '''
        this function will automatically update the gradeField from
        the RadioCollection class
        it will use the chcker class to check for naming, format, and size
        '''
        self.grades.queryGrade().setValue(100)
        self.scrollField.clear()
        self.checker.update(objList)
        myGrade = 100
        
        # this loop checks the name and if it doesnt match the name from 
        # the checker class it deducts 25
        # points from the grading field (Radio_Collection class)   
        # it will stop at the first encounter of something wrong
         
        for obj in objList:
            myImage = Image.open('%s' % obj)
            # getting the name from the checker
            myName = self.checker.queryName().getText()
            
            
            if '%s' % (myName) not in '%s' % (obj):
                myGrade -= 25
                self.grades.queryGrade().setValue(myGrade)
                #print myName, obj, myGrade
                break
        
        # this loop checks the format and if it doesnt match the format from 
        # the checker class it deducts 25
        # points from the grading field (Radio_Collection class)    
        # it will stop at the first encounter of something wrong
        
        for obj in objList:
            myImage = Image.open('%s' % obj)
            # getting the format from the checker
            format = self.checker.queryFormat().getText().upper()
            #print format
            
            myFormat = myImage.format
            
            if '%s' % (format) not in myFormat:
                myGrade -= 25
                self.grades.queryGrade().setValue(myGrade)
                #print myFormat, obj, myGrade
                break
            
        # this loop checks the size and if it doesnt match the size from 
        # the checker class it deducts 25
        # points from the grading field (Radio_Collection class)    
        # it will stop at the first encounter of something wrong
        
        for obj in objList:
            myImage = Image.open('%s' % obj)
            # getting the size from the checker
            size = self.checker.querySize()
            #print size
            
            mySize = myImage.size
            
            if size.getValue1() != mySize[0] or size.getValue2() != mySize[1]:
                myGrade -= 25
                self.grades.queryGrade().setValue(myGrade)
                #print mySize, obj, myGrade
                break
            
        self.field.setValue1(myGrade)
        self.toUpdate.updateTotal()
        
        # this next section will see if anything doesnt match and
        # take that info to the scroll field for outputting
        # so the students know which files had the wrong format, size, and name
        for obj in objList:
            myImage = Image.open('%s' % obj)
            mySize = myImage.size
            myFormat = myImage.format
            # getting the name from the checker
            myName = self.checker.queryName().getText()
            size = self.checker.querySize()
            format = self.checker.queryFormat().getText().upper()
            
            
            if '%s' % (myName) not in '%s' % (obj):
                self.insertText('wrong name: %s\r\n' % (os.path.basename(obj)) )
                self.insertText('--------------\r\n')
                
            if size.getValue1() != mySize[0] or size.getValue2() != mySize[1]:
                self.insertText('wrong size: %s\r\n' % (os.path.basename(obj)))
                self.insertText('expected %s X %s, got %s X %s\r\n' % (size.getValue1(), size.getValue2(), mySize[0], mySize[1]))
                self.insertText('--------------\r\n')
                
            if '%s' % (format) not in myFormat:
                self.insertText('wrong format: %s\r\n' % (os.path.basename(obj)))
                self.insertText('expected %s, got %s\r\n' % (format, myFormat))
                self.insertText('--------------\r\n')
                
                
            
            
    def insertText(self, text):
        # this will get some text and insert it into the scroll field
        # the update method uses it
        self.scrollField.insertText(text)
        
    
    def query(self):
        # this will return the text from the scrollField for outputting
        return self.scrollField.getText()
           
class Grading_Prof02(Grading_Prof):
    '''
    this one uses Radio_Collection02 which is in reverse
    A = 0
    F = 100
    because it will be used for deductions
    '''
    def create(self):
        # this will end up on the right
        self.grades = Radio_Collection02(self.field, self.toUpdate)
        radio = self.grades.create()
        # setting parent so they dont end up under the Radio_Collection UIs
        
        pm.setParent(self.layout) 
        pm.text( label= '') # creating this for spacing also there are 3 rows
        self.scrollField = CommentWidget(width= 280, height= 120, fileName= self.file).create()
        pm.setParent(self.frame)
        
        self.checker = Checker(self.fileStart)
        self.checker.create()
        
    def update(self, objList):
        '''
        this function will automatically update the gradeField from
        the RadioCollection class
        it will use the chcker class to check for naming, format, and size
        '''
        self.grades.queryGrade().setValue(0)
        self.scrollField.clear()
        self.checker.update(objList)
        myGrade = 0
        
        # this loop checks the name and if it doesnt match the name from 
        # the checker class it adds 25
        # points from the grading field (Radio_Collection class)   
        # it will stop at the first encounter of something wrong
         
        for obj in objList:
            myImage = Image.open('%s' % obj)
            # getting the name from the checker
            myName = self.checker.queryName().getText()
            
            
            if '%s' % (myName) not in '%s' % (obj):
                myGrade += 25
                self.grades.queryGrade().setValue(myGrade)
                #print myName, obj, myGrade
                break
        
        # this loop checks the format and if it doesnt match the format from 
        # the checker class it adds 25
        # points from the grading field (Radio_Collection class)    
        # it will stop at the first encounter of something wrong
        
        for obj in objList:
            myImage = Image.open('%s' % obj)
            # getting the format from the checker
            format = self.checker.queryFormat().getText().upper()
            #print format
            
            myFormat = myImage.format
            
            if '%s' % (format) not in myFormat:
                myGrade += 25
                self.grades.queryGrade().setValue(myGrade)
                #print myFormat, obj, myGrade
                break
            
        # this loop checks the size and if it doesnt match the size from 
        # the checker class it adds 25
        # points from the grading field (Radio_Collection class)    
        # it will stop at the first encounter of something wrong
        
        for obj in objList:
            myImage = Image.open('%s' % obj)
            # getting the size from the checker
            size = self.checker.querySize()
            #print size
            
            mySize = myImage.size
            
            if size.getValue1() != mySize[0] or size.getValue2() != mySize[1]:
                myGrade += 25
                self.grades.queryGrade().setValue(myGrade)
                #print mySize, obj, myGrade
                break
            
        self.field.setValue1(myGrade)
        self.toUpdate.updateTotal()
        
        # this next section will see if anything doesnt match and
        # take that info to the scroll field for outputting
        # so the students know which files had the wrong format, size, and name
        for obj in objList:
            myImage = Image.open('%s' % obj)
            mySize = myImage.size
            myFormat = myImage.format
            # getting the name from the checker
            myName = self.checker.queryName().getText()
            size = self.checker.querySize()
            format = self.checker.queryFormat().getText().upper()
            
            
            if '%s' % (myName) not in '%s' % (obj):
                self.insertText('wrong name: %s\r\n' % (os.path.basename(obj)) )
                self.insertText('--------------\r\n')
                
            if size.getValue1() != mySize[0] or size.getValue2() != mySize[1]:
                self.insertText('wrong size: %s\r\n' % (os.path.basename(obj)))
                self.insertText('expected %s X %s, got %s X %s\r\n' % (size.getValue1(), size.getValue2(), mySize[0], mySize[1]))
                self.insertText('--------------\r\n')
                
            if '%s' % (format) not in myFormat:
                self.insertText('wrong format: %s\r\n' % (os.path.basename(obj)))
                self.insertText('expected %s, got %s\r\n' % (format, myFormat))
                self.insertText('--------------\r\n')
                   
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
        # this will insert text into the scroll field
        self.scrollField.insertText(comment, insertionPosition = 0)
        self.scrollField.setBackgroundColor([1,1,0])
        
    def clear(self):
        # this will clear the scrollField of any existing text
        self.scrollField.setText('')
        self.scrollField.setBackgroundColor([1,0,0])
        
    def custom(self):
        '''
        this will create a window with an existing scrollField
        for custom commetns
        '''
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
        '''
        this will add the custom comment to the scrollField
        '''
        
        self.scrollField.insertText(self.customComment.getText())
        
        self.scrollField.setBackgroundColor([0,1,0])
        
        # deleting the window
        pm.deleteUI(self.customWin)
        
        self.menus()
       
    def saveComment(self):
        # this will add the comment to the selected file 
        self.customFeedback.setLabel('%s added to file' % self.customLabel.getText())
        self.writeFile = open(self.fileName , 'a')
        #print self.customLabel.getText()
        self.writeFile.write(self.customLabel.getText() + '\n')
        #print self.customComment.getText()
        self.writeFile.write(self.customComment.getText() + '\n')
        self.writeFile.close()
        self.menus()
            
# the total grade section for each Script
class Total_Grades():
    
    '''
    creates the summary section that has all the final grades and the output button
    '''
    def __init__(self, width = 480):
        self.width = width
        pm.frameLayout(label = 'Total Grades', cll = True, cl = True, borderStyle = 'etchedIn', width = self.width)
        self.columnLayout = pm.columnLayout( adjustableColumn=True , width= 480 )
        self.layout = pm.formLayout()
    
    # command for the radioButtons that connect  to the late deduction field
    def radioUpdate(self):
        # this will update the total grade field based on which button is selected
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
    # it also checks to make sure the weighting == to 100
    # if not it gives an indication
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
        '''
        creating the different components
        '''
        self.text = pm.text(label = '' )
        self.antiField = pm.intFieldGrp( numberOfFields=2, label='Antialias/Noise Quality', extraLabel = 'Weight %' , value2 = 45 , enable1 = True ,
                                        enable2 = True,  changeCommand=pm.Callback(self.updateTotal))
        self.compField = pm.intFieldGrp( numberOfFields=2, label='Composition/Focal Length', extraLabel = 'Weight %' , value2 = 45 , enable1 = True ,
                                        enable2 = True ,changeCommand=pm.Callback(self.updateTotal))
        self.proField = pm.intFieldGrp( numberOfFields=2, label='Professionalism', extraLabel = 'Weight %' ,value2 = 10 ,enable1 = True ,
                                       enable2 = True, changeCommand=pm.Callback(self.updateTotal))
        self.lateField = pm.intFieldGrp( numberOfFields=1, label='Late Deduction' , changeCommand=pm.Callback(self.updateTotal))
        self.totalField = pm.intFieldGrp( numberOfFields=1, label='Total Grade',enable1 = True, changeCommand=pm.Callback(self.updateTotal))
        self.radioButtons = pm.radioButtonGrp(columnWidth3 = [60,60,60] , width = 480, numberOfRadioButtons = 3, labelArray3 = ['1 day', '2 days', '3 days'], onCommand = pm.Callback(self.radioUpdate))
        
        # attaching the controls
        pm.formLayout( self.layout, edit=1, attachForm=[[self.text, "left", 140], [self.text, "top", 5]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.antiField ,"top", 10, self.text], [self.antiField, "right", 10, self.text]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.compField ,"top", 30, self.antiField], [self.compField, "right", 10, self.antiField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.proField ,"top", 30, self.compField], [self.proField, "right", 10, self.compField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.lateField ,"top", 30, self.proField], [self.lateField, "left", 0, self.proField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.totalField ,"top", 30, self.lateField], [self.totalField, "left", 0, self.lateField]])
        pm.formLayout( self.layout , edit=1, attachOppositeControl=[[self.radioButtons, "top", 30, self.proField],[self.radioButtons, "left", 250, self.proField]]) 
       
        pm.setParent(self.columnLayout)
        # these are the labels that will give a warning if the percentage != 100
        self.color01 = pm.text(label = '') 
        self.warning = pm.text(label='')
        self.color02 = pm.text(label = '')
       
        return None 
        
    

   # this section will give access to the different fields so another section of the script can update them or getThem()
    def queryAnti(self):
        #print self.antiField.getValue1()
        return self.antiField
    
    def queryComp(self):
        #print self.compField.getValue1()
        return self.compField
    
    def queryPro(self):
        #print self.proField.getValue1()
        return self.proField
    
    def queryLate(self):
        #print self.lateField.getValue1()
        return self.lateField
    
    def queryTotal(self):
        #print self.totalField.getValue1()
        return self.totalField

# this one is for project02 and  project03        
class Total_Grades02(Total_Grades):
    '''
    based on class Total_Grades meant to be used for project02 and project03
    '''
    def create(self):
       
        self.text = pm.text(label = '' )
        self.lightField = pm.intFieldGrp( numberOfFields=2, label='Lighting', extraLabel = 'Weight %' , value2 = 100 , enable1 = True ,
                                        enable2 = True,  changeCommand=pm.Callback(self.updateTotal))
        self.antiField = pm.intFieldGrp( numberOfFields=2, label='Antialias/Noise Quality', extraLabel = 'Deduction %' , value2 = 15 , enable1 = True ,
                                        enable2 = True,  changeCommand=pm.Callback(self.updateTotal))
        self.compField = pm.intFieldGrp( numberOfFields=2, label='Composition/Focal Length', extraLabel = 'Deduction %' , value2 = 15 , enable1 = True ,
                                        enable2 = True ,changeCommand=pm.Callback(self.updateTotal))
        self.proField = pm.intFieldGrp( numberOfFields=2, label='Professionalism', extraLabel = 'Deduction %' ,value2 = 10 ,enable1 = True ,
                                       enable2 = True, changeCommand=pm.Callback(self.updateTotal))
        self.lateField = pm.intFieldGrp( numberOfFields=1, label='Late Deduction' , changeCommand=pm.Callback(self.updateTotal))
        self.totalField = pm.intFieldGrp( numberOfFields=1, label='Total Grade',enable1 = True, changeCommand=pm.Callback(self.updateTotal))
        self.radioButtons = pm.radioButtonGrp(columnWidth3 = [60,60,60] , width = 480, numberOfRadioButtons = 3, labelArray3 = ['1 day', '2 days', '3 days'], onCommand = pm.Callback(self.radioUpdate))
        
        # attaching the controls
        pm.formLayout( self.layout, edit=1, attachForm=[[self.text, "left", 140], [self.text, "top", 5]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.lightField ,"top", 10, self.text], [self.lightField, "right", 10, self.text]])
        
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.compField ,"top", 30, self.lightField], [self.compField, "right", 10, self.lightField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.antiField ,"top", 30, self.compField], [self.antiField, "right", 10, self.compField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.proField ,"top", 30, self.antiField], [self.proField, "right", 10, self.antiField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.lateField ,"top", 30, self.proField], [self.lateField, "left", 0, self.proField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.totalField ,"top", 30, self.lateField], [self.totalField, "left", 0, self.lateField]])
        pm.formLayout( self.layout , edit=1, attachOppositeControl=[[self.radioButtons, "top", 30, self.proField],[self.radioButtons, "left", 250, self.proField]]) 
       
        pm.setParent(self.columnLayout)
        self.color01 = pm.text(label = '')
        self.warning = pm.text(label='')
        self.color02 = pm.text(label = '')
        #pm.button( label = 'Output Grade and Comment' , width = 480)
        return None 
    
    def updateTotal(self):
        
        
        grade = (self.lightField.getValue1() /  float(100) * self.lightField.getValue2())
        deduction = (self.compField.getValue1() /  float(100) * self.compField.getValue2() +
                     self.proField.getValue1() /  float(100) * self.proField.getValue2() +
                     self.antiField.getValue1() /  float(100) * self.antiField.getValue2())
        late = self.lateField.getValue1()
        total = grade - deduction - late
        
        self.totalField.setValue1(int(total))
        
        if self.lightField.getValue2() != 100:
            self.warning.setLabel('Error : Total Weighting Must Equal 100')
            self.warning.setBackgroundColor([1,0,0])
            self.color01.setBackgroundColor([1,0,0])
            self.color02.setBackgroundColor([1,0,0])
            #print self.lightField.getValue2()
        else:
            self.warning.setLabel('')
            self.warning.setBackgroundColor([.68,.68,.68])
            self.color01.setBackgroundColor([.68,.68,.68])
            self.color02.setBackgroundColor([.68,.68,.68])
            
    def queryLight(self):
        #print self.lightField.getValue1()
        return self.lightField

# for project04, project07, and the Final project
class Total_Grades03(Total_Grades02):
    '''
    based on class Total_Grades02 meant to be used for project04
    '''
    def create(self):
       
        self.text = pm.text(label = '' )
        self.lightField = pm.intFieldGrp( numberOfFields=2, label='Lighting', extraLabel = 'Weight %' , value2 = 50 , enable1 = True ,
                                        enable2 = True,  changeCommand=pm.Callback(self.updateTotal))
        self.matField = pm.intFieldGrp( numberOfFields=2, label='Materials/Textures', extraLabel = 'Weight %' , value2 = 50 , enable1 = True ,
                                        enable2 = True,  changeCommand=pm.Callback(self.updateTotal))
        self.antiField = pm.intFieldGrp( numberOfFields=2, label='Antialias/Noise Quality', extraLabel = 'Deduction %' , value2 = 10 , enable1 = True ,
                                        enable2 = True,  changeCommand=pm.Callback(self.updateTotal))
        self.compField = pm.intFieldGrp( numberOfFields=2, label='Composition/Focal Length', extraLabel = 'Deduction %' , value2 = 10 , enable1 = True ,
                                        enable2 = True ,changeCommand=pm.Callback(self.updateTotal))
        self.proField = pm.intFieldGrp( numberOfFields=2, label='Professionalism', extraLabel = 'Deduction %' ,value2 = 10 ,enable1 = True ,
                                       enable2 = True, changeCommand=pm.Callback(self.updateTotal))
        self.lateField = pm.intFieldGrp( numberOfFields=1, label='Late Deduction' , changeCommand=pm.Callback(self.updateTotal))
        self.totalField = pm.intFieldGrp( numberOfFields=1, label='Total Grade',enable1 = True, changeCommand=pm.Callback(self.updateTotal))
        self.radioButtons = pm.radioButtonGrp(columnWidth3 = [60,60,60] , width = 480, numberOfRadioButtons = 3, labelArray3 = ['1 day', '2 days', '3 days'], onCommand = pm.Callback(self.radioUpdate))
        
        # attaching the controls
        pm.formLayout( self.layout, edit=1, attachForm=[[self.text, "left", 140], [self.text, "top", 5]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.lightField ,"top", 10, self.text], [self.lightField, "right", 10, self.text]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.matField ,"top", 30, self.lightField], [self.matField, "right", 10, self.lightField]])
        
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.compField ,"top", 30, self.matField], [self.compField, "right", 10, self.matField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.antiField ,"top", 30, self.compField], [self.antiField, "right", 10, self.compField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.proField ,"top", 30, self.antiField], [self.proField, "right", 10, self.antiField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.lateField ,"top", 30, self.proField], [self.lateField, "left", 0, self.proField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.totalField ,"top", 30, self.lateField], [self.totalField, "left", 0, self.lateField]])
        pm.formLayout( self.layout , edit=1, attachOppositeControl=[[self.radioButtons, "top", 30, self.proField],[self.radioButtons, "left", 250, self.proField]]) 
       
        pm.setParent(self.columnLayout)
        self.color01 = pm.text(label = '')
        self.warning = pm.text(label='')
        self.color02 = pm.text(label = '')
        return None
    
    def updateTotal(self):
        
        
        grade = (self.lightField.getValue1() /  float(100) * self.lightField.getValue2() + self.matField.getValue1() /  float(100) * self.matField.getValue2())
        deduction = (self.compField.getValue1() /  float(100) * self.compField.getValue2() +
                     self.proField.getValue1() /  float(100) * self.proField.getValue2() +
                     self.antiField.getValue1() /  float(100) * self.antiField.getValue2())
        late = self.lateField.getValue1()
        total = grade - deduction - late
        
        self.totalField.setValue1(int(total))
        
        if self.lightField.getValue2() + self.matField.getValue2() != 100:
            self.warning.setLabel('Error : Total Weighting Must Equal 100')
            self.warning.setBackgroundColor([1,0,0])
            self.color01.setBackgroundColor([1,0,0])
            self.color02.setBackgroundColor([1,0,0])
            #print self.lightField.getValue2()
        else:
            self.warning.setLabel('')
            self.warning.setBackgroundColor([.68,.68,.68])
            self.color01.setBackgroundColor([.68,.68,.68])
            self.color02.setBackgroundColor([.68,.68,.68])
            
    def queryLight(self):
        #print self.lightField.getValue1()
        return self.lightField
    
    def queryMat(self):
       # print self.matField.getValue1()
        return self.matField

# for porject05
class Total_Grades04(Total_Grades03):
    '''
    based on class Total_Grades03 meant to be used for project05
    '''
    def create(self):
       
        self.text = pm.text(label = '' )
        self.lightField = pm.intFieldGrp( numberOfFields=2, label='Lighting', extraLabel = 'Weight %' , value2 = 30 , enable1 = True ,
                                        enable2 = True,  changeCommand=pm.Callback(self.updateTotal))
        self.matField = pm.intFieldGrp( numberOfFields=2, label='Materials/Textures', extraLabel = 'Weight %' , value2 = 30 , enable1 = True ,
                                        enable2 = True,  changeCommand=pm.Callback(self.updateTotal))
        self.rayField = pm.intFieldGrp( numberOfFields=2, label='Raytracing', extraLabel = 'Weight %' , value2 = 40 , enable1 = True ,
                                        enable2 = True,  changeCommand=pm.Callback(self.updateTotal))
        self.antiField = pm.intFieldGrp( numberOfFields=2, label='Antialias/Noise Quality', extraLabel = 'Deduction %' , value2 = 10 , enable1 = True ,
                                        enable2 = True,  changeCommand=pm.Callback(self.updateTotal))
        self.compField = pm.intFieldGrp( numberOfFields=2, label='Composition/Focal Length', extraLabel = 'Deduction %' , value2 = 10 , enable1 = True ,
                                        enable2 = True ,changeCommand=pm.Callback(self.updateTotal))
        self.proField = pm.intFieldGrp( numberOfFields=2, label='Professionalism', extraLabel = 'Deduction %' ,value2 = 10 ,enable1 = True ,
                                       enable2 = True, changeCommand=pm.Callback(self.updateTotal))
        self.lateField = pm.intFieldGrp( numberOfFields=1, label='Late Deduction' , changeCommand=pm.Callback(self.updateTotal))
        self.totalField = pm.intFieldGrp( numberOfFields=1, label='Total Grade',enable1 = True, changeCommand=pm.Callback(self.updateTotal))
        self.radioButtons = pm.radioButtonGrp(columnWidth3 = [60,60,60] , width = 480, numberOfRadioButtons = 3, labelArray3 = ['1 day', '2 days', '3 days'], onCommand = pm.Callback(self.radioUpdate))
        
        # attaching the controls
        pm.formLayout( self.layout, edit=1, attachForm=[[self.text, "left", 140], [self.text, "top", 5]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.lightField ,"top", 10, self.text], [self.lightField, "right", 10, self.text]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.matField ,"top", 30, self.lightField], [self.matField, "right", 10, self.lightField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.rayField ,"top", 30, self.matField], [self.rayField, "right", 10, self.matField]])
        
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.compField ,"top", 30, self.rayField], [self.compField, "right", 10, self.rayField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.antiField ,"top", 30, self.compField], [self.antiField, "right", 10, self.compField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.proField ,"top", 30, self.antiField], [self.proField, "right", 10, self.antiField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.lateField ,"top", 30, self.proField], [self.lateField, "left", 0, self.proField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.totalField ,"top", 30, self.lateField], [self.totalField, "left", 0, self.lateField]])
        pm.formLayout( self.layout , edit=1, attachOppositeControl=[[self.radioButtons, "top", 30, self.proField],[self.radioButtons, "left", 250, self.proField]]) 
       
        pm.setParent(self.columnLayout)
        self.color01 = pm.text(label = '')
        self.warning = pm.text(label='')
        self.color02 = pm.text(label = '')
        
        return None
    
    def updateTotal(self):
        
        
        grade = (self.lightField.getValue1() /  float(100) * self.lightField.getValue2()
                 + self.matField.getValue1() /  float(100) * self.matField.getValue2()
                 + self.rayField.getValue1() /  float(100) * self.rayField.getValue2())
        
        deduction = (self.compField.getValue1() /  float(100) * self.compField.getValue2() +
                     self.proField.getValue1() /  float(100) * self.proField.getValue2() +
                     self.antiField.getValue1() /  float(100) * self.antiField.getValue2())
        
        late = self.lateField.getValue1()
        
        total = grade - deduction - late
        
        self.totalField.setValue1(int(total))
        
        if self.lightField.getValue2() + self.matField.getValue2() + self.rayField.getValue2() != 100:
            self.warning.setLabel('Error : Total Weighting Must Equal 100')
            self.warning.setBackgroundColor([1,0,0])
            self.color01.setBackgroundColor([1,0,0])
            self.color02.setBackgroundColor([1,0,0])
            #print self.lightField.getValue2()
        
        else:
            self.warning.setLabel('')
            self.warning.setBackgroundColor([.68,.68,.68])
            self.color01.setBackgroundColor([.68,.68,.68])
            self.color02.setBackgroundColor([.68,.68,.68])
    
    def queryRay(self):
        #print self.rayField.getValue1()
        return self.rayField

# for project06
class Total_Grades05(Total_Grades04):
    '''
    based on class Total_Grades04 meant to be used for project06
    '''
    def create(self):
       
        self.text = pm.text(label = '' )
        self.lightField = pm.intFieldGrp( numberOfFields=2, label='Lighting', extraLabel = 'Weight %' , value2 = 34 , enable1 = True ,
                                        enable2 = True,  changeCommand=pm.Callback(self.updateTotal))
        self.matField = pm.intFieldGrp( numberOfFields=2, label='Materials/Textures', extraLabel = 'Weight %' , value2 = 33 , enable1 = True ,
                                        enable2 = True,  changeCommand=pm.Callback(self.updateTotal))
        self.rayField = pm.intFieldGrp( numberOfFields=2, label='Raytracing', extraLabel = 'Weight %' , value2 = 33 , enable1 = True ,
                                        enable2 = True,  changeCommand=pm.Callback(self.updateTotal))
        self.antiField = pm.intFieldGrp( numberOfFields=2, label='Antialias/Noise Quality', extraLabel = 'Deduction %' , value2 = 10 , enable1 = True ,
                                        enable2 = True,  changeCommand=pm.Callback(self.updateTotal))
        self.compField = pm.intFieldGrp( numberOfFields=2, label='Composition/Focal Length', extraLabel = 'Deduction %' , value2 = 10 , enable1 = True ,
                                        enable2 = True ,changeCommand=pm.Callback(self.updateTotal))
        self.proField = pm.intFieldGrp( numberOfFields=2, label='Professionalism', extraLabel = 'Deduction %' ,value2 = 10 ,enable1 = True ,
                                       enable2 = True, changeCommand=pm.Callback(self.updateTotal))
        self.lateField = pm.intFieldGrp( numberOfFields=1, label='Late Deduction' , changeCommand=pm.Callback(self.updateTotal))
        self.totalField = pm.intFieldGrp( numberOfFields=1, label='Total Grade',enable1 = True, changeCommand=pm.Callback(self.updateTotal))
        self.radioButtons = pm.radioButtonGrp(columnWidth3 = [60,60,60] , width = 480, numberOfRadioButtons = 3, labelArray3 = ['1 day', '2 days', '3 days'], onCommand = pm.Callback(self.radioUpdate))
        
        # attaching the controls
        pm.formLayout( self.layout, edit=1, attachForm=[[self.text, "left", 140], [self.text, "top", 5]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.lightField ,"top", 10, self.text], [self.lightField, "right", 10, self.text]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.matField ,"top", 30, self.lightField], [self.matField, "right", 10, self.lightField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.rayField ,"top", 30, self.matField], [self.rayField, "right", 10, self.matField]])
        
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.compField ,"top", 30, self.rayField], [self.compField, "right", 10, self.rayField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.antiField ,"top", 30, self.compField], [self.antiField, "right", 10, self.compField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.proField ,"top", 30, self.antiField], [self.proField, "right", 10, self.antiField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.lateField ,"top", 30, self.proField], [self.lateField, "left", 0, self.proField]])
        pm.formLayout( self.layout, edit=1, attachOppositeControl=[[self.totalField ,"top", 30, self.lateField], [self.totalField, "left", 0, self.lateField]])
        pm.formLayout( self.layout , edit=1, attachOppositeControl=[[self.radioButtons, "top", 30, self.proField],[self.radioButtons, "left", 250, self.proField]]) 
       
        pm.setParent(self.columnLayout)
        self.color01 = pm.text(label = '')
        self.warning = pm.text(label='')
        self.color02 = pm.text(label = '')
        
        return None
    
# this will open images (file info) for each script
class Images():
    '''
    this class will create the upper section for the SAL grading scripts
    that section opens the images
    
    it takes an object to update
    it takes speciafically an instance of the  Grading_Prof class
    it will give it a list of the images it opened
    so the Checker (checking system) can work 
    
    '''
    def __init__(self, update, width = 480):
        self.width = width
        self.update = update
        
        
        #------------------
        pm.frameLayout(label = 'File Info', cll = True, cl = False, borderStyle = 'etchedIn', width = self.width)
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
        
    # this will dynmically create the fields
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
        # this will add the selected images from the file dialog
        # add it to the image list
        # and do an edit on the field and add the base name to the field
        
        # takes a text field button group
        # returns nothing
        self.file = pm.fileDialog2(dialogStyle= 2, fileMode= 1)
        print self.file[0]
        self.newFile = os.path.basename(self.file[0])
        pm.textFieldButtonGrp('%s' % field, edit = True, text = '%s' % self.newFile )
        self.imageList.append(self.file[0])
        self.nameList.append(self.newFile)
        
        
        
    def openReference(self):
        # this will open the image from the file dialog with the selected app
        self.ref = pm.fileDialog2(dialogStyle= 2, fileMode= 1)
        
        # button 2 for photoshop
        if self.openButtons.getSelect() == 2:
            pm.util.shellOutput(r"open -a Adobe\ Photoshop\ CS5.1 %s " % self.ref)
        
        # buttton 1 for preview    
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
            self.path += str(self.imageList[x]) + str(self.blank)
            x += 1
        
        # this will check to see which program to open the images with
        if self.openButtons.getSelect() == 2:
            pm.util.shellOutput(r"open -a Adobe\ Photoshop\ CS5.1 %s " % self.path)
            
        if self.openButtons.getSelect() == 1:
            pm.util.shellOutput(r"open  %s " % self.path)
            
        print self.queryNamesString(), self.path
        
        
        
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
    
    # this will return the list of base names
    def queryNamesList(self):
        print self.nameList
        return self.nameList
    
    # this give access to the path so the output function can create the
    # comment file in the right place
    # it returns the path to the first image in the list
    def queryPath(self, index = 0):
        path = self.imageList[index]
        
        return path

class Images02(Images):
    '''
    this class will create the upper section for the SAL grading scripts
    that section opens the images
    
    it takes an object to update
    it takes speciafically an instance of the  Grading_Prof class
    it will give it a list of the images it opened
    so the Checker (checking system) can work
    
    * this version will open a reference image from a folder
    
    '''
    def __init__(self, update, image, width = 480):
        self.width = width
        self.update = update
        self.image = image # the image teh reference button will open
        
        
        #------------------
        pm.frameLayout(label = 'File Info', cll = True, cl = False, borderStyle = 'etchedIn', width = self.width)
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
    
    def openReference(self):
        # this will open the image from the file dialog with the selected app
        
        
        # button 2 for photoshop
        if self.openButtons.getSelect() == 2:
            
            pm.util.shellOutput(r"open -a Adobe\ Photoshop\ CS5.1 %s" % (self.image))
            
        
        # buttton 1 for preview    
        if self.openButtons.getSelect() == 1:
            
            pm.util.shellOutput(r"open  %s" % (self.image))
    
# for the final project   
class Images03(Images):
    def __init__(self, update, image01, image02, image03, image04, width = 480):
        self.width = width
        self.update = update
        self.image01 = image01 # the image teh reference button will open
        self.image02 = image02
        self.image03 = image03
        self.image04 = image04
        
        
        #------------------
        pm.frameLayout(label = 'File Info', cll = True, cl = False, borderStyle = 'etchedIn', width = self.width)
        self.mainLayout = pm.columnLayout(adjustableColumn = True)
        pm.button(label = 'new image', ann = 'press to add as many images aa you want' , command = pm.Callback(self.createFields))
        self.openButtons = pm.radioButtonGrp(numberOfRadioButtons = 2 , columnAlign = [ 1 , 'center' ],
                            label = ' Choose Program ', label1 = 'Preview',label2 = 'Photoshop')
        pm.button(label = 'open images', ann = 'this will open images with the selected programs', command = pm.Callback(self.openImage))
        self.refButtons = pm.radioButtonGrp(numberOfRadioButtons = 4 , columnAlign = [ 1 , 'center' ],
                    label= 'Choose Reference', label1= 'Museum',label2= 'Bathroom',
                    label3= 'Sci-fi', label4= 'Staircase', columnWidth5= [120, 90, 90, 90, 90])
        pm.button(label = 'open reference', ann= 'this will only open a reference (with the selected program)', command = pm.Callback(self.openReference))
        pm.text(label= '')
        self.layout = pm.rowColumnLayout(nc=2 , cw =([1, 430], [2, 50]))
        
        # self.num is a number, which will be used to give unique names to the dynamically created fields
        self.num = 1
        # the list of the paths for the images
        self.imageList = []
        # this list will have the base name of all the images
        self.nameList = []
        
    def openReference(self):
        # this will open the image from the file dialog with the selected app
        
        
        # button 2 for photoshop
        if self.openButtons.getSelect() == 2:
            
            if self.refButtons.getSelect() == 1:
                pm.util.shellOutput(r"open -a Adobe\ Photoshop\ CS5.1 %s" % (self.image01))
                
            if self.refButtons.getSelect() == 2:
                pm.util.shellOutput(r"open -a Adobe\ Photoshop\ CS5.1 %s" % (self.image02))
                
            if self.refButtons.getSelect() == 3:
                pm.util.shellOutput(r"open -a Adobe\ Photoshop\ CS5.1 %s" % (self.image03))
                
            if self.refButtons.getSelect() == 4:
                pm.util.shellOutput(r"open -a Adobe\ Photoshop\ CS5.1 %s" % (self.image04))
            
        
        # buttton 1 for preview    
        if self.openButtons.getSelect() == 1:
            
            if self.refButtons.getSelect() == 1:
                pm.util.shellOutput(r"open  %s" % (self.image01))
                
            if self.refButtons.getSelect() == 2:
                pm.util.shellOutput(r"open  %s" % (self.image02))
                
            if self.refButtons.getSelect() == 3:
                pm.util.shellOutput(r"open  %s" % (self.image03))
                
            if self.refButtons.getSelect() == 4:
                pm.util.shellOutput(r"open  %s" % (self.image04))
        
