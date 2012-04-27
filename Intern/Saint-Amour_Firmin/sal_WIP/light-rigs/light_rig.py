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
import glob
import cPickle as pickle
import os
import lights
reload(lights)

preset_obj_list = []

class Preset_win():
    '''
    # this creates the window from which presets will be created
    # takes the path where the file will be saved as an arg
    # returns none
    '''
    def __init__(self, path):
        
        self.path = path # the path to save the presets
        
        preset_win = 'preset_win'
        if pm.window(preset_win, exists= True):
            pm.deleteUI(preset_win)
            
        if pm.windowPref(preset_win, exists= True):
            pm.windowPref(preset_win, remove= True)
            
        temp_win = pm.window(preset_win, title= 'presets', width= 300,sizeable= False)
        
        pm.columnLayout(adjustableColumn= True)
        pm.text(label= '')
        
        pm.text(label= 'Preset Name')
        self.field = pm.textField()
        pm.text(label= '')
        pm.text(label= 'Description')
        pm.text(label= '')
        self.scroll = pm.scrollField(width= 300, wordWrap= True)
        pm.text(label= '')
        pm.button(label= 'Create Preset', command= pm.Callback(self.create_preset))
        pm.text(label= '')
        
        temp_win.show()
        
    def create_preset(self):
        '''
        # creates the file for the preset
        ******
        # file pattern
        # data = ['preset name', 'light type', 'description',
                            xform_attrs[], shape_attrs[]] 
        ******
        '''
        sel = pm.ls(selection= True)[0]
        sel_shape = sel.getShape()
        node_type = pm.nodeType(sel_shape)
        
        if 'Light' not in node_type:
            return
        
        data = []
        
        data.append('%s' % (self.field.getText()))
        
        data.append('%s' % (node_type))
        
        data.append('%s' % (self.scroll.getText()))
        
        sel_data = []
        
        sel_shape_data = []
        
        sel_attrs = pm.listAttr(sel)
        sel_shape_attrs = pm.listAttr(sel_shape)
        
        for attr in sel_attrs:
            try :
                value = pm.getAttr('%s.%s' % (sel, attr))
                temp_data = (attr , value)
                sel_data.append(temp_data)
            
            except:
                pass
            
        for attr in sel_shape_attrs:
            try:
                value = pm.getAttr('%s.%s' % (sel_shape, attr))
                temp_data = (attr , value)
                sel_shape_data.append(temp_data)
            
            except:
                pass
            
            
        data.append(sel_data)
        data.append(sel_shape_data)
        
        name ='%s.light'  % (self.field.getText())
        full_path = os.path.join(self.path, name)
        f = open(full_path, 'w')
        pickle_data = pickle.dump(data, f)
        f.close()
        
        preset_ui() # this will list wil update the preset section
            
        
            
            
    
        
    
    pass

class Light_Preset_UI(object):
    '''
    # creates the ui for each light preset
    # takes in a '.light' as
    # returns none
    '''
    
    def __init__(self, attr_file):
        self.file = attr_file # the .light file
        
        f = open(self.file, 'r')
        self.data = pickle.load(f)
        f.close()
        
        
        self.xform = self.data[3]
        
        self.shape = self.data[4]
        
        
    def create(self):
        '''
        # creates the actual ui
        '''
        self.layout = pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1, 150],[2, 100], [3, 300]))
        self.checkbox = pm.checkBox(label='Apply Transforms')
        pm.button(label= 'Create Light', height=100, command= pm.Callback(self.create_light))
        pm.scrollField(width= 300, height= 100, wordWrap= True, enable= True,
                       text= 'Preset Name: %s\n'
                       % (self.data[0]) + 'Light Type: %s\n' % (self.data[1]) +
                          'Description: %s' % (self.data[2]))
        pm.separator()
        pm.separator()
        pm.separator()
 
    def delete_ui(self):
        '''
        # deletes the ui
        '''
        pm.deleteUI(self.layout)
        
    def create_light(self):
        '''
        # creates the light
        '''
        temp_light = pm.shadingNode('%s' % (self.data[1]), asLight= True)
        my_light = pm.rename(temp_light, '%s_%s' % (self.data[1], self.data[0])) # renaming
        
        my_shape = my_light.getShape() # getting shape
        
        if self.checkbox.getValue() == 1:
        
            for data in self.xform:
                try:
                    pm.setAttr('%s.%s' % (my_light, data[0]), data[1])
                    
                except:
                    pass
            
        for data in self.shape:
            try:
                pm.setAttr('%s.%s' % (my_shape, data[0]), data[1])
                
            except:
                pass
            
        pm.select(my_light)
    
