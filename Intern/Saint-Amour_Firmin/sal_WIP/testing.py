"""
testing the seperate pieces that will make up the whole script

"""

import maya.cmds as cmds
import pymel.core as pm
#import EasyDialogs 
import salModule as sal
import os

win = 'testingWin'

def command01(* args):
    pass

global fileList

fileList = []

def gui():
    if(pm.window(win, ex = True)):
        pm.deleteUI(win)
        
    if(pm.windowPref(win, ex = True)):
        pm.windowPref(win, remove = True)
    
    myWin = pm.window(win, title='Testing' , sizeable = True, mnb = True, width = 480, height = 900,  backgroundColor = [.5, .5, .5])
    pm.scrollLayout()
    main01 = pm.columnLayout( adjustableColumn=True )
    main02 = pm.columnLayout( adjustableColumn=True )

    pm.setParent(main02)
    # file info section
    pm.frameLayout(label = 'File Info', cll = True, cl = False, borderStyle = 'etchedIn', w = 480)
    global fileField01, fileField02, fileField03, fileField04
    fileField01 = pm.textFieldButtonGrp( text='image01', buttonLabel='Load Image', bc=addImage01, ed=0 )
    fileField02 = pm.textFieldButtonGrp( text='image02', buttonLabel='Load Image', bc=addImage02, ed=0 )
    fileField03 = pm.textFieldButtonGrp( text='image03', buttonLabel='Load Image', bc=addImage03, ed=0 )
    fileField04 = pm.textFieldButtonGrp( text='image04', buttonLabel='Load Image', bc=addImage04, ed=0 )
    pm.button( label = 'Open Images' , command = openImage)
    
    pm.setParent(main02)
    
    infoFrame = pm.frameLayout( label = 'Grades Total', cll = True, cl = True , borderStyle = 'etchedIn', w = 480 )
    infoLayout = pm.formLayout()
    global infoCheckBox, antiField, compField, proField, lateField, totalField, warningText
    infoCheckBox = pm.checkBox(label = 'Modify Weighting', onCommand = editFields, offCommand = editFields )
    
    antiField = pm.intFieldGrp( numberOfFields=2, label='Antialias/Noise Quality', extraLabel = 'Weight %' , value2 = 45 , enable1 = True ,
                                        enable2 = False,  changeCommand=updateTotal)
    compField = pm.intFieldGrp( numberOfFields=2, label='Composition/Focal Length', extraLabel = 'Weight %' , value2 = 45 , enable1 = False ,
                                        enable2 = False ,changeCommand=updateTotal)
    proField = pm.intFieldGrp( numberOfFields=2, label='Professionalism', extraLabel = 'Weight %' ,value2 = 10 ,enable1 = False ,
                                       enable2 = False, changeCommand=updateTotal)
    lateField = pm.intFieldGrp( numberOfFields=1, label='Late Deduction' , changeCommand=updateTotal)
    totalField = pm.floatFieldGrp( numberOfFields=1, label='Total Grade',enable1 = False, changeCommand=updateTotal)
    
    pm.formLayout( infoLayout, edit=1, attachForm=[[infoCheckBox, "left", 140], [infoCheckBox, "top", 5]])
    pm.formLayout( infoLayout, edit=1, attachOppositeControl=[[antiField ,"top", 40, infoCheckBox], [antiField, "right", 10, infoCheckBox]])
    pm.formLayout( infoLayout, edit=1, attachOppositeControl=[[compField ,"top", 40, antiField], [compField, "right", 10, antiField]])
    pm.formLayout( infoLayout, edit=1, attachOppositeControl=[[proField ,"top", 40, compField], [proField, "right", 10, compField]])
    pm.formLayout( infoLayout, edit=1, attachOppositeControl=[[lateField ,"top", 40, proField], [lateField, "left", 0, proField]])
    pm.formLayout( infoLayout, edit=1, attachOppositeControl=[[totalField ,"top", 40, lateField], [totalField, "left", 0, lateField]])
    
    pm.setParent(infoFrame)
    pm.text(label = '')
    warningText = pm.text(label='')
    pm.text(label = '')
    pm.button( label = 'Output Grade and Comment' )
    
    pm.setParent(main02)
    pm.frameLayout( label = 'Grade', cll = True, cl = True , borderStyle = 'etchedIn', w = 480 )
    mainLayout = pm.formLayout()

    
    # first intance of Section for antiAliasing / Noise Quality
    antiAlising = sal.Section( name = 'Anitalias/Noise Qual', layout = mainLayout ,
                              fileRead =  "/Users/Fearman/Library/Preferences/Autodesk/maya/2011-x64/scripts/proj01_antiAlisaing.txt",updateField = antiField).create()
    
    # second intance of Section for Composition / Focal Lenght
    compFocalLenght = sal.Section( name = 'Comp/Focal Length', layout = mainLayout ,
                                  fileRead =  "/Users/Fearman/Library/Preferences/Autodesk/maya/2011-x64/scripts/proj01_antiAlisaing.txt", updateField = compField, control=antiAlising).create()
    
    # first intance of Section for proffesionalism
    prof = sal.Section( name = 'Professionalism', layout = mainLayout ,
                       fileRead = "/Users/Fearman/Library/Preferences/Autodesk/maya/2011-x64/scripts/proj01_antiAlisaing.txt", updateField = proField, control=compFocalLenght).create()
    
    pm.showWindow()


def addImage01(* args):
    global file01
    
    file01 = pm.fileDialog()
    newFile = os.path.basename(file01)
    fileField01.setText(newFile)
    fileList.append(file01)
    
    

def addImage02(* args):
    global file02
    
    file02 = pm.fileDialog()
    newFile = os.path.basename(file02)
    fileField02.setText(newFile)
    fileList.append(file02)
    
    
    

def addImage03(* args):
    global file03
    file03 = pm.fileDialog()
    newFile = os.path.basename(file03)
    fileField03.setText(newFile)
    fileList.append(file03)

    

    
def addImage04(* args):
    global file04
    file04 = pm.fileDialog()
    newFile = os.path.basename(file04)
    fileField04.setText(newFile)
    fileList.append(file04)
    
    

def openImage(* args):
    for files in fileList:
        pm.launchImageEditor(editImageFile=files)
        
        # import pymel.internal as pmi
        # util.shellOutput
        
def editFields(* args):
        if infoCheckBox.getValue() != 0:
            antiField.setEnable2(True)
            compField.setEnable2(True)
            proField.setEnable2(True)
        
        else :
            antiField.setEnable2(False)
            compField.setEnable2(False)
            proField.setEnable2(False)
            
def updateTotal(* args):
        antitotal = (antiField.getValue1() / float(100)) * antiField.getValue2()
      
        comptotal = (compField.getValue1() / float(100)) * compField.getValue2()
        prototal = (proField.getValue1() / float(100)) * proField.getValue2()
        gradetotal = ( antitotal + comptotal+ prototal ) - lateField.getValue1()
        
       
        
      
        
        
        
        
        
        totalField.setValue1(gradetotal)
        
        if antiField.getValue2() + compField.getValue2() + proField.getValue2() != 100:
            warningText.setLabel('Error : Total Weighting Must Equal 100')
            warningText.setBackgroundColor([1,0,0])
        else:
            warningText.setLabel('')
            warningText.setBackgroundColor([.5,.5,.5])


