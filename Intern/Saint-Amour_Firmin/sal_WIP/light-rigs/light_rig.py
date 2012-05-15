"""
Author:
    Firmin Saint-Amour
    
Description:
    General lighting tool for shortcuts
    
How to run:
    import light_rig
    light_rig.gui()
"""
from maya import cmds
import pymel.core as pm
import glob
import cPickle as pickle
import os
import lights
reload(lights)

preset_obj_list = []
obj_ui_list = []
lights_dict = {}


class IBL_section():
    def __init__(self):
        self.uis = [] # list of uis
        self.main_layout = pm.columnLayout(adjustableColumn= True)
        pm.button(label= 'Create IBLs', command = pm.Callback(self.create_ibl))
        self.main_layout = pm.rowColumnLayout(numberOfColumns= 2, columnWidth= [150, 400])
        pm.columnLayout(width= 150, adjustableColumn=False)
        self.scroll_list = pm.textScrollList(width= 150, height= 200,
                                  selectCommand= pm.Callback(self.create_ui),
                                                    allowMultiSelection= False)
        pm.button(label= "List IBL's", command= pm.Callback(self.list_ibls),
                        width= 150)
        pm.setParent(self.main_layout)
        self.ui_layout = pm.columnLayout(width= 400)
    
    def create_ibl(self):
        my_ibl = pm.shadingNode('mentalrayIblShape', asLight= True)
        pm.connectAttr('%s.message' % (my_ibl),
                   'mentalrayGlobals.imageBasedLighting', force= True)
        pm.setAttr('%s.primaryVisibility' % (my_ibl), 1)
        pm.setAttr('%s.visibleInReflections' % (my_ibl), 1)
        pm.setAttr('%s.visibleInRefractions' % (my_ibl), 1)
        pm.setAttr('%s.visibleInEnvironment' % (my_ibl), 1)
        pm.setAttr('%s.visibleInFinalGather' % (my_ibl), 1)
        
        scene_objects = pm.ls(type= ['mesh', 'nurbsSurface'])

        bounding_box = pm.exactWorldBoundingBox(scene_objects)
        bounding_box.sort()
    
        ibl_size = bounding_box[-1]

        pm.setAttr('%s.scaleX' % (my_ibl), ibl_size)
        pm.setAttr('%s.scaleY' % (my_ibl), ibl_size)
        pm.setAttr('%s.scaleZ' % (my_ibl), ibl_size)
        
    def create_ui(self):
        pm.setParent(self.ui_layout)
        if len(self.uis) > 1:
            for ui in self.uis:
                
                try:
                    ui.delete_ui()
                    self.uis.remove(ui)
                
                except:
                    pass
        
        ibl = self.scroll_list.getSelectItem()[0]
        ui = lights.IBL_UI(ibl).create()
        self.uis.append(ui)
        
    def list_ibls(self):
        ibls = pm.ls(exactType= 'mentalrayIblShape')
        for ibl in ibls:
            self.scroll_list.append('%s' % (ibl))

