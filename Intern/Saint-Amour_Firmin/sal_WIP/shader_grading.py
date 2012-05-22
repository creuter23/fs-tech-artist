'''

Author:
    Firmin Saint-Amour
    
Description:
    Script to quickly grade shaders
    
How to run:
    import shader_grading
    shader_grader.gui()
    
'''

import pymel.core as pm
from maya import cmds

class Shader_sorter(object):
    
    def __init__(self):
        '''
        # class to sort and give info on shaders
        '''
        
        self.layout = pm.rowColumnLayout(numberOfColumns= 3, columnWidth=([1, 150],
                                                [2, 150], [3, 250]))
        pm.columnLayout()
        pm.text(label= 'Shaders')
        self.shader_list = pm.textScrollList(width= 150, height= 200,
                       selectCommand= pm.Callback(self.update_connections_list))
        pm.button(label= 'Refresh', width= 150,
                  command= pm.Callback(self.update_shader_list))
        
        pm.setParent(self.layout)
        pm.columnLayout()
        pm.text(label='Connections')
        self.connections_list = pm.textScrollList(width= 150, height= 200,
                       selectCommand= pm.Callback(self.write_info))
        self.check_box = pm.checkBox(label= 'Select Node')
        
        pm.setParent(self.layout)
        pm.columnLayout()
        pm.text(label='Node Info')
        self.info_field = pm.scrollField(wordWrap= True, width= 250, height= 200)
        
        self.attr_check_box = pm.checkBox(label= 'Show All')
        
        
        self.update_shader_list()
             
    def update_shader_list(self):
        '''
        # updates the shader list and the shader scroll list
        '''
        self.mat_list = pm.ls(mat= True)
        self.mat_dict = {} # dictionary of material objects
        
        self.shader_list.removeAll()
        for mat in self.mat_list:
            self.mat_dict['%s' % (mat)] = mat
            if '%s' % (mat) == 'lambert1' or mat == 'shaderGlow1' or \
                            mat == 'particleCloud1':
                continue
            self.shader_list.append('%s' % (mat))
            
    def update_connections_list(self):
        '''
        # updates the connections for the selected shader
        '''
        mat = self.shader_list.getSelectItem()[0]
        if self.check_box.getValue() == 1:
            pm.select(mat)
        
        
        shader_connections = self.mat_dict[mat].inputs()
        
        node_connections = []
        
        self.connections_dict = {} # dictionary of connections objects
        
        
        for x in shader_connections:
            node_connections.append(x)
            self.connections_dict['%s' % (x)] = x
            inputs = x.inputs()
            
            
            
            if inputs > 0:
                for i in inputs:
                    if i in node_connections:
                        continue
                    node_connections.append(i)
                    self.connections_dict['%s' % (i)] = i
                    inputs = i.inputs()
                    
                    if inputs > 0:
                        for i in inputs:
                            if i in node_connections:
                                continue
                            node_connections.append(i)
                            self.connections_dict['%s' % (i)] = i
                            inputs = i.inputs()
                            
                            if inputs > 0:
                                for i in inputs:
                                    if i in node_connections:
                                        continue
                                    node_connections.append(i)
                                    self.connections_dict['%s' % (i)] = i
         
        
        node_connections.sort()
        
        self.connections_list.removeAll()
        
        for node in node_connections:
            self.connections_list.append('%s' % (node))
            
    def get_ramp_attrs(self, ramp):
        ramp_type = {0:'V Ramp', 1:'U Ramp',2:'Diagonal Ramp',
                     3:'Radial Ramp', 4:'Circular Ramp', 5:'Box Ramp',
                     6:'UV Ramp', 7:'Four Corner Ramp', 8:'Tartan Ramp'}
        
        interp_type = {0:'None', 1:'Linear',2:'Exponential Up',
                     3:'Exponential Down', 4:'Smooth', 5:'Bump',
                     6:'Spike'}
        
        type_value = pm.getAttr('%s.type' % (ramp))
        interp_value = pm.getAttr('%s.interpolation' % (ramp))
        u_wave = pm.getAttr('%s.uWave' % (ramp))
        v_wave = pm.getAttr('%s.vWave' % (ramp))
        noise = pm.getAttr('%s.noise' % (ramp))
        noise_freq = pm.getAttr('%s.noiseFreq' % (ramp))
        
        output = ['Type: %s' % (ramp_type[type_value]),
                  'Interpolation: %s' % (interp_type[interp_value]),
                  'U Wave: %s' % (u_wave), 'V Wave: %s' % (v_wave),
                  'Noise: %s' % (noise), 'Noise Frequency: %s' % (noise_freq)]
        
        
        
        return output
    
    def get_noise_attrs(self, noise):
        noise_type = {0:'Perlin Noise', 1:'Billow',2:'Wave',
                     3:'Wispy', 4:'Space Time'}
        output= []
        
        value = pm.getAttr('%s.noiseType' % (noise))
        
        output.append('Noise Type: %s' % (noise_type[value]))
       
        attrs = pm.listAttr(noise, keyable= True, settable= True, write= True,
                            hasData= True)
        
        for attr in attrs:
            if attr == 'noiseType':
                continue
            value = pm.getAttr('%s.%s' % (noise, attr))
            
            output.append('%s: %s' % (attr, value))
            
        
        return output
    
    def get_layered_texture_input_index(self, node, child):
        
        conn = cmds.listConnections('%s' % (child), c= 1, plugs= 1)
        
        for c in conn:
            
            if '%s.inputs' % (node) in c:
                return c
        
    def get_layered_texture_attrs(self, node):
        blend_mode = {0:'None', 1:'Over', 2:'In', 3:'Out', 4:'Add',
                      5:'Subtract', 6:'Multiply', 7:'Difference', 8:'Lighten',
                      9:'Darken', 10:'Saturate', 11:'Desaturate',
                      12:'Illuminate'}
        
        output = []
        inputs = node.inputs()
        for i in inputs:
            attr = self.get_layered_texture_input_index(node, i)
            
            new_attr = attr.split('.color')[0]
            mode = pm.getAttr('%s.blendMode' % (new_attr))
            output.append("Layer '%s' Blend Mode: %s" % (i, blend_mode[mode]))
            
            
        
        
        return output
                    
    def write_info(self):
        
        self.info_field.setText('')
        
        node = self.connections_list.getSelectItem()[0]
        if self.check_box.getValue() == 1:
            pm.select(node)
        
        node_type = pm.nodeType(node)
        #print node_type
        
        
        if node_type == 'layeredTexture':
            result = self.get_layered_texture_attrs(self.connections_dict[node])
            for r in result:
                self.info_field.insertText('%s\n' % (r) )
                
        if node_type == 'ramp':
            result = self.get_ramp_attrs(node)
            for r in result:
                self.info_field.insertText('%s\n' % (r) )
                
        if node_type == 'noise':
            result = self.get_noise_attrs(node)
            for r in result:
                self.info_field.insertText('%s\n' % (r) )
                
        if node_type != 'ramp' and node_type != 'noise':
            if self.attr_check_box.getValue() == 1:
                attrs = pm.listAttr('%s' % (node), write= True, settable= True,
                            keyable= True)
                
            if self.attr_check_box.getValue() == 0:
                attrs = pm.listAttr('%s' % (node), write= True, settable= True,
                            keyable= True, inUse= True)
                
            for attr in attrs:
                try:
                    value = pm.getAttr('%s.%s' % (node, attr))
                    self.info_field.insertText('%s: %s\n' % (attr, value))
                except:
                    pass
          
