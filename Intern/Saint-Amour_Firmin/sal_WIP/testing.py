"""
testing the seperate pieces that will make up the whole script

"""


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
    
    myWin = pm.window(win, title='Testing' , sizeable = True, mnb = True, width = 480, backgroundColor = [.5, .5, .5])
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
    pm.frameLayout( label = 'Grades Total', cll = True, cl = True , borderStyle = 'etchedIn', w = 480 )
    gradesTotal = sal.UpperSection()
    gradesTotal.create()
    print 'show up'
    
    pm.setParent(main02)
    pm.frameLayout( label = 'Grade', cll = True, cl = True , borderStyle = 'etchedIn', w = 480 )
    mainLayout = pm.formLayout()

    
    # first intance of Section for antiAliasing
    antiAlising = sal.Section( name = 'Anitalias/Noise Qual', layout = mainLayout ,  total = command01)
    old = antiAlising.create()
    
    # second intance of Section for Composition
    compFocalLenght = sal.Section( name = 'Comp/Focal Length', layout = mainLayout ,  total = command01, control=old)
    old01 = compFocalLenght.create()
    
    # first intance of Section for proffesionalsim
    prof = sal.Section( name = 'Professionalism', layout = mainLayout ,  total = command01, control=old01)
    prof.create()
    
    pm.showWindow()


def addImage01(* args):
    global file01
    print 'this is working'
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