class Fog_editor(object):
    '''
    # class for connecting and disconnecting lights to parti_volume nodes
    '''
    def __init__(self):
        
        self.parti_nodes = []
        self.scene_lights = []
        self.parti_lights = []
        
        self.parti_dict = {}
        self.parti_lights_dict = {}
        self.scene_lights_dict = {}
        
        pm.columnLayout(adjustableColumn= True)
        main = pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,180],
            [2, 180], [3,180]))
        pm.columnLayout(adjustableColumn= True)
        pm.text(label= 'Parti Volumes')
        self.parti_scroll = pm.textScrollList(width= 180, height= 125,
                            selectCommand = pm.Callback(self.get_input_lights))
        pm.button(label= 'Refresh', command= pm.Callback(self.refresh_nodes))
        
        pm.setParent('..')
        pm.columnLayout(adjustableColumn= True)
        pm.text(label= 'Parti Lights')
        self.parti_light_scroll = pm.textScrollList(width= 180, height= 125)
        pm.rowColumnLayout(numberOfColumns= 2, columnWidth= ([1, 90], [2, 90]))
        pm.button(label= '+', command= pm.Callback(self.add_light))
        pm.button(label= '-', command= pm.Callback(self.remove_light))
        
        pm.setParent(main)
        pm.columnLayout(adjustableColumn= True)
        pm.text(label= 'Scene Lights')
        self.light_scroll = pm.textScrollList(width= 180, height= 125)
        pm.button(label= 'Refresh', command= pm.Callback(self.refresh_lights))
        
        self.refresh_lights()
        self.refresh_nodes()
        
    def get_input_lights(self):
        '''
        # get a list of the input lights
        # and append them to the related text scroll list
        '''
        node = self.parti_scroll.getSelectItem()[0]
        self.parti_lights = self.parti_dict[node].inputs()
        self.parti_light_scroll.removeAll()
        
        for light in self.parti_lights:
            self.parti_light_scroll.append('%s' % (light))
            self.parti_lights_dict['%s' % (light)] = light
            
        
    def add_light(self):
        '''
        # connects the selected light to the selected parti_volume node
        '''
        light = self.light_scroll.getSelectItem()[0]
        node = self.parti_dict[self.parti_scroll.getSelectItem()[0]]
        index = len(self.parti_lights)
        #inputs = node.inputs()
        #index_list = []
        
       
        pm.connectAttr('%s.message' % (light),
                                    '%s.lights[%s]' % (node, str(index)))
                
        self.get_input_lights()
            
    def reorder_input_lights(self):
        '''
        # this will reorder the light connections
        # so adding the lights will be easier
        # that way i can just add a light based
            on the len(self.parti_lights)
        # connectAttr(light.message, node.lights[len(self.parti_lights)])    
        '''
        node = self.parti_scroll.getSelectItem()[0]
        temp_remove_index = ''
        
        # removing the connections
        for light in self.parti_lights:
            light_shape = light.getShape()
            conn = cmds.listConnections('%s' % (light), c= 1, plugs= 1)
            for c in conn:
            # checking if there's an attribute named:
            # '%s.lights' % (parti_volume_node)
            # if the attributes exist it wil return
            # '%s.lights[some #]' % (parti_volume_node)
            # so that way i can konw which index to use to disconnect the light
                if '%s.lights' % (node) in c:
                    temp_remove_index = conn[conn.index(c)]
                    
                try:
                    pm.disconnectAttr('%s.message' % (light_shape),
                                    '%s' % (temp_remove_index))
                    
                except:
                    pass
                    
                
                    
        # reconnecting everything
        # but in order
        i = 0
        while i < len(self.parti_lights):
            
            try:
                pm.connectAttr('%s.message' % (self.parti_lights[i].getShape()),
                            '%s.lights[%s]' % (node, str(i)))
                
            except:
                pass
            
            i += 1
                    
          
        self.get_input_lights()
    
    def remove_light(self):
        '''
        # disconnect the selected light from the selected parti_volume node
        '''
        node = self.parti_scroll.getSelectItem()[0]
        light = self.parti_light_scroll.getSelectItem()[0]
        light_shape = self.parti_lights_dict[light].getShape()
        # listing the connections
        conn = cmds.listConnections('%s' % (light_shape), c= 1, plugs= 1)
        
        self.remove_index = ''
        
        print node, light, light_shape
        
        for c in conn:
            # checking if there's an attribute named:
            # '%s.lights' % (parti_volume_node)
            # if the attributes exist it wil return
            # '%s.lights[some #]' % (parti_volume_node)
            # so that way i can konw which index to use to disconnect the light
            if '%s.lights' % (node) in c:
                self.remove_index = conn[conn.index(c)]
                print self.remove_index
                
                
        try:
            pm.disconnectAttr('%s.message' % (light_shape),
                                    '%s' % (self.remove_index))
        except:
            pm.disconnectAttr('%s.message' % (light),
                                    '%s' % (self.remove_index))
            
                    
        
        
        self.get_input_lights()
        
        self.reorder_input_lights()
                
    def refresh_lights(self):
        # listing all lights in the scene
        self.scene_lights = pm.ls(type= ['volumeLight', 'spotLight', 'directionalLight',
                'areaLight', 'pointLight', 'ambientLight'])
        
        self.light_scroll.removeAll()
        
        for light in self.scene_lights:
            try:
                light = light.getShape()
                self.scene_lights_dict['%s' % (light)] = light
                self.light_scroll.append('%s' % (light))
            except:
                self.scene_lights_dict['%s' % (light)] = light
                self.light_scroll.append('%s' % (light))
    
    def refresh_nodes(self):
        '''
        # this will list all the parti_volume nodes in the scene
        # and append them to the relating text scroll list
        '''
        self.parti_nodes = pm.ls(type= 'parti_volume')
        self.parti_scroll.removeAll()
        for node in self.parti_nodes:
            self.parti_dict['%s' % (node)] = node
            self.parti_scroll.append('%s' % node)
            
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
        
        preset_ui() # this will list will update the preset section
            
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
            
