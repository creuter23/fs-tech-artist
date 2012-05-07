



import pymel.core as pm

class Shader_sorter(object):
    
    def __init__(self):
        self.node_list = pm.ls(type=('ramp', 'place3dTexture',
            'place2dTexture', 'layeredTexture', 'bump3d', 'bump2d', 'granite',
            'noise', 'stucco', 'marble', 'checker','cloth', 'fractal', 'grid',
            'leather', 'crater', 'cloud', 'brownian', 'wood'))
        
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
        
        pm.setParent(self.layout)
        pm.columnLayout()
        pm.text(label='Node Info')
        self.info_field = pm.scrollField(wordWrap= True, width= 250, height= 200)
        
        
        self.update_shader_list()
             
    def update_shader_list(self):
        self.node_list = pm.ls(type=('ramp', 'place3dTexture',
            'place2dTexture', 'layeredTexture', 'bump3d', 'bump2d', 'granite',
            'noise', 'stucco', 'marble', 'checker','cloth', 'fractal', 'grid',
            'leather', 'crater', 'cloud', 'brownian', 'wood'))
        
        self.mat_list = pm.ls(mat= True)
        
        self.shader_list.removeAll()
        for mat in self.mat_list:
            self.shader_list.append('%s' % (mat))
            
    def update_connections_list(self):
        mat = self.shader_list.getSelectItem()[0]
        
        shader_connections = pm.listConnections('%s' %(mat))    
        
        node_connections = []
        
        
        
        for x in shader_connections:
            
            if x not in self.node_list:
                continue           
    
            node_connections.append(x)
            
            temp_list01 = pm.listConnections('%s' %(x))
            
            for x in temp_list01:
                
                if x in node_connections or x in self.mat_list:
                    continue
                
                if x not in self.node_list:
                    continue
                
                
                node_connections.append(x)
                
                temp_list02 = pm.listConnections('%s' % (x))
                
                for x in temp_list02:
                    if x in node_connections or x in self.mat_list:
                        continue
                
                    if x not in self.node_list:
                        continue
                
                
                    node_connections.append(x)
                    
                    temp_list03 = pm.listConnections('%s' % (x))
                    
                    for x in temp_list03:
                        if x in node_connections or x in self.mat_list:
                            continue
                
                        if x not in self.node_list:
                            continue
                
                
                        node_connections.append(x)
                    
        print node_connections
        
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
        
        output = ['Type: %s' % (ramp_type[type_value]),
                  'Interpolation: %s' % (interp_type[interp_value])]
        
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
            
        
        
            
    def write_info(self):
        
        self.info_field.setText('')
        
        node = self.connections_list.getSelectItem()[0]
        
        node_type = pm.nodeType(node)
        print node_type
        
        
                
        if node_type == 'ramp':
            result = self.get_ramp_attrs(node)
            for r in result:
                self.info_field.insertText('%s\n' % (r) )
                
        if node_type == 'noise':
            result = self.get_noise_attrs(node)
            for r in result:
                self.info_field.insertText('%s\n' % (r) )
                
        if node_type != 'ramp' or node_type != 'noise':
            attrs = pm.listAttr('%s' % (node), write= True, settable= True,
                                keyable= True)
            for attr in attrs:
                try:
                    value = pm.getAttr('%s.%s' % (node, attr))
                    self.info_field.insertText('%s: %s\n' % (attr, value))
                except:
                    pass
                
    
                
            
                
            
      

    
def gui():
    win = 'shader_grading'
    if(pm.window(win, ex = True)):
        pm.deleteUI(win)
        
    if(pm.windowPref(win, ex = True)):
        pm.windowPref(win, remove = True)
    
    my_win = pm.window(win, title= 'shader_grading', width= 550,
                       height= 250)
    
    grader = Shader_sorter()
    
    my_win.show()