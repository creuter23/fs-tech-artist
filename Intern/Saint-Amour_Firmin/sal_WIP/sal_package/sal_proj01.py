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



global fileList

fileList = []

def gui(dir_path):
    if(pm.window(win, ex = True)):
        pm.deleteUI(win)
        
    if(pm.windowPref(win, ex = True)):
        pm.windowPref(win, remove = True)
    
    myWin = pm.window(win, title='sal_testing' , sizeable = True, mnb = True, width = 480, height = 900, backgroundColor= [.68,.68,.68])
    pm.scrollLayout()
    main01 = pm.columnLayout( adjustableColumn=True )
    main02 = pm.columnLayout( adjustableColumn=True )
    global antiAlising, compFocalLenght, prof
    pm.setParent(main02)
    # file info section
    
    
    
    pm.setParent(main02)
    
    infoColumn = pm.columnLayout(adjustableColumn=True)
    global fileInfo
    
    pm.setParent(main02)
     # grade total section
    infoFrame = pm.columnLayout(adjustableColumn=True)
    #infoLayout = pm.formLayout()
    # isntancing the total grade section
    global totalGrades
    totalGrades = sal.Total_Grades()
    totalGrades.create()
    
    #pm.setParent(infoFrame)
    pm.button( label = 'Output Grade and Comment' , command = checkWeighting)
    
    pm.setParent(main02)
    #pm.frameLayout( label = 'Grade', cll = True, cl = True , borderStyle = 'etchedIn', w = 480 )
    #mainLayout = pm.formLayout()
   
    # grading / commenting section
    # first intance of Section for antiAliasing / Noise Quality
    grading = pm.frameLayout( label= 'Grading', cll = True, cl = True , borderStyle = 'etchedIn', w = 480)
    pm.setParent(grading)
    antiAlising = sal.Grading_Section( name = 'Anitalias/Noise Qual', fileName =  r"%s/Comments/proj01_antiAlisaing.txt" % dir_path,
                                      field = totalGrades.queryAnti(), toUpdate = totalGrades)
    section01 = antiAlising.create()
    
    pm.setParent(grading)
    # second intance of Section for Composition / Focal Lenght
    compFocalLenght = sal.Grading_Section( name = 'Comp/Focal Length', fileName = r"%s/Comments/proj01_compFocal.txt" % dir_path,
                                          field = totalGrades.queryComp(), toUpdate = totalGrades)
    section02 = compFocalLenght.create()
    
    pm.setParent(grading)
    prof = sal.Grading_Prof( name = 'Professionalism', fileName = r"%s/Comments/proj01_prof.txt" % (dir_path),
                            field = totalGrades.queryPro(), fileStart = r"%s/Startup/proj01_start.db" % (dir_path), toUpdate = totalGrades)
    prof.create()
    # first intance of Section for proffesionalism
    #prof = sal.Checker( fileName= r"/Users/Fearman/Desktop/sal_package/Sartup/proj01_start")
    #section03 = prof.create()
    
    
    pm.setParent(infoColumn)
    fileInfo = sal.Images(prof)
    
    
    
    myWin.show()
    
 
def checkWeighting(*args):
    percent = totalGrades.queryAnti().getValue2() + totalGrades.queryComp().getValue2() + totalGrades.queryPro().getValue2()
    print percent
    
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
    if totalGrades.queryLate().getValue1() == 10:
        sceneFileOutput.write("1 DAY LATE (-10)\r\n")
        sceneFileOutput.write("-----------------------------------\r\n")
    if totalGrades.queryLate().getValue1() == 20:
        sceneFileOutput.write("2 DAYS LATE (-20)\r\n")
        sceneFileOutput.write("-----------------------------------\r\n")
    if totalGrades.queryLate().getValue1() == 30:
        sceneFileOutput.write("3 DAYS LATE (-30)\r\n")
        sceneFileOutput.write("-----------------------------------\r\n")
        
    sceneFileOutput.write("Grading for:\r\n")
    
    for names in fileInfo.queryNamesList():
        sceneFileOutput.write('%s\r\n' % names)
        
        
        
    #sceneFileOutput.write("Grading for: %s\r\n" % fileInfo.queryNamesString() )
    sceneFileOutput.write("-----------------------------------\r\n")
    sceneFileOutput.write("Antialiasing & Noise Quality Comments: \r\n" )
    sceneFileOutput.write('%s\r\n' % antiAlising.query())
    sceneFileOutput.write("Antialiasing & Noise Quality Grade Total:  \r\n")
    sceneFileOutput.write('%s\r\n' % totalGrades.queryAnti().getValue1() )
    sceneFileOutput.write("-----------------------------------\r\n")
    sceneFileOutput.write("Composition & Focal Length Comments: \r\n")
    sceneFileOutput.write('%s\r\n' % compFocalLenght.query())
    sceneFileOutput.write("Composition & Focal Length Grade Total:\r\n" )
    sceneFileOutput.write('%s\r\n'% totalGrades.queryComp().getValue1() )
    sceneFileOutput.write("-----------------------------------\r\n")
    sceneFileOutput.write("Professionalism Comments: \r\n")
    sceneFileOutput.write('%s\r\n' % prof.query())
    sceneFileOutput.write("Professionalism  Grade Total: \r\n" )
    sceneFileOutput.write('%s\r\n' % totalGrades.queryPro().getValue1() )
    sceneFileOutput.write("-----------------------------------\r\n")
    sceneFileOutput.write("Late Deductions: - %s \r\n" % totalGrades.queryLate().getValue1())
    sceneFileOutput.write("-----------------------------------\r\n")
    sceneFileOutput.write("Overall Grade Total: %s \r\n" % totalGrades.queryTotal().getValue1())
    sceneFileOutput.close()
    
    
    pm.util.shellOutput(r"open  %s.txt " % fileInfo.queryPath())
    


