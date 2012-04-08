'''
Author: Firmin Saint-Amour

Description:
    # classes for each project
    in this module the classes from salModule will be combine
    into new classes
    there will be one class per project

'''

import pymel.core as pm # maya pymel
import salModule as sal # custom module
reload(sal)
import os # python module
from PIL import Image # this reads metadata from images

class Project02():
    def __init__(self, path):
        self.path = path
        print 'project02'
            
    def create(self):
        self.mainLayout = pm.columnLayout(adjustableColumn=True)
        self.infoLayout = pm.columnLayout(adjustableColumn=True)
        pm.setParent(self.mainLayout)
        self.layout = pm.columnLayout(adjustableColumn=True)
        pm.setParent(self.layout)
        # the total Grades Section
        self.total = sal.Total_Grades02()
        self.total.create()
        
        pm.button(label = 'Output Grade and Comment', command = pm.Callback(self.check))
        
        pm.setParent(self.layout)
        grading = pm.frameLayout( label= 'Grading', cll = True, cl = True , borderStyle = 'etchedIn', w = 480)
        # grading for lighting
        self.lighting = sal.Grading_Section(name = 'Lighting',
                fileName = r"%s/Comments/proj02_lighting.txt" % (self.path),
                field = self.total.queryLight(), toUpdate = self.total)
        self.lighting.create()
        
        pm.setParent(grading)
        # grading for Composition/Focal Lenght
        self.compFocal = sal.Grading_Section02(name = 'Comp/Focal Length',
                fileName = r"%s/Comments/proj02_compFocal.txt" % (self.path),
                field = self.total.queryComp(), toUpdate = self.total)
        self.compFocal.create()
        
        pm.setParent(grading)
        # grading for antialiasing
        self.antiAliasing = sal.Grading_Section02(name = 'Antialias/Noise Qual',
                fileName = r"%s/Comments/proj02_antiAliasing.txt" % (self.path),
                field = self.total.queryAnti(), toUpdate = self.total)
        self.antiAliasing.create()
        
        pm.setParent(grading)
        # grading for Professionalism
        self.pro = sal.Grading_Prof02(name = 'Professionalism',
                fileName = r"%s/Comments/proj02_prof.txt" % (self.path),
                field = self.total.queryPro(),
                fileStart = r"%s/Startup/proj02_start.db" % (self.path),
                toUpdate = self.total)
        self.pro.create()
        
        # the Images info section
        # *takes the professionalism section as an arguement
        pm.setParent(self.infoLayout)
        self.info = sal.Images02(self.pro, image = r"%s/Reference_Images/proj02_ref.tga" % (self.path))
        
        return self.layout
    
    def check(self):
        # this check the weighting before outputting
        percent = self.total.queryLight().getValue2() 
        print percent
    
        if percent != 100 :
            dialogCheck=pm.confirmDialog( title='Confirm Output', message='percentage not equal 100', button=['override','change'], defaultButton='change', cancelButton='change', dismissString='override' )
            if dialogCheck == 'change':
                    print ("Output Cancelled")
            else:
                print ("override")
                output()
        else:
            self.output()
            
    def output(self):
        # this outputs to a text file
        oldPath = self.info.queryPath()
        image = Image.open(oldPath)
        ending = image.format
        newPath = oldPath.split('.%s' % (ending.lower()))
        
        sceneFileOutput = open('%s.txt' % (newPath[0]), 'w')
        if self.total.queryLate().getValue1() == 10:
            sceneFileOutput.write("1 DAY LATE (-10)\r\n")
            sceneFileOutput.write("-----------------------------------\r\n")
        if self.total.queryLate().getValue1() == 20:
            sceneFileOutput.write("2 DAYS LATE (-20)\r\n")
            sceneFileOutput.write("-----------------------------------\r\n")
        if self.total.queryLate().getValue1() == 30:
            sceneFileOutput.write("3 DAYS LATE (-30)\r\n")
            sceneFileOutput.write("-----------------------------------\r\n")
            
        sceneFileOutput.write("Grading for:\r\n")
        
        for names in self.info.queryNamesList():
            sceneFileOutput.write('%s\r\n' % names)
            
        #sceneFileOutput.write("Grading for: %s\r\n" % fileInfo.queryNamesString() )
        sceneFileOutput.write("-----------------------------------\r\n")
        sceneFileOutput.write("Lighting Comments: \r\n" )
        sceneFileOutput.write('%s\r\n' % self.lighting.query())
        sceneFileOutput.write("Lighting Grade Total:  \r\n")
        sceneFileOutput.write('%s\r\n' % self.total.queryLight().getValue1() )
        
        sceneFileOutput.write("-----------------------------------\r\n")
        
        sceneFileOutput.write("Antialiasing & Noise Quality Comments: \r\n" )
        sceneFileOutput.write('%s\r\n' % self.antiAliasing.query())
        sceneFileOutput.write("Antialiasing & Noise Quality Deduction:  \r\n")
        sceneFileOutput.write('%s\r\n' % self.total.queryAnti().getValue1() )
        
        sceneFileOutput.write("-----------------------------------\r\n")
        
        sceneFileOutput.write("Composition & Focal Length Comments: \r\n")
        sceneFileOutput.write('%s\r\n' % self.compFocal.query())
        sceneFileOutput.write("Composition & Focal Length Deduction:\r\n" )
        sceneFileOutput.write('%s\r\n'% self.total.queryComp().getValue1() )
        
        sceneFileOutput.write("-----------------------------------\r\n")
        
        sceneFileOutput.write("Professionalism Comments: \r\n")
        sceneFileOutput.write('%s\r\n' % self.pro.query())
        sceneFileOutput.write("Professionalism Deduction: \r\n" )
        sceneFileOutput.write('%s\r\n' % self.total.queryPro().getValue1() )
        
        sceneFileOutput.write("-----------------------------------\r\n")
        sceneFileOutput.write("Late Deductions: - %s \r\n" % self.total.queryLate().getValue1())
        sceneFileOutput.write("-----------------------------------\r\n")
        sceneFileOutput.write("Overall Grade Total: %s \r\n" % self.total.queryTotal().getValue1())
        sceneFileOutput.close()
        
        pm.util.shellOutput(r"open  %s.txt " % (newPath[0]))
        
