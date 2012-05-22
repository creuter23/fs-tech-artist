'''

Author:
    Firmin Saint-Amour
    
Description:
    pass
    
How To Run:
    pass

'''

import os
import pymel.core as pm
import maya.cmds as cmds



class Bound_Geo(object):
    '''
    # 
    '''
    def __init__(self, rigid_body):
        self.rigid_body = rigid_body
        
    def create_system(self):
        self.duplicate_rigid_body()
        self.create_joint()
        self.position_joint()
        self.bind_geo()
        self.constrain_joint_to_rigid_body()
        
    def duplicate_rigid_body(self):
        self.bound_geo = pm.duplicate(self.rigid_body,
                                      name= '%s_rb' % (self.rigid_body))[0]
        shape_nodes = self.bound_geo.getShapes()
        for shape_node in shape_nodes:
                if 'rigidBody' in '%s' % (shape_node):
                    pm.delete(shape_node)
    
    def create_joint(self):
        pm.select(clear= True)
        self.joint = pm.joint(name= '%s_bake' % (self.rigid_body))
        
    def position_joint(self):
        temp_parent_constraint = pm.parentConstraint(self.bound_geo, self.joint,
                            maintainOffset= False)
        pm.delete(temp_parent_constraint)
        
    def bind_geo(self):
        pm.select(clear= True)
        pm.skinCluster(self.joint, self.bound_geo)
        
    def constrain_joint_to_rigid_body(self):
        self.parent_constraint = pm.parentConstraint(self.rigid_body,
                                    self.joint, maintainOffset= False)
        
    def delete_rigid_body_to_joint_constraint(self):
        pm.delete(self.parent_constraint)
        
    def get_joint(self):
        return self.joint
    
    def get_bound_geo(self):
        return self.bound_geo
    
    def kill(self):
        del self

class Rigid_Body_Manager(object):
    '''
    # 
    '''
    def __init__(self, rigid_body_objects, root_joint= True, start= 1, end= 100,
                    name= 'rigid_bodies', export= True, delete= True,
                    visibility= True):
        '''
        # 
        '''
        self.bound_geo_instances = []
        self.rigid_body_objects = rigid_body_objects
        self.root_joint = root_joint
        self.name = name
        self.export = export
        self.delete = delete
        self.visibility = visibility
        self.start_frame = start
        self.end_frame = end
     
    def create_system(self):
        self.create_bound_geo_instances()
        self.create_root_joint()
        self.group_system()
        self.bake_simulation_to_joints()
    
    
    
    def create_bound_geo_instances(self):
        for rigid_body in self.rigid_body_objects:
            bound_geo_instance = Bound_Geo('%s' % (rigid_body))
            bound_geo_instance.create_system()
            self.bound_geo_instances.append(bound_geo_instance)
       
    def delete_rigid_body_to_joint_constraint(self):
        for bound_geo in self.bound_geo_instances:
                bound_geo.delete_rigid_body_to_joint_constraint()
                
        
            
    def create_root_joint(self):
        if self.root_joint == True:
            pm.select(clear= True)
            self.world = pm.joint(name= '%s_master' % (self.name))
            
            self.parent_joints_to_root()
            
        if self.root_joint == False:
            pass
    
    def parent_joints_to_root(self):
        for bound_geo in self.bound_geo_instances:
            joint = bound_geo.get_joint()
            pm.parent('%s' % (joint), self.world)
    
    def group_system(self):
        geo_group = self.group_bound_geo()
        joints_group = self.group_joints()
        self.main_group = pm.group(geo_group, joints_group,
                                   name= '%s' % (self.name))
    
    def group_bound_geo(self):
        bound_objects = []
        for bound_geo in self.bound_geo_instances:
            geo = bound_geo.get_bound_geo()
            bound_objects.append(geo)
            
        group = pm.group(bound_objects, name= '%s_geo' % (self.name))
        return group
  
    
    def group_joints(self):
        if self.root_joint == True:
            group = pm.group(self.world, name= '%s_joints' % (self.name))
            return group
            
        if self.root_joint == False:
            joints = []
            for bound_geo in self.bound_geo_instances:
                joint = bound_geo.get_joint()
                joints.append('%s' % (joint))
                
            group = pm.group(joints, name= '%s_joints' % (self.name))
            return group
        
        
    def bake_simulation_to_joints(self):
        joints = []
        for bound_geo in self.bound_geo_instances:
            joint = bound_geo.get_joint()
            joints.append('%s' % (joint))
        
        pm.bakeResults(joints, simulation= True,
                time= (self.start_frame, self.end_frame), sampleBy= 1,
                disableImplicitControl= True, preserveOutsideKeys= True,
               sparseAnimCurveBake= False, removeBakedAttributeFromLayer= False,
               bakeOnOverrideLayer= False, controlPoints= False, shape= True)
        
        self.delete_rigid_body_to_joint_constraint()
        self.visibility_state()
        self.export_to_ma()
        self.delete_system()
    
    def visibility_state(self):
        if self.visibility == True:
            pass
        
        if self.visibility == False:
            pm.setAttr('%s.visibility' % (self.main_group), 0)
    
    def export_to_ma(self):
        
        if self.export == True:
            pm.select(clear= True)
            pm.select(self.main_group)
            current_scene = pm.sceneName()
            dir_name = os.path.dirname(current_scene)
            new_scene_name = os.path.join(dir_name, self.name)
            try:
                pm.exportSelected(new_scene_name, force= True, channels= True,
                              type=  'mayaAscii')
            except:
                pm.exportSelected(new_scene_name, force= True, channels= True,
                              type=  'mayaBinary')

            
        if self.export == False:
            pass
    
    def delete_system(self):
        if self.delete == True:
            pm.delete(self.main_group)
            self.kill()
        
        if self.delete == False:
            self.kill()
    
    def kill(self):
        for bound_geo in self.bound_geo_instances:
            bound_geo.kill()
        del self
        
        
