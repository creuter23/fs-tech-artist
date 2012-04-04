'''
* based on Tony's grading script

Author: Firmin Saint-Amour

Description: window contains all the grading scripts

'''

import pymel.core as pm
import sal_GUI as sal
reload(sal)
import os

def gui(path):
    win = 'salwindow'
    if(pm.window(win, ex = True)):
        pm.deleteUI(win)
        
    if(pm.windowPref(win, ex = True)):
        pm.windowPref(win, remove = True)
        
    myWin = pm.window(win, title='SAL_Grading' , sizeable = True, mnb = True, width = 490, height = 900, backgroundColor= [.68,.68,.68])
    main = pm.scrollLayout(width = 490)
    tabs = pm.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    
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


    
    
    
    pm.tabLayout( tabs, edit=True, tabLabel=((first, 'Project1'), (second, 'Project2'), (third, 'Project3'), (fourth, 'Project4')) )
    
    
    myWin.show()