class Project03(Project02):
    def __init__(self, path):
        self.path = path
        print 'project02'
    
    def create(self):
        self.mainLayout = pm.columnLayout(adjustableColumn=True)
        self.infoLayout = pm.columnLayout(adjustableColumn=True)
        pm.setParent(self.mainLayout)
        self.layout = pm.columnLayout(adjustableColumn=True)
        pm.setParent(self.layout)
        self.total = sal.Total_Grades02()
        self.total.create()
        
        pm.button(label = 'Output Grade and Comment', command = pm.Callback(self.check))
        
        pm.setParent(self.layout)
        grading = pm.frameLayout( label= 'Grading', cll = True, cl = True , borderStyle = 'etchedIn', w = 480)
        
        self.lighting = sal.Grading_Section(name = 'Lighting',
                fileName = r"%s/Comments/proj03_lighting.txt" % (self.path),
                field = self.total.queryLight(), toUpdate = self.total)
        self.lighting.create()
        
        pm.setParent(grading)
        
        self.compFocal = sal.Grading_Section02(name = 'Comp/Focal Length',
                fileName = r"%s/Comments/proj03_compFocal.txt" % (self.path),
                field = self.total.queryComp(), toUpdate = self.total)
        self.compFocal.create()
        
        pm.setParent(grading)
        
        self.antiAliasing = sal.Grading_Section02(name = 'Antialias/Noise Qual',
                fileName = r"%s/Comments/proj03_antiAliasing.txt" % (self.path),
                field = self.total.queryAnti(), toUpdate = self.total)
        self.antiAliasing.create()
        
        pm.setParent(grading)
        
        self.pro = sal.Grading_Prof02(name = 'Professionalism',
                fileName = r"%s/Comments/proj03_prof.txt" % (self.path),
                field = self.total.queryPro(),
                fileStart = r"%s/Startup/proj03_start.db" % (self.path),
                toUpdate = self.total)
        self.pro.create()
        
        pm.setParent(self.infoLayout)
        self.info = sal.Images02(self.pro, image = r"%s/Reference_Images/proj03_ref.tga" % (self.path))
        
        return self.layout
    