class Light_rig():
    
    def __init__(self):
        pass
    
    def create(self):
        '''
        # creates the actual ui
        '''
        self.layout = pm.columnLayout()
        pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1, 180],[2, 180], [3, 180]))
        pm.text(label='Fill Type')
        pm.separator()
        pm.separator()
        pm.separator()
        
class Three_Point_Rig():
    
    def __init__(self):
        self.light_types = {1: 'spotLight', 2: 'areaLight',
                            3: 'directionalLight',4: 'pointLight',
                            5: 'ambientLight', 6: 'volumeLight'}
        
        
        self.layout = pm.columnLayout(adjustableColumn= False)
        pm.rowColumnLayout(numberOfColumns= 2, columnWidth= ([1,200], [2,150]),
                           columnAlign= ([1, 'center'], [2, 'center']))
        # fill light option menu
        self.fill_type = pm.optionMenu( label='Fill Light', width= 200)
        pm.menuItem( label='Spot')
        pm.menuItem( label='Area')
        pm.menuItem( label='Directional')
        pm.menuItem( label='Point')
        pm.menuItem( label='Ambient')
        pm.menuItem( label='Volume')
        self.fill_name = pm.textField(text= 'Fill_Light', width= 100)
        #pm.setParent('..')
        
        # key light option menu
        self.key_type = pm.optionMenu( label='key Light', width= 200)
        pm.menuItem( label='Spot')
        pm.menuItem( label='Area')
        pm.menuItem( label='Directional')
        pm.menuItem( label='Point')
        pm.menuItem( label='Ambient')
        pm.menuItem( label='Volume')
        self.key_name = pm.textField(text= 'Key_Light', width= 100)
        # rim light option menu
        #pm.setParent('..')
        self.rim_type = pm.optionMenu( label='Rim Light', width= 200)
        pm.menuItem( label='Spot')
        pm.menuItem( label='Area')
        pm.menuItem( label='Directional')
        pm.menuItem( label='Point')
        pm.menuItem( label='Ambient')
        pm.menuItem( label='Volume')
        self.rim_name = pm.textField(text= 'Rim_Light', width= 100)
        pm.setParent(self.layout)
        pm.button(label= 'Create 3 Point System', command= pm.Callback(self.create_rig),
                  width= 550)
        
    def create_fill(self):
        fill = self.fill_type.getSelect()
        fill_light = pm.shadingNode('%s' % (self.light_types[fill]),
                                                        asLight= True)
        new_light = pm.rename(fill_light, '%s' % (self.fill_name.getText()))
        
        return new_light
    
    def create_key(self):
        key = self.key_type.getSelect()
        key_light = pm.shadingNode('%s' % (self.light_types[key]),
                                                        asLight= True)
        new_light = pm.rename(key_light, '%s' % (self.key_name.getText()))
        
        return new_light
    
    def create_rim(self):
        rim = self.rim_type.getSelect()
        rim_light = pm.shadingNode('%s' % (self.light_types[rim]),
                                                        asLight= True)
        new_light = pm.rename(rim_light, '%s' % (self.rim_name.getText()))
        
        return new_light
    
    def create_rig(self):
        self.selected = pm.ls(selection= True)
        
        fill_light = self.create_fill()
        key_light = self.create_key()
        rim_light = self.create_rim()
        key_light.translate.set([6.7, 10.7, 6.7])
        key_light.rotate.set([-35, 48, 0])
        
        fill_light.translate.set([-10.01 ,9.045, 7.056])
        fill_light.rotate.set([-35, -48, 0])
        
        rim_light.translate.set([.5,10.7,-16.7])
        rim_light.rotate.set([-215, 0, 180])
        
        self.group = pm.group(empty= True, name= 'three_point_system')
        pm.parent(fill_light, key_light, rim_light, self.group)
        
        self.move_system()
        
    def move_system(self):
        
        if len(self.selected) == 0:
            return
        temp_point = pm.pointConstraint(self.selected, self.group)
        pm.delete(temp_point)
        