class Options_UI(object):
    '''
    self, rigid_body_objects, root_joint= True, start= 1, end= 100,
                    name= 'rigid_bodies', export= True, delete= True,
                    visibility= True):
        
    '''
    def __init__(self, rigid_body_objects, name):
        self.rigid_body_objects = rigid_body_objects
        self.name = name
        
    def create_ui(self):
        self.layout = pm.columnLayout(adjustableColumn= True)
        self.root_joint = pm.checkBox(label='Create Root Joint')
        self.export = pm.checkBox(label='Export When Finished')
        self.delete = pm.checkBox(label='Delete When Finished')
        self.visibility = pm.checkBox(label='Visibility State', value= 1)
        self.start_end_fields = pm.intFieldGrp( numberOfFields=2,
                        label=u'Start & End Frames', value1=0, value2=100,
                        columnWidth3= [105,90,90])
        pm.text(label= '')
        pm.button(label= 'Bake Simulation', height= 190,
                            command= pm.Callback(self.bake_simulation))
        
        return self.layout
        
    def bake_simulation(self):
        start = self.start_end_fields.getValue1()
        end = self.start_end_fields.getValue2()
        root_joint = self.root_joint.getValue()
        export = self.export.getValue()
        delete = self.delete.getValue()
        visibility = self.visibility.getValue()
        
        manager = Rigid_Body_Manager(rigid_body_objects= self.rigid_body_objects,
                        root_joint= root_joint, start= start, end= end,
                        export= export, delete= delete, visibility= visibility,
                        name= self.name)
        
        manager.create_system()
        self.delete_ui()
        
    def delete_ui(self):
        pm.deleteUI(self.layout)
        self.kill()
        
    def kill(self):
        del self
        
def gui():
    win = 'rigid_body_win'
    if pm.window(win, exists= True):
        pm.deleteUI(win)
        
    if pm.windowPref(win, exists= True):
        pm.windowPref(win, remove= True)
    
    global obj_scroll_list, name_field, tab_layout
    
    my_win = pm.window(win, title= 'BAKE', toolbox= True, width= 300)
    tab_layout = pm.tabLayout()
    
    ui_creator = pm.columnLayout(adjustableColumn= False)
    name_field = pm.textFieldGrp(label = 'System Name', text= 'Name',
                                 columnWidth2= [145, 150])
    obj_scroll_list = pm.textScrollList(width= 300, height= 200,
                                    allowMultiSelection= True)
    pm.rowColumnLayout(nc=3, columnWidth= ([1,100], [2,100], [1,100]))
    pm.button(label= 'Load', command= pm.Callback(load_objects), width= 100)
    pm.button(label= '+', command= pm.Callback(add_objects), width= 100)
    pm.button(label= '-', command= pm.Callback(remove_objects), width= 100)
    
    pm.setParent('..')
    pm.button(label= 'Create Baking System', height= 50, width= 300,
              command= pm.Callback(create_baking_system))
    
    pm.tabLayout( tab_layout, edit=True, tabLabel=((ui_creator, 'Setup')))
    
    my_win.show()
        
        
def load_objects():
    '''
    # loads the selected objects in the text scroll list
    # also clears out the text scroll list
    '''
    obj_scroll_list.removeAll()
    objs = pm.ls(selection= True)
    for obj in objs:
        obj_scroll_list.append(obj)
        
        
        
def add_objects():
    '''
    # adds the selected objects in the text scroll list
    '''
    objs = pm.ls(selection= True)
    for obj in objs:
        obj_scroll_list.append(obj)
        
    
def remove_objects():
    '''
    # removes the selected objects in the text scroll list
    '''
    objs = obj_scroll_list.getSelectItem()
    for obj in objs:
        obj_scroll_list.removeItem(obj)
        
        
        
def create_baking_system():
    pm.setParent(tab_layout)
    rigid_body_objects = obj_scroll_list.getAllItems()
    
    
    name = name_field.getText()
    
    ui = Options_UI(rigid_body_objects, name)
    
    layout = ui.create_ui()
    
    pm.tabLayout( tab_layout, edit=True, tabLabel=((layout, '%s' % (name))))
        
        
        