class Project04():
    def __init__(self, path):
        self.path = path
        #print 'project04'
    
    def create(self):
        self.mainLayout = pm.columnLayout(adjustableColumn=True)
        self.infoLayout = pm.columnLayout(adjustableColumn=True)
        pm.setParent(self.mainLayout)
        self.layout = pm.columnLayout(adjustableColumn=True)
        pm.setParent(self.layout)
        self.total = sal.Total_Grades03()
        self.total.create()
        
        pm.button(label = 'Output Grade and Comment', command = pm.Callback(self.check))
        
        pm.setParent(self.layout)
        grading = pm.frameLayout( label= 'Grading', cll = True, cl = True , borderStyle = 'etchedIn', w = 480)
        
        self.lighting = sal.Grading_Section(name = 'Lighting',
                fileName = r"%s/Comments/proj04_lighting.txt" % (self.path),
                field = self.total.queryLight(), toUpdate = self.total)
        self.lighting.create()
        
        
        pm.setParent(grading)
        
        self.mat = sal.Grading_Section(name = 'Materials/Textures',
                fileName = r"%s/Comments/proj04_mat.txt" % (self.path),
                field = self.total.queryMat(), toUpdate = self.total)
        self.mat.create()
        
        
        pm.setParent(grading)
        
        self.compFocal = sal.Grading_Section02(name = 'Comp/Focal Length',
                fileName = r"%s/Comments/proj04_compFocal.txt" % (self.path),
                field = self.total.queryComp(), toUpdate = self.total)
        self.compFocal.create()
        
        pm.setParent(grading)
        
        self.antiAliasing = sal.Grading_Section02(name = 'Antialias/Noise Qual',
                fileName = r"%s/Comments/proj04_antiAliasing.txt" % (self.path),
                field = self.total.queryAnti(), toUpdate = self.total)
        self.antiAliasing.create()
        
        pm.setParent(grading)
        
        self.pro = sal.Grading_Prof02(name = 'Professionalism',
                fileName = r"%s/Comments/proj04_prof.txt" % (self.path),
                field = self.total.queryPro(),
                fileStart = r"%s/Startup/proj04_start.db" % (self.path),
                toUpdate = self.total)
        self.pro.create()
        
        pm.setParent(self.infoLayout)
        self.info = sal.Images02(self.pro, image = r"%s/Reference_Images/proj04_ref.tga" % (self.path))
        
        return self.layout
    
    def check(self):
        percent = self.total.queryLight().getValue2() + self.total.queryMat().getValue2()
        print percent
    
        if percent != 100 :
            dialogCheck=pm.confirmDialog( title='Confirm Output', message='percentage not equal 100', button=['override','change'], defaultButton='change', cancelButton='change', dismissString='override' )
            if dialogCheck == 'change':
                    print ("Output Cancelled")
            else:
                print ("override")
                output()
        else:
            self.output()
            
    def output(self):
        oldPath = self.info.queryPath()
        image = Image.open(oldPath)
        ending = image.format
        newPath = oldPath.split('.%s' % (ending.lower()))
        #print newPath[0], 'path'
        
        
        sceneFileOutput = open('%s.txt' % (newPath[0]), 'w')
        if self.total.queryLate().getValue1() == 10:
            sceneFileOutput.write("1 DAY LATE (-10)\r\n")
            sceneFileOutput.write("-----------------------------------\r\n")
        if self.total.queryLate().getValue1() == 20:
            sceneFileOutput.write("2 DAYS LATE (-20)\r\n")
            sceneFileOutput.write("-----------------------------------\r\n")
        if self.total.queryLate().getValue1() == 30:
            sceneFileOutput.write("3 DAYS LATE (-30)\r\n")
            sceneFileOutput.write("-----------------------------------\r\n")
            
        sceneFileOutput.write("Grading for:\r\n")
        
        for names in self.info.queryNamesList():
            sceneFileOutput.write('%s\r\n' % names)
            
            
            
        
        sceneFileOutput.write("-----------------------------------\r\n")
        sceneFileOutput.write("Lighting Comments: \r\n" )
        sceneFileOutput.write('%s\r\n' % self.lighting.query())
        sceneFileOutput.write("Lighting Grade Total:  \r\n")
        sceneFileOutput.write('%s\r\n' % self.total.queryLight().getValue1() )
        
        sceneFileOutput.write("-----------------------------------\r\n")
        
        sceneFileOutput.write("Material & Textures Comments: \r\n" )
        sceneFileOutput.write('%s\r\n' % self.mat.query())
        sceneFileOutput.write("Material & Textures Grade Total:  \r\n")
        sceneFileOutput.write('%s\r\n' % self.total.queryMat().getValue1() )
        
        sceneFileOutput.write("-----------------------------------\r\n")
        
        sceneFileOutput.write("Antialiasing & Noise Quality Comments: \r\n" )
        sceneFileOutput.write('%s\r\n' % self.antiAliasing.query())
        sceneFileOutput.write("Antialiasing & Noise Quality Deduction:  \r\n")
        sceneFileOutput.write('%s\r\n' % self.total.queryAnti().getValue1() )
        
        sceneFileOutput.write("-----------------------------------\r\n")
        
        sceneFileOutput.write("Composition & Focal Length Comments: \r\n")
        sceneFileOutput.write('%s\r\n' % self.compFocal.query())
        sceneFileOutput.write("Composition & Focal Length Deduction:\r\n" )
        sceneFileOutput.write('%s\r\n'% self.total.queryComp().getValue1() )
        
        sceneFileOutput.write("-----------------------------------\r\n")
        
        sceneFileOutput.write("Professionalism Comments: \r\n")
        sceneFileOutput.write('%s\r\n' % self.pro.query())
        sceneFileOutput.write("Professionalism Deduction: \r\n" )
        sceneFileOutput.write('%s\r\n' % self.total.queryPro().getValue1() )
        
        sceneFileOutput.write("-----------------------------------\r\n")
        sceneFileOutput.write("Late Deductions: - %s \r\n" % self.total.queryLate().getValue1())
        sceneFileOutput.write("-----------------------------------\r\n")
        sceneFileOutput.write("Overall Grade Total: %s \r\n" % self.total.queryTotal().getValue1())
        sceneFileOutput.close()
        
        pm.util.shellOutput(r"open  %s.txt " % (newPath[0]))
    