class Menu_item(object):
    '''
    # creates a option menu with menu items
    '''
    def __init__(self):
        self.option_menu = pm.optionMenu( label='Light Type', width= 200)
        pm.menuItem( label='Spot')
        pm.menuItem( label='Area')
        pm.menuItem( label='Directional')
        pm.menuItem( label='Point')
        pm.menuItem( label='Ambient')
        pm.menuItem( label='Volume')
        
    def get_value(self):
        '''
        # gets the the selected menu item
        '''
        value = self.option_menu.getSelect()
        return value
    
    def delete_ui(self):
        '''
        # deletes the ui and the object
        '''
        pm.deleteUI(self.option_menu)
        del self
        
class Fog_creator(object):
    # mrCreateCustomNode -asUtility "" physical_light;
    # // Result: Connected physical_light1.message to fog_lightShape.mentalRayControls.miLightShader. // 
    def __init__(self):
        self.menu_item_list = []
        self.light_types = {1: 'spotLight', 2: 'areaLight',
                            3: 'directionalLight',4: 'pointLight',
                            5: 'ambientLight', 6: 'volumeLight'}
        
        self.layout = pm.columnLayout(adjustableColumn= False)
        self.checkBox = pm.checkBox(label= 'Use Physical Light')
        self.slider = pm.intSliderGrp(label= 'Number Of lights', field= True,
                                min= 0,max= 20,columnWidth3 = [200,75,200],
                            changeCommand=pm.Callback(self.create_menu_items))
        self.menu_layout = pm.columnLayout()
        pm.setParent('..')
        
        pm.button(label= 'Create Fog System', width= 500,
                  command= pm.Callback(self.create_system01))
        
    def create_menu_items(self):
        value = self.slider.getValue()
        for item in self.menu_item_list:
            try:
                item.delete_ui()
                self.menu_item_list.remove(item)
            except:
                print item
                pass
           
            
        for i in xrange(value):
            pm.setParent(self.menu_layout)
            ui = Menu_item()
            self.menu_item_list.append(ui)
            
        print self.menu_item_list
        
        
    def create_system01(self):
        step = 0
        index = 0
        values = []
        lights_list = []
        for item in self.menu_item_list:
            value = item.get_value()
            values.append(value)
            
        for value in values:
            light_node = pm.shadingNode('%s' % (self.light_types[value]),
                                                    asLight= True)
            light_node.translate.set(step,15,0)
            step += 2
            light_node.rotate.set(-90,0,0)
            node_type = pm.nodeType(light_node.getShape())
            light = pm.rename(light_node, 'fog_%s' % (node_type))
            lights_list.append(light)
            
        if self.checkBox.getValue() == 1:
            
            
            for light in lights_list:
                
                phys_light = pm.mel.eval('mrCreateCustomNode -asUtility "" physical_light;')
            
                pm.connectAttr('%s.message' % (phys_light),
                     '%s.mentalRayControls.miLightShader' % (light.getShape()))
                
        shader = pm.shadingNode('transmat', asShader= True)
        volume = pm.polyCube(name= 'fog_volume', width=60,
                                        height=60, depth=60)[0]
        
        pm.hyperShade(volume, assign= shader)
        
        parti_volume = pm.mel.eval('mrCreateCustomNode -asShader "" parti_volume;')
        pm.setAttr('%s.scatter' % (parti_volume), 1,1,1, type= 'double3' )
        
        pm.setAttr('%s.min_step_len' % (parti_volume), .03)
        pm.setAttr('%s.max_step_len' % (parti_volume), .2)
        
        pm.connectAttr('%s.outValue' % (parti_volume),
                       '%sSG.miVolumeShader' % (shader), force= True)
        
        
        for light in lights_list:
            
            pm.connectAttr('%s.message' % (light.getShape()),
                    '%s.lights[%s]' % (parti_volume, str(index)), force= True)
            
            index += 1
                
        
            
        
            
            
            
        
        
        
        
    def create_system(self):
        
        shader = pm.shadingNode('transmat', asShader= True)
        volume = pm.polyCube(name= 'fog_volume', width=40,
                                        height=40, depth=40)[0]
        
        pm.hyperShade(volume, assign= shader)
        
        parti_volume = pm.mel.eval('mrCreateCustomNode -asShader "" parti_volume;')
        pm.setAttr('%s.scatter' % (parti_volume), 1,1,1, type= 'double3' )
        
        pm.setAttr('%s.min_step_len' % (parti_volume), .03)
        pm.setAttr('%s.max_step_len' % (parti_volume), .2)
        
        pm.connectAttr('%s.outValue' % (parti_volume),
                       '%sSG.miVolumeShader' % (shader), force= True)
        
        light_node = pm.shadingNode('%s' % (self.light_types[value]),
                                                    asLight= True)
        light_node.translate.set(0,15,0)
        light_node.rotate.set(-90,0,0)
        light = pm.rename(light_node, 'fog_light')
        
        pm.connectAttr('%s.message' % (light.getShape()),
                                '%s.lights[0]' % (parti_volume), force= True)
        if self.checkBox.getValue() == 1:
            # mrCreateCustomNode -asUtility "" physical_light;
            # // Result: Connected physical_light1.message to fog_lightShape.mentalRayControls.miLightShader. // 
            phys_light = pm.mel.eval('mrCreateCustomNode -asUtility "" physical_light;')
            
            pm.connectAttr('%s.message' % (phys_light),
                     '%s.mentalRayControls.miLightShader' % (light.getShape()))
            
        
