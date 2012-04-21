"""
Author:
    Firmin Saint-Amour
    
Description:
    General lighting tool for shortcuts
    
How to run:
    import light_rig
    light_rig.gui()
"""

import pymel.core as pm
import lights
reload(lights)

class Lights_UI():
    """
    this will create uis for selected lights
    takes a light
    returns a layout
    """
    
    def __init__(self,light):
        self.light = light
        
    def create(self):
        self.layout = pm.frameLayout(label= '%s' % (self.light), collapsable= True)
        pm.frameLayout( label='Light Attributes', collapsable= True)
        pm.attrColorSliderGrp(at= '%s.color' % (self.light),
                              columnWidth4= [100, 75, 175, 50])
    
        pm.attrFieldSliderGrp(at= '%s.intensity' % (self.light), columnWidth4= [100, 75, 175, 50])
        
        try:
            pm.attrFieldSliderGrp(at= '%s.coneAngle' % (self.light), columnWidth4= [100, 75, 175, 50])
            pm.attrFieldSliderGrp(at= '%s.penumbraAngle' % (self.light), columnWidth4= [100, 75, 175, 50])
            pm.attrFieldSliderGrp(at= '%s.dropoff' % (self.light), columnWidth4= [100, 75, 175, 50])
            
        except:
            print "#"
            
        try:
            pm.attrFieldSliderGrp(at= '%s.ambientShade' % (self.light), columnWidth4= [100, 75, 175, 50])
            
            
        except:
            print "#"
            
        try:
            
            pm.getAttr('%s.decayRate' % (self.light))
            self.decay_menu = pm.optionMenu( label='Decay Rate',
                    changeCommand= pm.Callback(self.decay_rate), width= 250)
            pm.menuItem( label='No Decay')
            pm.menuItem( label='Linear')
            pm.menuItem( label='Quadratic')
            pm.menuItem( label='Cubic')
            
            
        except:
            print "#"
            
            
        try:
            
            pm.getAttr('%s.lightShape' % (self.light))
            self.light_shape_menu = pm.optionMenu( label='Light Shape',
                    changeCommand= pm.Callback(self.light_shape), width= 250)
            pm.menuItem( label='Box')
            pm.menuItem( label='Sphere')
            pm.menuItem( label='Cylinder')
            pm.menuItem( label='Cone')
            
            
        except:
            print "#"
            
        pm.setParent(self.layout)    
        pm.frameLayout( label='Shadows', collapsable= True)
        pm.attrColorSliderGrp( at='%s.shadowColor' % (self.light),
                              columnWidth4= [100, 75, 175, 50])
        self.check_box = pm.checkBox(label= 'Use Ray Trace Shadows',
                        changeCommand= pm.Callback(self.ray_trace))
        
        try:
            pm.attrFieldSliderGrp( at='%s.lightAngle' %(self.light),
                                columnWidth4= [100, 75, 175, 50])
        except:
            print ''
            
        try:
            pm.attrFieldSliderGrp( at='%s.lightRadius' %(self.light),
                                columnWidth4= [100, 75, 175, 50])
        except:
            print ''
            
        try:
            pm.attrFieldSliderGrp( at='%s.shadowRadius' %(self.light),
                                columnWidth4= [100, 75, 175, 50])
        except:
            print ''
            
        try:
            pm.attrFieldSliderGrp( at='%s.shadowRays' %(self.light),
                                columnWidth4= [100, 75, 175, 50])
            pm.attrFieldSliderGrp( at='%s.rayDepthLimit' %(self.light),
                                columnWidth4= [100, 75, 175, 50])
            
            
        except:
            print ''
            
        pm.setParent(self.layout)
        pm.rowColumnLayout(numberOfColumns= 2, columnWidth= [200, 200])
        pm.button(label= 'Select Light', width= 200, command= pm.Callback(self.select))
        pm.button(label= 'Delete UI', width= 200, command= pm.Callback(self.delete))
            
        return self.layout
    
    def select(self):
        pm.select(self.light)
        
    
    def light_shape(self):
        selected = self.light_shape_menu.getSelect()
    
        if selected == 1:
            pm.setAttr('%s.lightShape' % (self.light), 0)
            
        if selected == 2:
            pm.setAttr('%s.lightShape' % (self.light), 1)
            
        if selected == 3:
            pm.setAttr('%s.lightShape' % (self.light), 2)
        
        if selected == 4:
            pm.setAttr('%s.lightShape' % (self.light), 3)
        
    def delete(self):
        pm.deleteUI(self.layout)
        
    def ray_trace(self):
        value = self.check_box.getValue()
        pm.setAttr('%s.useRayTraceShadows' % (self.light), int(value))
    
    def depth_map(self):
        pass
    
    def decay_rate(self):
        selected = self.decay_menu.getSelect()
    
        if selected == 1:
            pm.setAttr('%s.decayRate' % (self.light), 0)
            
        if selected == 2:
            pm.setAttr('%s.decayRate' % (self.light), 1)
            
        if selected == 3:
            pm.setAttr('%s.decayRate' % (self.light), 2)
        
        if selected == 4:
            pm.setAttr('%s.decayRate' % (self.light), 3)
    