class Project05():
    def __init__(self, path):
        self.path = path
        print 'project05'
    
    def create(self):
        self.mainLayout = pm.columnLayout(adjustableColumn=True)
        self.infoLayout = pm.columnLayout(adjustableColumn=True)
        pm.setParent(self.mainLayout)
        self.layout = pm.columnLayout(adjustableColumn=True)
        pm.setParent(self.layout)
        self.total = sal.Total_Grades04()
        self.total.create()
        
        pm.button(label = 'Output Grade and Comment', command = pm.Callback(self.check))
        
        pm.setParent(self.layout)
        grading = pm.frameLayout( label= 'Grading', cll = True, cl = True , borderStyle = 'etchedIn', w = 480)
        
        self.lighting = sal.Grading_Section(name = 'Lighting',
                fileName = r"%s/Comments/proj05_lighting.txt" % (self.path),
                field = self.total.queryLight(), toUpdate = self.total)
        self.lighting.create()
        
        
        pm.setParent(grading)
        
        self.mat = sal.Grading_Section(name = 'Materials/Textures',
                fileName = r"%s/Comments/proj05_mat.txt" % (self.path),
                field = self.total.queryMat(), toUpdate = self.total)
        self.mat.create()
        
        pm.setParent(grading)
        
        self.ray = sal.Grading_Section(name = 'Raytracing',
                fileName = r"%s/Comments/proj05_ray.txt" % (self.path),
                field = self.total.queryRay(), toUpdate = self.total)
        self.ray.create()
        
        
        pm.setParent(grading)
        
        self.compFocal = sal.Grading_Section02(name = 'Comp/Focal Length',
                fileName = r"%s/Comments/proj05_compFocal.txt" % (self.path),
                field = self.total.queryComp(), toUpdate = self.total)
        self.compFocal.create()
        
        pm.setParent(grading)
        
        self.antiAliasing = sal.Grading_Section02(name = 'Antialias/Noise Qual',
                fileName = r"%s/Comments/proj05_antiAliasing.txt" % (self.path),
                field = self.total.queryAnti(), toUpdate = self.total)
        self.antiAliasing.create()
        
        pm.setParent(grading)
        
        self.pro = sal.Grading_Prof02(name = 'Professionalism',
                fileName = r"%s/Comments/proj05_prof.txt" % (self.path),
                field = self.total.queryPro(),
                fileStart = r"%s/Startup/proj05_start.db" % (self.path),
                toUpdate = self.total)
        self.pro.create()
        
        pm.setParent(self.infoLayout)
        self.info = sal.Images02(self.pro, image = r"%s/Reference_Images/proj05_ref.tga" % (self.path) )
        
        return self.layout
    
    def check(self):
        percent = self.total.queryLight().getValue2() + self.total.queryMat().getValue2() + self.total.queryRay().getValue2()
        print percent
    
        if percent != 100 :
            dialogCheck=pm.confirmDialog( title='Confirm Output', message='percentage not equal 100', button=['override','change'], defaultButton='change', cancelButton='change', dismissString='override' )
            if dialogCheck == 'change':
                    print ("Output Cancelled")
            else:
                print ("override")
                output()
        else:
            self.output()
            
    def output(self):
        oldPath = self.info.queryPath()
        image = Image.open(oldPath)
        ending = image.format
        newPath = oldPath.split('.%s' % (ending.lower()))
        #print newPath[0], 'path'
        
        sceneFileOutput = open('%s.txt' % (newPath[0]), 'w')
        if self.total.queryLate().getValue1() == 10:
            sceneFileOutput.write("1 DAY LATE (-10)\r\n")
            sceneFileOutput.write("-----------------------------------\r\n")
        if self.total.queryLate().getValue1() == 20:
            sceneFileOutput.write("2 DAYS LATE (-20)\r\n")
            sceneFileOutput.write("-----------------------------------\r\n")
        if self.total.queryLate().getValue1() == 30:
            sceneFileOutput.write("3 DAYS LATE (-30)\r\n")
            sceneFileOutput.write("-----------------------------------\r\n")
            
        sceneFileOutput.write("Grading for:\r\n")
        
        for names in self.info.queryNamesList():
            sceneFileOutput.write('%s\r\n' % names)
            
        sceneFileOutput.write("-----------------------------------\r\n")
        sceneFileOutput.write("Lighting Comments: \r\n" )
        sceneFileOutput.write('%s\r\n' % self.lighting.query())
        sceneFileOutput.write("Lighting Grade Total:  \r\n")
        sceneFileOutput.write('%s\r\n' % self.total.queryLight().getValue1() )
        
        sceneFileOutput.write("-----------------------------------\r\n")
        
        sceneFileOutput.write("Material & Textures Comments: \r\n" )
        sceneFileOutput.write('%s\r\n' % self.mat.query())
        sceneFileOutput.write("Material & Textures Grade Total:  \r\n")
        sceneFileOutput.write('%s\r\n' % self.total.queryMat().getValue1() )
        
        sceneFileOutput.write("-----------------------------------\r\n")
        
        sceneFileOutput.write("Raytracing Comments: \r\n" )
        sceneFileOutput.write('%s\r\n' % self.ray.query())
        sceneFileOutput.write("Raytracing Grade Total:  \r\n")
        sceneFileOutput.write('%s\r\n' % self.total.queryRay().getValue1() )
        
        sceneFileOutput.write("-----------------------------------\r\n")
        
        sceneFileOutput.write("Antialiasing & Noise Quality Comments: \r\n" )
        sceneFileOutput.write('%s\r\n' % self.antiAliasing.query())
        sceneFileOutput.write("Antialiasing & Noise Quality Deduction:  \r\n")
        sceneFileOutput.write('%s\r\n' % self.total.queryAnti().getValue1() )
        
        sceneFileOutput.write("-----------------------------------\r\n")
        
        sceneFileOutput.write("Composition & Focal Length Comments: \r\n")
        sceneFileOutput.write('%s\r\n' % self.compFocal.query())
        sceneFileOutput.write("Composition & Focal Length Deduction:\r\n" )
        sceneFileOutput.write('%s\r\n'% self.total.queryComp().getValue1() )
        
        sceneFileOutput.write("-----------------------------------\r\n")
        
        sceneFileOutput.write("Professionalism Comments: \r\n")
        sceneFileOutput.write('%s\r\n' % self.pro.query())
        sceneFileOutput.write("Professionalism Deduction: \r\n" )
        sceneFileOutput.write('%s\r\n' % self.total.queryPro().getValue1() )
        
        sceneFileOutput.write("-----------------------------------\r\n")
        sceneFileOutput.write("Late Deductions: - %s \r\n" % self.total.queryLate().getValue1())
        sceneFileOutput.write("-----------------------------------\r\n")
        sceneFileOutput.write("Overall Grade Total: %s \r\n" % self.total.queryTotal().getValue1())
        sceneFileOutput.close()
        
        pm.util.shellOutput(r"open  %s.txt " % (newPath[0]))
      