class duplicator(object):
    def __init__(self):
        '''
        # the duplicate light class
        # has options for the replication of lights
        '''
        self.layout = pm.columnLayout(adjustableColumn= True)
        pm.rowColumnLayout(numberOfColumns= 2,columnWidth= ([1, 250], [2, 250]),
                           columnAlign= ([1, 'center'], [2, 'center']))
        
        self.override_intensity = pm.checkBox(label= 'Override Intensity',
                                        changeCommand= self.override_intensity)
        self.int_slider = pm.intSliderGrp(field= True, enable= False,
                                          min=-500, max=500)
        
        self.override_color = pm.checkBox(label= 'Override Color',
                                        changeCommand= self.override_color)
        self.color_slider = pm.colorSliderGrp(rgb=(0, 0, 1), enable= False)
        
        self.xform = pm.checkBox(label= 'Apply Transforms')
        pm.button(label= 'Duplicate', command= self.duplicate)
        
    def override_intensity(self, * args):
        '''
        # overrides the intensity 
        '''
        if self.int_slider.getEnable() == False:
            self.int_slider.setEnable(True)
        
        else:
            self.int_slider.setEnable(False)
            
        
    def override_color(self, * args):
        '''
        # overrides the color 
        '''
        if self.color_slider.getEnable() == False:
            self.color_slider.setEnable(True)
            
        else:
            self.color_slider.setEnable(False)
        
    def duplicate(self, * args):
        '''
        # duplicates selected lights
        '''
        selected = pm.ls(sl= True)
                   
        for sel in selected:
            sel_shape = sel.getShape() # getting the shape node
            sel_type = pm.nodeType(sel_shape) # getting the node type
            
            xform = self.xform.getValue()
            
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
            
            if xform == 1:
                for attr in input_attrs:
                    try:
                        value = pm.getAttr('%s.%s' % (sel, attr))
                        pm.setAttr('%s.%s' % (new_light, attr), value)
                    
                    except:
                        pass
                    
            for attr in shape_attrs:
                try:
                    value = pm.getAttr('%s.%s' % (sel_shape, attr))
                    pm.setAttr('%s.%s' % (new_shape, attr), value)
                
                except:
                    pass
            
            pm.select(new_light)
            if self.override_intensity.getValue() == 1:
                #pm.setAttr('%s.intensity' % (new_light), self.int_slider.getValue())
                new_light.intensity.set(self.int_slider.getValue())
            
            if self.override_color.getValue() == 1:
                #pm.setAttr('%s.color' % (new_light), self.color_slider.getRgbValue())
                new_light.color.set(self.color_slider.getRgbValue())
            
        
        
def gui():
    '''
    # the gui for the tool
    '''
    #start() # loading mental ray drawing guis for all mental ray tabs
    
    win = 'lightingtools'
    if pm.window(win, exists= True):
        pm.deleteUI(win)
        
    if pm.windowPref(win, exists= True):
        pm.windowPref(win, remove= True)
        
        
    my_win = pm.window(win, title= 'Lighting', width= 550, height= 600, sizeable= True)
    pm.scrollLayout(width= 550)
    tabs = pm.tabLayout(innerMarginWidth=5, innerMarginHeight=5, width = 550)
    global scroll_list, light_row, text_field, light_type, sroll_list, lights_layout, ui_row, ibl_layout, presets_layout
    lights_layout = pm.columnLayout(width= 550)
    
    
    light_type = pm.optionMenu( label='Light Type', width= 200)
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
    duplicator_ui = duplicator()
    
    # pm.button(label= 'Duplicate Selected Lights', command= duplicate_light)
    
    pm.setParent(tabs)
    ibl_layout = pm.columnLayout(adjustableColumn= True)
    pm.button(label= 'Create IBL', command= create_ibl)
    
    pm.setParent(tabs)
    rigs_layout = pm.columnLayout(adjustableColumn= True)
    pm.frameLayout(label= '3 point light system', collapsable= True)
    three_point = Three_Point_Rig()
    pm.setParent(rigs_layout)
    pm.frameLayout(label= 'simple outdoor', collapsable= True)
    simple_outdoor = Three_Point_Rig()
    pm.setParent(rigs_layout)
    pm.frameLayout(label= 'complex outdoor', collapsable= True)
    complex_outdoor = Three_Point_Rig()
    #pm.button(label= 'Create IBL', command= create_ibl)
    
    pm.setParent(tabs)
    presets_layout = pm.columnLayout(adjustableColumn= True)
    pm.rowColumnLayout(numberOfColumns= 2, columnWidth= ([1,275], [2,275]))
    pm.button(label= 'new preset', command= create_preset)
    pm.button(label= 'refresh', command= preset_ui)
    
    
    pm.tabLayout( tabs, edit=True, tabLabel=((lights_layout, 'Lights'),
        (ibl_layout, 'IBL'), (light_utils, 'Utilities'), (rigs_layout, 'Rigs'), (presets_layout, 'Presets')))
    
    list_lights()
    list_ibls()
    
    preset_ui()
    
    my_win.show()
      
