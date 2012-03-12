"""
testing the seperate pieces that will make up the whole script

"""


import pymel.core as pm
#import EasyDialogs 
import salModule as sal
import os

win = 'testingWin'

def command01(* args):
    pm.select(cl=1)

global fileList

fileList = []

def gui():
    if(pm.window(win, ex = True)):
        pm.deleteUI(win)
        
    if(pm.windowPref(win, ex = True)):
        pm.windowPref(win, remove = True)
    
    pm.window(win, title='Testing' , sizeable = True, mnb = True, width = 480, backgroundColor = [.5, .5, .5])
    pm.scrollLayout()
    main01 = pm.columnLayout( adjustableColumn=True )
    main02 = pm.columnLayout( adjustableColumn=True )

    pm.setParent(main02)
    pm.frameLayout(label = 'Images', cll = True, cl = True , borderStyle = 'etchedIn', w = 480)
    global fileField01, fileField02, fileField03, fileField04
    fileField01 = pm.textFieldButtonGrp( text='image01', buttonLabel='image', bc=addImage01, ed=0, width= 480 )
    fileField02 = pm.textFieldButtonGrp( text='image02', buttonLabel='image', bc=addImage02, ed=0, width= 480 )
    fileField03 = pm.textFieldButtonGrp( text='image03', buttonLabel='image', bc=addImage03, ed=0, width= 480 )
    fileField04 = pm.textFieldButtonGrp( text='image04', buttonLabel='image', bc=addImage04, ed=0, width= 480 )
    pm.button( label = 'Open Images' , command = openImage)
    
    pm.setParent(main02)
    pm.frameLayout( label = 'Grade', cll = True, cl = True , h = 900 , borderStyle = 'etchedIn', w = 480 )
    mainLayout = pm.formLayout()

    
    
    test = sal.Section( name = 'Luke', layout = mainLayout , command = command01, total = command01)
    old = test.create()
    
    
    
    test01 = sal.Section( name = 'yeah', layout = mainLayout , command = command01, total = command01, control=old)
    old01 = test01.create()
    
    test02 = sal.Section( name = 'noWay', layout = mainLayout , command = command01, total = command01, control=old01)
    test02.create()
    
    pm.showWindow()


def addImage01(* args):
    global file01
    file01 = pm.fileDialog()
    newFile = os.path.basename(file01)
    fileField01.setText(newFile)
    fileList.append(file01)
    
    print fileList

def addImage02(* args):
    global file02
    file02 = pm.fileDialog()
    newFile = os.path.basename(file02)
    fileField02.setText(newFile)
    fileList.append(file02)
    
    print fileList

def addImage03(* args):
    global file03
    file03 = pm.fileDialog()
    newFile = os.path.basename(file03)
    fileField03.setText(newFile)
    fileList.append(file03)

    print fileList

    
def addImage04(* args):
    global file04
    file04 = pm.fileDialog()
    newFile = os.path.basename(file04)
    fileField04.setText(newFile)
    fileList.append(file04)
    
    print fileList

def openImage(* args):
    for files in fileList:
        pm.launchImageEditor(editImageFile=files)