class Lambert_object_button(object):
    '''
    # this creates a button for and object
    # the label of the button is the name of the object
    # the button selects the objects
    '''
    def __init__(self, obj):
        self.obj = obj.getParent()
        pm.button(label= '%s' % (self.obj), command= pm.Callback(self.select))
        
    def select(self):
        pm.select('%s' % (self.obj))

class Lambert_objects_checker(object):
    '''
    # class for objects that have the default lambert material
    # checks the scene for any polygon or nurbs object with a default lambert
    '''
    def __init__(self):
        
        self.lambert_objs = []
        self.main_layout = pm.columnLayout(adjustableColumn= True)
        self.buttons_layout = pm.rowColumnLayout(numberOfColumns= 3,
                    columnWidth= ([1,180], [2,180], [3,180]))
        pm.setParent(self.main_layout)
        self.layout = pm.columnLayout(adjustableColumn= True)
        self.scene_objs = pm.ls(type= ['mesh', 'nurbsSurface'])
        
        for obj in self.scene_objs:
            shaders = obj.outputs()
            for shader in shaders:
                if '%s' % (shader) == 'initialShadingGroup':
                    self.lambert_objs.append(obj)
                    
        self.create_buttons()
              
    def create_buttons(self):
        '''
        # this initatializes a Lambert_object_button object for each object
            with a default lambert
        '''
        for obj in self.lambert_objs:
            pm.setParent(self.buttons_layout)
            button = Lambert_object_button(obj)
            
        pm.setParent(self.layout)
        pm.button(label= 'Select All', command= pm.Callback(self.select_all),
                  height= 50)
        
    def select_all(self):
        pm.select(self.lambert_objs)
                
def gui():
    '''
    # gui for the script
    '''
    win = 'shader_grading'
    if(pm.window(win, ex = True)):
        pm.deleteUI(win)
        
    if(pm.windowPref(win, ex = True)):
        pm.windowPref(win, remove = True)
    
    my_win = pm.window(win, title= 'shader_grading', width= 550,
                       height= 250)
    main = pm.columnLayout()
    
    grader = Shader_sorter()
    
    pm.setParent(main)
    
    pm.text(label= 'Objects With Default Lambert', align= 'center',
            height= 50, backgroundColor= [1,0,0], width= 550)
    
    pm.scrollLayout(width= 560, height= 300)
    
    lambert_objs = Lambert_objects_checker()
    
    my_win.show()