def gui():
    '''
    # the gui for the tool
    '''
    load_mr() # loading mental ray drawing guis for all mental ray tabs
    
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
    scroll_list = pm.textScrollList(width= 150, height= 200,
        selectCommand= pm.Callback(create_ui), allowMultiSelection= True)
    pm.button(label= 'List Lights', command= pm.Callback(list_lights), width= 150)
    pm.setParent(light_row)
    ui_row = pm.columnLayout(width= 400)
    
    pm.setParent(tabs)
    light_utils = pm.columnLayout(adjustableColumn= True)
    pm.frameLayout(label= 'Duplicate Lights')
    duplicator_ui = duplicator()
    
    pm.setParent('..')
    pm.frameLayout(label= 'Fog Editor')
    fog_editor_ui = Fog_editor()
    
    
    # pm.button(label= 'Duplicate Selected Lights', command= duplicate_light)
    
    pm.setParent(tabs)
    ibl_layout = pm.columnLayout(adjustableColumn= True)
    # pm.button(label= 'Create IBL', command= create_ibl)
    ibls_ui = IBL_section()
    
    pm.setParent(tabs)
    rigs_layout = pm.columnLayout(adjustableColumn= True)
    pm.frameLayout(label= 'Three Point System')
    pm.text(label='')
    three_point = Three_Point_Rig()
    pm.text(label='')
    pm.setParent(rigs_layout)
    pm.frameLayout(label= 'Simple Outdoor System')
    pm.text(label='')
    pm.button(label='Simple Outdoor', command= simple_outdoor)
    pm.text(label='')
    pm.setParent(rigs_layout)
    pm.frameLayout(label= 'Complex Outdoor System')
    pm.text(label='')
    pm.button(label='Complex Outdoor', command= complex_outdoor)
    pm.text(label='')
    pm.setParent(rigs_layout)
    pm.frameLayout(label= u'Smoke & Fog')
    pm.text(label='')
    smoke_fog = Fog_creator()
    pm.text(label='')
    
    pm.setParent(tabs)
    presets_layout = pm.columnLayout(adjustableColumn= True)
    pm.rowColumnLayout(numberOfColumns= 2, columnWidth= ([1,275], [2,275]))
    pm.button(label= 'new preset', command= create_preset)
    pm.button(label= 'refresh', command= preset_ui)
    
    
    pm.tabLayout( tabs, edit=True, tabLabel=((lights_layout, 'Lights'),
        (ibl_layout, 'IBL'), (light_utils, 'Utilities'), (rigs_layout, 'Rigs'), (presets_layout, 'Presets')))
    
    list_lights()
    #list_ibls()
    
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
    
    my_ibl = pm.shadingNode('mentalrayIblShape', asLight= True)
    pm.connectAttr('%s.message' % (my_ibl),
                   'mentalrayGlobals.imageBasedLighting', force= True)
    pm.setAttr('%s.primaryVisibility' % (my_ibl), 1)
    pm.setAttr('%s.visibleInReflections' % (my_ibl), 1)
    pm.setAttr('%s.visibleInRefractions' % (my_ibl), 1)
    pm.setAttr('%s.visibleInEnvironment' % (my_ibl), 1)
    pm.setAttr('%s.visibleInFinalGather' % (my_ibl), 1)
    
    scene_objects = pm.ls(type= ['mesh', 'nurbsSurface'])

    bounding_box = pm.exactWorldBoundingBox(scene_objects)
    bounding_box.sort()
    
    ibl_size = bounding_box[-1]

    pm.setAttr('%s.scaleX' % (my_ibl), ibl_size)
    pm.setAttr('%s.scaleY' % (my_ibl), ibl_size)
    pm.setAttr('%s.scaleZ' % (my_ibl), ibl_size)
    
    return my_ibl
    
    
    
    