class Project06(Project05):
    def create(self):
        self.mainLayout = pm.columnLayout(adjustableColumn=True)
        self.infoLayout = pm.columnLayout(adjustableColumn=True)
        pm.setParent(self.mainLayout)
        self.layout = pm.columnLayout(adjustableColumn=True)
        pm.setParent(self.layout)
        self.total = sal.Total_Grades05()
        self.total.create()
        
        pm.button(label = 'Output Grade and Comment', command = pm.Callback(self.check))
        
        pm.setParent(self.layout)
        grading = pm.frameLayout( label= 'Grading', cll = True, cl = True , borderStyle = 'etchedIn', w = 480)
        
        self.lighting = sal.Grading_Section(name = 'Lighting',
                fileName = r"%s/Comments/proj06_lighting.txt" % (self.path),
                field = self.total.queryLight(), toUpdate = self.total)
        self.lighting.create()
        
        
        pm.setParent(grading)
        
        self.mat = sal.Grading_Section(name = 'Materials/Textures',
                fileName = r"%s/Comments/proj06_mat.txt" % (self.path),
                field = self.total.queryMat(), toUpdate = self.total)
        self.mat.create()
        
        pm.setParent(grading)
        
        self.ray = sal.Grading_Section(name = 'Raytracing',
                fileName = r"%s/Comments/proj06_ray.txt" % (self.path),
                field = self.total.queryRay(), toUpdate = self.total)
        self.ray.create()
        
        
        pm.setParent(grading)
        
        self.compFocal = sal.Grading_Section02(name = 'Comp/Focal Length',
                fileName = r"%s/Comments/proj06_compFocal.txt" % (self.path),
                field = self.total.queryComp(), toUpdate = self.total)
        self.compFocal.create()
        
        pm.setParent(grading)
        
        self.antiAliasing = sal.Grading_Section02(name = 'Antialias/Noise Qual',
                fileName = r"%s/Comments/proj06_antiAliasing.txt" % (self.path),
                field = self.total.queryAnti(), toUpdate = self.total)
        self.antiAliasing.create()
        
        pm.setParent(grading)
        
        self.pro = sal.Grading_Prof02(name = 'Professionalism',
                fileName = r"%s/Comments/proj06_prof.txt" % (self.path),
                field = self.total.queryPro(),
                fileStart = r"%s/Startup/proj06_start.db" % (self.path),
                toUpdate = self.total)
        self.pro.create()
        
        pm.setParent(self.infoLayout)
        self.info = sal.Images(self.pro)
        
        return self.layout
    