def gui():
    win = 'lightingtools'
    if pm.window(win, exists= True):
        pm.deleteUI(win)
        
    if pm.windowPref(win, exists= True):
        pm.windowPref(win, remove= True)
        
        
    my_win = pm.window(win, title= 'Lighting', width= 550, height= 600, sizeable= True)
    pm.scrollLayout(width= 550)
    tabs = pm.tabLayout(innerMarginWidth=5, innerMarginHeight=5, width = 550)
    global scroll_list, light_row, text_field, light_type, sroll_list, lights_layout, ui_row, ibl_layout
    lights_layout = pm.columnLayout(width= 550)
    
    
    light_type = pm.optionMenu( label='Light Type', width= 200,)
    pm.menuItem( label='Spot')
    pm.menuItem( label='Area')
    pm.menuItem( label='Directional')
    pm.menuItem( label='Point')
    pm.menuItem( label='Ambient')
    pm.menuItem( label='Volume')
    
    
    text_field = pm.textFieldButtonGrp(label= 'Light Name', buttonLabel= 'Create Light', 
       buttonCommand= pm.Callback(create_light), columnWidth3= [100, 250, 200])
    
    light_row = pm.rowColumnLayout(numberOfColumns= 2, columnWidth= [150, 400])
    pm.columnLayout(width= 150, adjustableColumn=False)
    scroll_list = pm.textScrollList(width= 150, height= 200, selectCommand= pm.Callback(create_ui))
    pm.button(label= 'List Lights', command= pm.Callback(list_lights), width= 150)
    pm.setParent(light_row)
    ui_row = pm.columnLayout(width= 400)
    
    pm.setParent(tabs)
    light_utils = pm.columnLayout(adjustableColumn= True)
    pm.button(label= 'Duplicate Selected Lights', command= duplicate_light)
    
    pm.setParent(tabs)
    ibl_layout = pm.columnLayout(adjustableColumn= True)
    pm.button(label= 'Create IBL', command= create_ibl)
    
    pm.setParent(tabs)
    rigs_layout = pm.columnLayout(adjustableColumn= True)
    pm.button(label= 'Create IBL', command= create_ibl)
    
    
    pm.tabLayout( tabs, edit=True, tabLabel=((lights_layout, 'Lights'),(ibl_layout, 'IBL'), (light_utils, 'Utilities'), (rigs_layout, 'Rigs')))
    
    list_lights()
    list_ibls()
    
    my_win.show()
    
def create_ibl(* args):
    pm.mel.eval('miCreateIbl;')
    list_ibls()
    
def list_ibls(* args):
    pm.setParent(ibl_layout)
    
    ibls = pm.ls(exactType= 'mentalrayIblShape')
    for ibl in ibls:
        ibl_ui = lights.IBL_UI(ibl).create()
    
