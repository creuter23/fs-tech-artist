"""
testing the seperate pieces that will make up the whole grading Script

"""

#import xlrd
#import xlwt
#import openpyxl
import maya.cmds as cmds
import pymel.core as pm
import salModule as sal
reload(sal)
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
    global fileInfo
    fileInfo = sal.Images()
    pm.setParent(main02)
     # grade total section
    infoFrame = pm.frameLayout( label = 'Grades Total', cll = True, cl = True , borderStyle = 'etchedIn', w = 480 )
    infoLayout = pm.formLayout()
    # isntancing the total grade section
    global totalGrades
    totalGrades = sal.UpperSection()
    totalGrades.create()
    
    pm.setParent(infoFrame)
    pm.button( label = 'Output Grade and Comment' , command = checkWeighting)
    
    pm.setParent(main02)
    pm.frameLayout( label = 'Grade', cll = True, cl = True , borderStyle = 'etchedIn', w = 480 )
    mainLayout = pm.formLayout()
   
    # grading / commenting section
    # first intance of Section for antiAliasing / Noise Quality
    global antiAlising, compFocalLenght, prof
    antiAlising = sal.Section( name = 'Anitalias/Noise Qual', layout = mainLayout , updateCommand = totalGrades,
                              fileRead =  "/Users/Fearman/Library/Preferences/Autodesk/maya/2011-x64/scripts/proj01_antiAlisaing.txt",updateField= totalGrades.queryAnti())
    section01 = antiAlising.create()
    
    # second intance of Section for Composition / Focal Lenght
    compFocalLenght = sal.Section( name = 'Comp/Focal Length', layout = mainLayout , updateCommand = totalGrades,
                                  fileRead =  "/Users/Fearman/Library/Preferences/Autodesk/maya/2011-x64/scripts/proj01_compFocal.txt", updateField = totalGrades.queryComp(), control=section01)
    section02 = compFocalLenght.create()
    
    # first intance of Section for proffesionalism
    prof = sal.Section( name = 'Professionalism', layout = mainLayout , updateCommand = totalGrades,
                       fileRead = "/Users/Fearman/Library/Preferences/Autodesk/maya/2011-x64/scripts/proj01_prof.txt", updateField = totalGrades.queryPro(), control=section02)
    section03 = prof.create()
    
    myWin.show()
    
 
def checkWeighting(*args):
    percent = totalGrades.queryAnti().getValue1() + totalGrades.queryComp().getValue1() + totalGrades.queryPro().getValue1()
    
    if percent != 100 :
        dialogCheck=pm.confirmDialog( title='Confirm Output', message='percentage not equal 100', button=['override','change'], defaultButton='change', cancelButton='change', dismissString='override' )
        if dialogCheck == 'change':
                print ("Output Cancelled")
        else:
            print ("override")
            output()
    else:
        output()
            
def output(* args):
    sceneFileOutput = open('%s.txt' % fileInfo.queryPath(), 'w')
    sceneFileOutput.write("Grading for: %s\r\n" % fileInfo.queryNames() )
    sceneFileOutput.write("-----------------------------------\r\n")
    sceneFileOutput.write("Antialiasing & Noise Quality Comments: %s \r\n" % antiAlising.query())
    sceneFileOutput.write("Antialiasing & Noise Quality Grade Total: %s \r\n" % totalGrades.queryAnti().getValue1())
    sceneFileOutput.write("-----------------------------------\r\n")
    sceneFileOutput.write("Composition & Focal Length Comments: %s \r\n" % compFocalLenght.query())
    sceneFileOutput.write("Composition & Focal Length Grade Total: %s \r\n" % totalGrades.queryComp().getValue1())
    sceneFileOutput.write("-----------------------------------\r\n")
    sceneFileOutput.write("Professionalism Comments: %s \r\n" % prof.query())
    sceneFileOutput.write("Professionalism  Grade Total: %s \r\n" % totalGrades.queryPro().getValue1())
    sceneFileOutput.write("-----------------------------------\r\n")
    sceneFileOutput.write("Late Deductions: - %s \r\n" % totalGrades.queryLate().getValue1())
    sceneFileOutput.write("-----------------------------------\r\n")
    sceneFileOutput.write("Overall Grade Total: %s \r\n" % totalGrades.queryTotal().getValue1())
    