class Project07(Project04):
    
    def create(self):
        self.mainLayout = pm.columnLayout(adjustableColumn=True)
        self.infoLayout = pm.columnLayout(adjustableColumn=True)
        pm.setParent(self.mainLayout)
        self.layout = pm.columnLayout(adjustableColumn=True)
        pm.setParent(self.layout)
        self.total = sal.Total_Grades03()
        self.total.create()
        
        pm.button(label = 'Output Grade and Comment', command = pm.Callback(self.check))
        
        pm.setParent(self.layout)
        grading = pm.frameLayout( label= 'Grading', cll = True, cl = True , borderStyle = 'etchedIn', w = 480)
        
        self.lighting = sal.Grading_Section(name = 'Lighting',
                fileName = r"%s/Comments/proj07_lighting.txt" % (self.path),
                field = self.total.queryLight(), toUpdate = self.total)
        self.lighting.create()
        
        
        pm.setParent(grading)
        
        self.mat = sal.Grading_Section(name = 'Materials/Textures',
                fileName = r"%s/Comments/proj07_mat.txt" % (self.path),
                field = self.total.queryMat(), toUpdate = self.total)
        self.mat.create()
        
        
        pm.setParent(grading)
        
        self.compFocal = sal.Grading_Section02(name = 'Comp/Focal Length',
                fileName = r"%s/Comments/proj07_compFocal.txt" % (self.path),
                field = self.total.queryComp(), toUpdate = self.total)
        self.compFocal.create()
        
        pm.setParent(grading)
        
        self.antiAliasing = sal.Grading_Section02(name = 'Antialias/Noise Qual',
                fileName = r"%s/Comments/proj07_antiAliasing.txt" % (self.path),
                field = self.total.queryAnti(), toUpdate = self.total)
        self.antiAliasing.create()
        
        pm.setParent(grading)
        
        self.pro = sal.Grading_Prof02(name = 'Professionalism',
                fileName = r"%s/Comments/proj07_prof.txt" % (self.path),
                field = self.total.queryPro(),
                fileStart = r"%s/Startup/proj07_start.db" % (self.path),
                toUpdate = self.total)
        self.pro.create()
        
        pm.setParent(self.infoLayout)
        self.info = sal.Images(self.pro)
        
        return self.layout
    