def duplicate_light(* args):
    selected = pm.ls(sl= True)
    print selected                
    
    for sel in selected:
        sel_shape = sel.getShape() # getting the shape node
        sel_type = pm.nodeType(sel_shape) # getting the node type
        
        if 'Light' not in sel_type:
            print '# wrong object type ', sel
            continue
        # creating a new light based on the recieved node type
        new_light = pm.shadingNode('%s' % (sel_type), asLight= True)
        new_light = pm.rename(new_light, '%s_copy' % (sel)) # renaming
        new_shape = new_light.getShape() # getting the shape
        # listing transform attrs
        input_attrs = pm.listAttr(sel) 
        # listing shape attrs
        shape_attrs = pm.listAttr(sel_shape)
        
        for attr in input_attrs:
            try:
                value = pm.getAttr('%s.%s' % (sel, attr))
                pm.setAttr('%s.%s' % (new_light, attr), value)
                #print '%s.%s' % (new_light, attr), value
                
            except:
                #print '# could not set attr:', attr
                pass
                
                
                
                
        for attr in shape_attrs:
            try:
                value = pm.getAttr('%s.%s' % (sel_shape, attr))
                pm.setAttr('%s.%s' % (new_shape, attr), value)
                #print '%s.%s' % (new_light, attr), value
                
            except:
                #print '# could not set attr:', attr
                pass
        
def create_ui(* args):
    selected = scroll_list.getSelectItem()[0]
    pm.select('%s' % (selected))
    selected = pm.ls(selection= True)[0]
    print 'testing :', selected
    shape = selected.getShape()
    pm.select('%s' % (shape))
    obj_type = pm.ls(selection= True, showType= True)[-1]
    
    pm.setParent(ui_row)
    
    if '%s' % (obj_type) == 'spotLight':
        light = lights.Light_spot(light= '%s' % (selected))
        light.create()
        
        
    if '%s' % (obj_type) == 'directionalLight':
        light = lights.Light_directional(light= '%s' % (selected))
        light.create()
        
        
    if '%s' % (obj_type) == 'ambientLight':
        light = lights.Light_ambient(light= '%s' % (selected))
        light.create()
        
        
    if '%s' % (obj_type) == 'areaLight':
        light = lights.Light_area(light= '%s' % (selected))
        light.create()
        
        
    if '%s' % (obj_type) == 'pointLight':
        light = lights.Light_point(light= '%s' % (selected))
        light.create()
        
        
    if '%s' % (obj_type) == 'volumeLight':
        light = lights.Light_volume(light= '%s' % (selected))
        light.create()
           
def create_light(* args):
    selected = light_type.getSelect()

    if selected == 1:
        light = pm.shadingNode('spotLight', asLight= True,
                               name= '%s' % (text_field.getText()))
        
        pm.rename(light, '%s' % (text_field.getText()))
        
        #pm.spotLight(name= '%s' % (text_field.getText()))
        
    if selected == 2:
         light = pm.shadingNode('areaLight', asLight= True,
                               name= '%s' % (text_field.getText()))
        
         pm.rename(light, '%s' % (text_field.getText()))
         
         #pm.areaLight(name= '%s' % (text_field.getText()))
        
    if selected == 3:
         light = pm.shadingNode('directionalLight', asLight= True,
                               name= '%s' % (text_field.getText()))
        
         pm.rename(light, '%s' % (text_field.getText()))
         
         #pm.directionalLight(name= '%s' % (text_field.getText()))
        
    if selected == 4:
         light = pm.shadingNode('pointLight', asLight= True,
                               name= '%s' % (text_field.getText()))
        
         pm.rename(light, '%s' % (text_field.getText()))
         
         #pm.pointLight(name= '%s' % (text_field.getText()))
        
    if selected == 5:
         light = pm.shadingNode('ambientLight', asLight= True,
                               name= '%s' % (text_field.getText()))
        
         pm.rename(light, '%s' % (text_field.getText()))
         
         #pm.ambientLight(name= '%s' % (text_field.getText()))
        
    if selected == 6:
         light = pm.shadingNode('volumeLight', asLight= True,
                               name= '%s' % (text_field.getText()))
        
         pm.rename(light, '%s' % (text_field.getText()))
         #pm.volumeLight(name= '%s' % (text_field.getText()))
         
    list_lights()

def list_lights(* args):
    lights = pm.ls(type= ['volumeLight', 'spotLight', 'directionalLight',
                'areaLight', 'pointLight', 'ambientLight']) # listing all lights in the scene
    
    scroll_list.removeAll() # clearing the text scroll list first
    
    for light in lights:
        my_light = light.getParent()
        
        scroll_list.append('%s' % (str(my_light))) # appending to the scroll list
        
        