def create_preset(* args):
    '''
    # this launches the create preset window
    # by instacing the Input_win class
    '''
    
    path = os.path.dirname(__file__)
    
    full_path = os.path.join(path, 'Light_Presets')
    
    preset_win = Preset_win(full_path)
    
def preset_ui(* args):
    '''
    # this creates the ui for each preset
    '''
    path = os.path.dirname(__file__)
    base_path = os.path.join(path, 'Light_Presets')
    full_path = os.path.join(base_path, '*.light')
    
    global preset_obj_list
    
    files = glob.glob(full_path)
    
    for obj in preset_obj_list:
        try:
            obj.delete_ui()
        
        except:
            pass
    
    for f in files:
        pm.setParent(presets_layout)
        ui = Light_Preset_UI(f)
        ui.create()
        preset_obj_list.append(ui)
        
def create_ibl(* args):
    '''
    # creates an ibl
    '''
    pm.mel.eval('miCreateIbl;')
    list_ibls()
    
def list_ibls(* args):
    '''
    # this list all the ibl's in the scene
    # and creates the ui for each ibl
    # most likely there will only be one
    '''
    pm.setParent(ibl_layout)
    
    ibls = pm.ls(exactType= 'mentalrayIblShape')
    for ibl in ibls:
        ibl_ui = lights.IBL_UI(ibl).create()
    
       
def create_ui(* args):
    '''
    # this creates the ui for the selected  light from the scrollField
    '''
    selected = scroll_list.getSelectItem()[0]
    pm.select('%s' % (selected))
    selected = pm.ls(selection= True)[0]
    print 'testing :', selected
    shape = selected.getShape()
    obj_type = pm.nodeType(shape)
    
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
    '''
    # this will created a light based on what's picked from the option menu
    '''
    selected = light_type.getSelect()

    if selected == 1:
        light = pm.shadingNode('spotLight', asLight= True)
        new = pm.rename(light, '%s' % (text_field.getText()))
        pm.select(new)
        
    if selected == 2:
         light = pm.shadingNode('areaLight', asLight= True)
         new = pm.rename(light, '%s' % (text_field.getText()))
         pm.select(new)
        
    if selected == 3:
         light = pm.shadingNode('directionalLight', asLight= True)
         new = pm.rename(light, '%s' % (text_field.getText()))
         pm.select(new)
        
    if selected == 4:
         light = pm.shadingNode('pointLight', asLight= True)
         new = pm.rename(light, '%s' % (text_field.getText()))
         pm.select(new)
         
    if selected == 5:
         light = pm.shadingNode('ambientLight', asLight= True)
         new = pm.rename(light, '%s' % (text_field.getText()))
         pm.select(new)
         
    if selected == 6:
         light = pm.shadingNode('volumeLight', asLight= True)
         new = pm.rename(light, '%s' % (text_field.getText()))
         pm.select(new)
         
    list_lights()

def list_lights(* args):
    '''
    # this list all the lights in the scene
    # * does not include ibls
    '''
    lights = pm.ls(type= ['volumeLight', 'spotLight', 'directionalLight',
                'areaLight', 'pointLight', 'ambientLight']) # listing all lights in the scene
    
    scroll_list.removeAll() # clearing the text scroll list first
    
    for light in lights:
        my_light = light.getParent()
        
        scroll_list.append('%s' % (str(my_light))) # appending to the scroll list
        
def start(* args):
    # pm.mel.eval('unifiedRenderGlobalsWindow;')
    mental_ray = pm.pluginInfo('Mayatomr', query= True, loaded= True)
    
    # pm.mel.eval('unifiedRenderGlobalsWindow;')
    
    


    if mental_ray == 0:
        pm.loadPlugin('Mayatomr')
        
      
    
    tab_layout = 'unifiedRenderGlobalsWindow|rgMainForm|tabForm|mentalRayTabLayout'
    indirect = 'unifiedRenderGlobalsWindow|rgMainForm|tabForm|mentalRayTabLayout|mentalRayIndirectLightingTab'
    features = 'unifiedRenderGlobalsWindow|rgMainForm|tabForm|mentalRayTabLayout|mentalRayFeaturesTab'
    pm.setAttr('defaultRenderGlobals.currentRenderer', 'mentalRay', type= 'string')
    
    
    
    
    pm.mel.eval('isDisplayingAllRendererTabs;')
    
    pm.tabLayout(tab_layout, edit= 1, selectTab= indirect)
    pm.mel.eval('fillSelectedTabForCurrentRenderer;')
    
    pm.tabLayout(tab_layout, edit= 1, selectTab= features)
    pm.mel.eval('fillSelectedTabForCurrentRenderer;')
            
        