class Final_Project(Project04):
    def create(self):
        self.mainLayout = pm.columnLayout(adjustableColumn=True)
        self.infoLayout = pm.columnLayout(adjustableColumn=True)
        pm.setParent(self.mainLayout)
        self.layout = pm.columnLayout(adjustableColumn=True)
        pm.setParent(self.layout)
        self.total = sal.Total_Grades03()
        self.total.create()
        
        pm.button(label = 'Output Grade and Comment', command = pm.Callback(self.check))
        
        pm.setParent(self.layout)
        grading = pm.frameLayout( label= 'Grading', cll = True, cl = True , borderStyle = 'etchedIn', w = 480)
        
        self.lighting = sal.Grading_Section(name = 'Lighting',
                fileName = r"%s/Comments/proj08_lighting.txt" % (self.path),
                field = self.total.queryLight(), toUpdate = self.total)
        self.lighting.create()
        
        
        pm.setParent(grading)
        
        self.mat = sal.Grading_Section(name = 'Materials/Textures',
                fileName = r"%s/Comments/proj08_mat.txt" % (self.path),
                field = self.total.queryMat(), toUpdate = self.total)
        self.mat.create()
        
        
        pm.setParent(grading)
        
        self.compFocal = sal.Grading_Section02(name = 'Comp/Focal Length',
                fileName = r"%s/Comments/proj08_compFocal.txt" % (self.path),
                field = self.total.queryComp(), toUpdate = self.total)
        self.compFocal.create()
        
        pm.setParent(grading)
        
        self.antiAliasing = sal.Grading_Section02(name = 'Antialias/Noise Qual',
                fileName = r"%s/Comments/proj08_antiAliasing.txt" % (self.path),
                field = self.total.queryAnti(), toUpdate = self.total)
        self.antiAliasing.create()
        
        pm.setParent(grading)
        
        self.pro = sal.Grading_Prof02(name = 'Professionalism',
                fileName = r"%s/Comments/proj08_prof.txt" % (self.path),
                field = self.total.queryPro(),
                fileStart = r"%s/Startup/proj08_start.db" % (self.path),
                toUpdate = self.total)
        self.pro.create()
        
        pm.setParent(self.infoLayout)
        self.info = sal.Images03(self.pro,
                image01 = r"%s/Reference_Images/final01_ref.tga" % (self.path),
                image02 = r"%s/Reference_Images/final02_ref.tga" % (self.path),
                image03 = r"%s/Reference_Images/final03_ref.tga" % (self.path),
                image04 = r"%s/Reference_Images/final04_ref.tga" % (self.path))
        
        return self.layout
    
            