def simple_outdoor(* args):
    create_ibl()
    my_node = pm.shadingNode('directionalLight', asLight= True)
    pm.rename(my_node, 'Sun')
    
def complex_outdoor(* args):
    create_ibl()
    my_sun = pm.shadingNode('directionalLight', asLight= True)
    pm.rename(my_sun, 'Sun')
    my_sky = pm.shadingNode('areaLight', asLight= True)
    new_light = pm.rename(my_sky, 'Sky')
    new_light.translate.set(0,16,0)
    new_light.rotate.set(-90,0,0)
    new_light.scale.set(16,16,16)
    

    
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
    selected = scroll_list.getSelectItem()
    global lights_dict
    global obj_ui_list
    
    
    
    for obj in obj_ui_list:
        try:
            obj.delete()
            
        except:
            pass
    
    
    for sel in selected:
        pm.setParent(ui_row)
        #pm.select('%s' % (sel))
        #node = pm.ls(selection= True)[0]
        print sel
        print lights_dict
        #shape = lights_dict[sel]
        obj_type = pm.nodeType('%s' % (lights_dict[u'%s' %(str(sel))]))
        if '%s' % (obj_type) == 'spotLight':
            light = lights.Light_spot(light= '%s' % (sel))
            light.create()
            obj_ui_list.append(light)
            
            
        if '%s' % (obj_type) == 'directionalLight':
            light = lights.Light_directional(light= '%s' % (sel))
            light.create()
            obj_ui_list.append(light)
            
            
        if '%s' % (obj_type) == 'ambientLight':
            light = lights.Light_ambient(light= '%s' % (sel))
            light.create()
            obj_ui_list.append(light)
            
            
        if '%s' % (obj_type) == 'areaLight':
            light = lights.Light_area(light= '%s' % (sel))
            light.create()
            obj_ui_list.append(light)
            
            
        if '%s' % (obj_type) == 'pointLight':
            light = lights.Light_point(light= '%s' % (sel))
            light.create()
            obj_ui_list.append(light)
            
            
        if '%s' % (obj_type) == 'volumeLight':
            light = lights.Light_volume(light= '%s' % (sel))
            light.create()
            obj_ui_list.append(light)
           
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
    global lights_dict
    lights_dict = {}
    print lights_dict
    lights = pm.ls(type= ['volumeLight', 'spotLight', 'directionalLight',
                'areaLight', 'pointLight', 'ambientLight']) # listing all lights in the scene
    
    scroll_list.removeAll() # clearing the text scroll list first
    
    for light in lights:
        my_light = light.getParent()
        lights_dict['%s' % (my_light)] = '%s' % (light)
        
        scroll_list.append(my_light) # appending to the scroll list
        
    print lights_dict
        
def load_mr(* args):
    mental_ray = pm.pluginInfo('Mayatomr', query= True, loaded= True)
    
    
    if mental_ray == 0:
        pm.loadPlugin('Mayatomr')
        
    pm.setAttr('defaultRenderGlobals.ren', 'mentalRay', type='string')
        
      
    
    
        