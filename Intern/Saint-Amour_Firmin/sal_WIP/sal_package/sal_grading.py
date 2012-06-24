'''
* based on Tony's grading script

Author: Firmin Saint-Amour

Description: window contains all the grading scripts

'''

import pymel.core as pm # maya pymel
import sal_GUI as sal # custom
reload(sal)
import os # python module

print 'Grading Script Initialized'

def gui(path):
    win = 'salwindow'
    if(pm.window(win, ex = True)):
        pm.deleteUI(win)
        
    if(pm.windowPref(win, ex = True)):
        pm.windowPref(win, remove = True)
        
    myWin = pm.window(win, title='SAL_Grading' , sizeable = True, mnb = True,
                      width = 490, height = 800, backgroundColor= [.68,.68,.68],
                      toolbox= 0)
    
    main = pm.scrollLayout(width = 490)
    tabs = pm.tabLayout(innerMarginWidth=5, innerMarginHeight=5, width = 490)
    
    pm.setParent(tabs)
    first = pm.columnLayout(adjustableColumn = True, width = 490)
    proj01 = sal.Project01(path).create()
    
    pm.setParent(tabs)
    second = pm.columnLayout(adjustableColumn = True, width = 490)
    proj02 = sal.Project02(path).create()
    
    pm.setParent(tabs)
    third = pm.columnLayout(adjustableColumn = True, width = 490)
    proj03 = sal.Project03(path).create()
    
    pm.setParent(tabs)
    fourth = pm.columnLayout(adjustableColumn = True, width = 490)
    proj04 = sal.Project04(path).create()
    
    pm.setParent(tabs)
    fith = pm.columnLayout(adjustableColumn = True, width = 490)
    proj05 = sal.Project05(path).create()
    
    pm.setParent(tabs)
    sixth = pm.columnLayout(adjustableColumn = True, width = 490)
    proj06 = sal.Project06(path).create()
    
    pm.setParent(tabs)
    seventh = pm.columnLayout(adjustableColumn = True, width = 490)
    proj07 = sal.Project07(path).create()
    
    pm.setParent(tabs)
    final = pm.columnLayout(adjustableColumn = True, width = 490)
    final_proj = sal.Final_Project(path).create()
    
    # ------------------------------------------

    pm.tabLayout( tabs, edit=True, tabLabel=((first, 'Proj01'),
        (second, 'Proj02'), (third, 'Proj03 '), (fourth, 'Proj04'),
        (fith, 'Proj05'), (sixth, 'Proj06'), (seventh, 'Proj07'),
        (final, '  Final   ')) )
    
    
    myWin.show()