class Project01():
    def __init__(self, path):
        self.path = path
        print 'project01'
            
    def create(self):
        self.mainLayout = pm.columnLayout(adjustableColumn=True)
        self.infoLayout = pm.columnLayout(adjustableColumn=True)
        pm.setParent(self.mainLayout)
        self.layout = pm.columnLayout(adjustableColumn=True)
        pm.setParent(self.layout)
        self.total = sal.Total_Grades()
        self.total.create()
        
        pm.button(label = 'Output Grade and Comment', command = pm.Callback(self.check))
        
        pm.setParent(self.layout)
        grading = pm.frameLayout( label= 'Grading', cll = True, cl = True , borderStyle = 'etchedIn', w = 480)
        
        self.compFocal = sal.Grading_Section(name = 'Comp/Focal Length',
                fileName = r"%s/Comments/proj01_compFocal.txt" % (self.path),
                field = self.total.queryComp(), toUpdate = self.total)
        self.compFocal.create()
        
        pm.setParent(grading)
        
        self.antiAliasing = sal.Grading_Section(name = 'Antialias/Noise Qual',
                fileName = r"%s/Comments/proj01_antiAliasing.txt" % (self.path),
                field = self.total.queryAnti(), toUpdate = self.total)
        self.antiAliasing.create()
        
        pm.setParent(grading)
        
        self.pro = sal.Grading_Prof(name = 'Professionalism',
                fileName = r"%s/Comments/proj01_prof.txt" % (self.path),
                field = self.total.queryPro(),
                fileStart = r"%s/Startup/proj01_start.db" % (self.path),
                toUpdate = self.total)
        self.pro.create()
        
        pm.setParent(self.infoLayout)
        
        self.info = sal.Images(self.pro)
        
        return self.layout
    
    def check(self):
        percent = self.total.queryAnti().getValue2() + self.total.queryComp().getValue2() + self.total.queryPro().getValue2() 
        print percent
    
        if percent != 100 :
            dialogCheck=pm.confirmDialog( title='Confirm Output', message='percentage not equal 100', button=['override','change'], defaultButton='change', cancelButton='change', dismissString='override' )
            if dialogCheck == 'change':
                    print ("Output Cancelled")
            else:
                print ("override")
                output()
        else:
            self.output()
            
    def output(self):
        oldPath = self.info.queryPath()
        image = Image.open(oldPath)
        ending = image.format
        newPath = oldPath.split('.%s' % (ending.lower()))
        #print newPath[0], 'path'
        
        sceneFileOutput = open('%s.txt' % (newPath[0]), 'w')
        if self.total.queryLate().getValue1() == 10:
            sceneFileOutput.write("1 DAY LATE (-10)\r\n")
            sceneFileOutput.write("-----------------------------------\r\n")
        if self.total.queryLate().getValue1() == 20:
            sceneFileOutput.write("2 DAYS LATE (-20)\r\n")
            sceneFileOutput.write("-----------------------------------\r\n")
        if self.total.queryLate().getValue1() == 30:
            sceneFileOutput.write("3 DAYS LATE (-30)\r\n")
            sceneFileOutput.write("-----------------------------------\r\n")
            
        sceneFileOutput.write("Grading for:\r\n")
        
        for names in self.info.queryNamesList():
            sceneFileOutput.write('%s\r\n' % names)
            
            
            
        #sceneFileOutput.write("Grading for: %s\r\n" % fileInfo.queryNamesString() )
        sceneFileOutput.write("-----------------------------------\r\n")
        sceneFileOutput.write("Antialiasing & Noise Quality Comments: \r\n" )
        sceneFileOutput.write('%s\r\n' % self.antiAliasing.query())
        sceneFileOutput.write("Antialiasing & Noise Quality Grade Total:  \r\n")
        sceneFileOutput.write('%s\r\n' % self.total.queryAnti().getValue1() )
        sceneFileOutput.write("-----------------------------------\r\n")
        sceneFileOutput.write("Composition & Focal Length Comments: \r\n")
        sceneFileOutput.write('%s\r\n' % self.compFocal.query())
        sceneFileOutput.write("Composition & Focal Length Grade Total:\r\n" )
        sceneFileOutput.write('%s\r\n'% self.total.queryComp().getValue1() )
        sceneFileOutput.write("-----------------------------------\r\n")
        sceneFileOutput.write("Professionalism Comments: \r\n")
        sceneFileOutput.write('%s\r\n' % self.pro.query())
        sceneFileOutput.write("Professionalism Grade Total: \r\n" )
        sceneFileOutput.write('%s\r\n' % self.total.queryPro().getValue1() )
        sceneFileOutput.write("-----------------------------------\r\n")
        sceneFileOutput.write("Late Deductions: - %s \r\n" % self.total.queryLate().getValue1())
        sceneFileOutput.write("-----------------------------------\r\n")
        sceneFileOutput.write("Overall Grade Total: %s \r\n" % self.total.queryTotal().getValue1())
        sceneFileOutput.close()
        
        
        pm.util.shellOutput(r"open  %s.txt " % (newPath[0]))
        
    