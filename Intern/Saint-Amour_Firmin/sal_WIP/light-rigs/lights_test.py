

import pymel.core as pm
import maya.cmds as cmds
import lights
reload(lights)

def gui():
    win = 'lighting'
    if pm.window(win, exists= True):
        pm.deleteUI(win)
        
    if pm.windowPref(win, exists= True):
        pm.windowPref(win, remove= True)
       
    global first, second   
    
    my_win = pm.window(win, title= 'lighting_tools', sizeable= True, width= 400,
                       backgroundColor= [.5, .5, .5])
    
    main_layout = pm.scrollLayout(width= 400)
    tabs = pm.tabLayout(innerMarginWidth=5, innerMarginHeight=5, width = 400)
    
    first = pm.columnLayout(adjustableColumn= True)
    global light_type
    light_type = pm.optionMenu( label='Light Type', width= 250,)
    pm.menuItem( label='Spot')
    pm.menuItem( label='Area')
    pm.menuItem( label='Directional')
    pm.menuItem( label='Point')
    pm.menuItem( label='Ambient')
    pm.menuItem( label='Volume')
    my_text = pm.textFieldButtonGrp('myText', label= 'light name', buttonLabel= 'create', 
        buttonCommand= create_light, columnWidth3= [100, 100, 100])
    
    pm.setParent(tabs)
    second = pm.columnLayout(adjustableColumn = True, width = 400)
    pm.button(label= 'Create IBL UI', command= create_ibl)
    
    pm.tabLayout( tabs, edit=True, tabLabel=((first, 'Create Lights'),(second, 'IBL UI')))
    
    
    my_win.show()
  

def create_ibl(* args):
    #light_name = pm.textFieldButtonGrp('myText', query= True, text= True)
    #print light_name, light_name
    pm.setParent(second)
    ibl = pm.ls(selection= True)[0]
    my_ibl = lights.IBL_UI(ibl).create()
  
  

def create_light(* args):
    selected = light_type.getSelect()
    
    if selected == 1:
        light_name = pm.textFieldButtonGrp('myText', query= True, text= True)
        print light_name, light_name
        pm.setParent(first)
        spot = lights.Light_spot(light_name).create()
        
    if selected == 2:
        light_name = pm.textFieldButtonGrp('myText', query= True, text= True)
        print light_name, light_name
        pm.setParent(first)
        spot = lights.Light_area(light_name).create()
        
    if selected == 3:
        light_name = pm.textFieldButtonGrp('myText', query= True, text= True)
        print light_name, light_name
        pm.setParent(first)
        spot = lights.Light_directional(light_name).create()
        
    if selected == 4:
        light_name = pm.textFieldButtonGrp('myText', query= True, text= True)
        print light_name, light_name
        pm.setParent(first)
        spot = lights.Light_point(light_name).create()
        
    if selected == 5:
        light_name = pm.textFieldButtonGrp('myText', query= True, text= True)
        print light_name, light_name
        pm.setParent(first)
        spot = lights.Light_ambient(light_name).create()
        
    if selected == 6:
        light_name = pm.textFieldButtonGrp('myText', query= True, text= True)
        print light_name, light_name
        pm.setParent(first)
        spot = lights.Light_volume(light_name).create()
