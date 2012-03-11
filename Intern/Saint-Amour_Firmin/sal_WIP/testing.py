import pymel.core as pm

import salModule as sal

win = 'testingWin'

def command01(* args):
    pm.select(cl=1)



def gui():
    if(pm.window(win, ex = True)):
        pm.deleteUI(win)
        
    if(pm.windowPref(win, ex = True)):
        pm.windowPref(win, remove = True)
    
    pm.window(win, title='Testing' , sizeable = False, mnb = True, width = 480, backgroundColor = [.5, .5, .5])
    pm.frameLayout( label = 'Grade', cll = True, cl = True , height = 880, borderStyle = 'etchedIn', w = 480 )
    mainLayout = pm.formLayout()

    
    
    test = sal.Section( name = 'Luke', layout = mainLayout , command = command01, total = command01)
    old = test.create()
    
    
    
    test01 = sal.Section( name = 'yeah', layout = mainLayout , command = command01, total = command01, control=old)
    old01 = test01.create()
    
    test02 = sal.Section( name = 'noWay', layout = mainLayout , command = command01, total = command01, control=old01)
    test02.create()
    
    pm.showWindow()
