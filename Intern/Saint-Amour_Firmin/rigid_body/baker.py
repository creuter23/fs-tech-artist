'''

Author:
    Firmin Saint-Amour
    
Description:
    tool to bake rigid body simulations to joints
    in order to make them exportable to an engine
    
How To Run:
    import baker
    baker.gui()

'''

import os
import pymel.core as pm
import maya.cmds as cmds

class Vertex_Checker(object):
    
    def __init__(self, joint, mesh, tollerance):
        self.positions = []
        self.joint = joint
        self.mesh = mesh
        self.tollerance = tollerance
        self.vertex_objects = []
        self.create_vertex_objects()
        self.get_vertex_positions()
        print tollerance
        
    def create_vertex_objects(self):
        vertex_number = pm.polyEvaluate(self.mesh, vertex= 1)
        i = 0
        while i != vertex_number:
            temp_vert_obj = pm.MeshVertex(u'%s.vtx[%i]' % (self.mesh, i))
            
            self.vertex_objects.append(temp_vert_obj)
            #print temp_vert_obj
            
            i += 1
            
    def get_vertex_positions(self):
        for vert in self.vertex_objects:
            vert_position = vert.getPosition(space= 'world')
            #print vert_position
            ouput = [vert_position[0], vert_position[1], vert_position[2]]
            self.positions.append(ouput)
    
    
    def paint_weights(self, position, skin_cluster, mesh):
        output = []
        #print position
        x = 0
        while x < len(position):
            i = 0
            while i < len(self.positions):
                temp_position = self.positions[i]
                max_pos = [temp_position[0]+ self.tollerance,
                           temp_position[1]+ self.tollerance,
                           temp_position[2]+ self.tollerance]
                
                min_pos = [temp_position[0]- self.tollerance,
                           temp_position[1]- self.tollerance,
                           temp_position[2]- self.tollerance]
                
                if (position[x] >= min_pos) and (position[x] <= max_pos): 
                   #print position[x]
                   pm.skinPercent( skin_cluster, '%s.vtx[%s]'
                                % (mesh,x), transformValue=[self.joint, 1])
                   output.append(position[x])
                   #self.positions.remove(temp_position)
                   print 'match', position[x]
                i += 1
            x += 1
        
        return output

class Bound_Geo(object):
    '''
    # class to create a bound object and joint
    # takes a rigidBody object
    '''
    def __init__(self, rigid_body, bind= True):
        self.rigid_body = rigid_body # rigid body objects
        self.bind = bind
        
    def create_system(self):
        '''
        # creates the system
        '''
        self.duplicate_rigid_body()
        self.create_joint()
        self.position_joint()
        if self.bind == True:
            self.bind_geo()
        self.constrain_joint_to_rigid_body()
        
    def duplicate_rigid_body(self):
        '''
        # duplicates the rigid body object, and names with _rb
        '''
        self.bound_geo = pm.duplicate(self.rigid_body,
                                      name= '%s_rb' % (self.rigid_body))[0]
        shape_nodes = self.bound_geo.getShapes()
        # deleting the rigid body shape on the duplicated object
        for shape_node in shape_nodes:
                if 'rigidBody' in '%s' % (shape_node):
                    pm.delete(shape_node)
    
    def create_joint(self):
        '''
        creates the joint
        '''
        pm.select(clear= True)
        self.joint = pm.joint(name= '%s_bake' % (self.rigid_body))
        
    def position_joint(self):
        '''
        # positions the joint
        '''
        temp_parent_constraint = pm.parentConstraint(self.bound_geo, self.joint,
                            maintainOffset= False)
        pm.delete(temp_parent_constraint)
        
    def bind_geo(self):
        '''
        # binds the duplicated geo to the joint
        '''
        #pm.select(clear= True)
        pm.skinCluster(self.joint, self.bound_geo)
        
    def constrain_joint_to_rigid_body(self):
        '''
        # constraint the joint to the original rigid body object
        '''
        self.parent_constraint = pm.parentConstraint(self.rigid_body,
                                    self.joint, maintainOffset= False)
        
    def delete_rigid_body_to_joint_constraint(self):
        '''
        # deletes the rigid body object's constraint
        '''
        pm.delete(self.parent_constraint)
        
    def get_joint(self):
        '''
        # returns the joint
        '''
        return self.joint
    
    def get_bound_geo(self):
        '''
        # returns the duplicated objects
        '''
        return self.bound_geo
    
    def kill(self):
        '''
        # deletes the objects
        '''
        del self

class Rigid_Body_Manager(object):
    '''
    # this call will manage the instances of the Bound_geo class
    # it will bake the simulations
    '''
    def __init__(self, rigid_body_objects, root_joint= True, start= 1, end= 100,
                    name= 'rigid_bodies', export= True, delete= True,
                    visibility= True, group= True):
        self.bound_geo_instances = []
        self.rigid_body_objects = rigid_body_objects # rigid body objects
        self.root_joint = root_joint # bool value for root_joint
        self.name = name # name of the system
        self.export = export # bool value for export
        self.delete = delete # bool value for delete
        self.visibility = visibility # bool value for visibility
        self.start_frame = start # strart frame for bake
        self.end_frame = end # end frame for bake
        self.group = group # bool value for grouping
     
    def create_system(self):
        '''
        # this creates the system
        '''
        self.create_bound_geo_instances()
        self.create_root_joint()
        if self.group == True:
            self.group_system()
        self.bake_simulation_to_joints()
    
    def create_bound_geo_instances(self):
        '''
        # this creates a Bound_geo instances for each of the given rigid body
            objects
        '''
        for rigid_body in self.rigid_body_objects:
            bound_geo_instance = Bound_Geo('%s' % (rigid_body))
            bound_geo_instance.create_system()
            self.bound_geo_instances.append(bound_geo_instance)
       
    def delete_rigid_body_to_joint_constraint(self):
        '''
        # this will delete the constraint on the joints
        # it invokes the 'delete_rigid_body_to_joint_constraint' method
            for each Bound_geo instance
        '''
        for bound_geo in self.bound_geo_instances:
                bound_geo.delete_rigid_body_to_joint_constraint()
                
    def create_root_joint(self):
        '''
        # this creates a joint at [0,0,0]
        '''
        if self.root_joint == True:
            pm.select(clear= True)
            self.world = pm.joint(name= '%s_master' % (self.name))
            
            self.parent_joints_to_root()
            
        if self.root_joint == False:
            pass
    
    def parent_joints_to_root(self):
        '''
        # this will parent all the joints to the root_joint
        '''
        for bound_geo in self.bound_geo_instances:
            joint = bound_geo.get_joint()
            pm.parent('%s' % (joint), self.world)
    
    def group_system(self):
        '''
        # this creates a master group for the system
        '''
        geo_group = self.group_bound_geo()
        joints_group = self.group_joints()
        self.main_group = pm.group(geo_group, joints_group,
                                   name= '%s' % (self.name))
    
    def group_bound_geo(self):
        '''
        # this groups all the bound geometry
        # returns that group
        '''
        bound_objects = []
        for bound_geo in self.bound_geo_instances:
            geo = bound_geo.get_bound_geo()
            bound_objects.append(geo)
            
        group = pm.group(bound_objects, name= '%s_geo' % (self.name))
        return group
    
    def group_joints(self):
        '''
        # this groups all the joints
        # returns that group
        '''
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
        '''
        # this bakes the simulation to the joints
        '''
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
        '''
        # this will hide the final group if True
        '''
        if self.visibility == True:
            pass
        
        if self.visibility == False:
            try:
                pm.setAttr('%s.visibility' % (self.main_group), 0)
            
            except:
                pass
    
    def export_to_ma(self):
        '''
        # this exports to a new ma file if True
        '''
        if self.export == True:
            if self.group== True:
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
            if self.group == False:
                joints = []
                geometry = []
                for bound_geo in self.bound_geo_instances:
                    joint = bound_geo.get_joint()
                    joints.append('%s' % (joint))
                    
                for bound_geo in self.bound_geo_instances:
                    geo = bound_geo.get_bound_geo()
                    geometry.append(geo)
                    
                pm.select(clear= True)
                pm.select(joints, geometry)
                current_scene = pm.sceneName()
                dir_name = os.path.dirname(current_scene)
                new_scene_name = os.path.join(dir_name, self.name)
                try:
                    pm.exportSelected(new_scene_name, force= True, channels= True,
                                  type=  'mayaAscii')
                except:
                    pm.exportSelected(new_scene_name, force= True, channels= True,
                                  type=  'mayaBinary')

    def delete_system(self):
        '''
        # this deletes the system if true
        '''
        if self.delete == True:
            if self.group == True:
                pm.delete(self.main_group)
                self.kill()
            if self.group == False:
                joints = []
                geometry = []
                for bound_geo in self.bound_geo_instances:
                    joint = bound_geo.get_joint()
                    joints.append('%s' % (joint))
                    
                for bound_geo in self.bound_geo_instances:
                    geo = bound_geo.get_bound_geo()
                    geometry.append(geo)
                    
                pm.delete(joints, geometry)
                self.kill()
            if self.root_joint == True:
                try:
                    pm.delete(self.world)
                    self.kill()
                except:
                    pass
        
    
    def kill(self):
        '''
        # this deletes the object
        '''
        for bound_geo in self.bound_geo_instances:
            bound_geo.kill()
        del self
              
class Combined_Manager(Rigid_Body_Manager):
    def __init__(self, rigid_body_objects, root_joint= True, start= 1, end= 100,
                    name= 'rigid_bodies', export= True, delete= True,
                    visibility= True, group= True, tollerance= .05):
        self.bound_geo_instances = []
        self.rigid_body_objects = rigid_body_objects # rigid body objects
        self.root_joint = root_joint # bool value for root_joint
        self.name = name # name of the system
        self.export = export # bool value for export
        self.delete = delete # bool value for delete
        self.visibility = visibility # bool value for visibility
        self.start_frame = start # strart frame for bake
        self.end_frame = end # end frame for bake
        self.group = group # bool value for grouping
        self.tollerance = tollerance
        self.vertex_objects = []
        self.vertex_checkers = []
        self.vertex_positions = []
    def create_system(self):
        '''
        # this creates the system
        '''
        self.create_bound_geo_instances()
        self.create_vertex_checkers()
        self.combine_meshes()
        self.create_vertex_objects()
        self.get_vertex_positions()
        self.bind_geo()
        self.paint_weights()
        print 'geo bound'
        self.create_root_joint()
        
        if self.group == True:
            self.group_system()
        self.bake_simulation_to_joints()
        
    def create_vertex_checkers(self):
        for bound_geo in self.bound_geo_instances:
            geo = bound_geo.get_bound_geo()
            joint = bound_geo.get_joint()
            vertex_checker = Vertex_Checker(joint, geo, self.tollerance)
            #print vertex_checker
            self.vertex_checkers.append(vertex_checker)
    
    def create_bound_geo_instances(self):
        '''
        # this creates a Bound_geo instances for each of the given rigid body
            objects
        '''
        for rigid_body in self.rigid_body_objects:
            bound_geo_instance = Bound_Geo('%s' % (rigid_body), bind= False)
            bound_geo_instance.create_system()
            self.bound_geo_instances.append(bound_geo_instance)
            
    def combine_meshes(self):
        bound_objects = []
        for bound_geo in self.bound_geo_instances:
            geo = bound_geo.get_bound_geo()
            bound_objects.append(geo)
            
        self.combined_object = pm.polyUnite(bound_objects,
                        name= '%s_mesh' % (self.name), ch= False)[0]
        
        return self.combined_object
    
    def create_vertex_objects(self):
        vertex_number = pm.polyEvaluate(self.combined_object, vertex= 1)
        i = 0
        while i != vertex_number:
            temp_vert_obj = pm.MeshVertex(u'%s.vtx[%i]' %
                                          (self.combined_object, i))
            
            self.vertex_objects.append(temp_vert_obj)
            #print temp_vert_obj
            
            i += 1
            
    def get_vertex_positions(self):
        for vert in self.vertex_objects:
            vert_position = vert.getPosition(space= 'world')
            #print vert_position
            ouput = [vert_position[0], vert_position[1], vert_position[2]]
            self.vertex_positions.append(ouput)
    
    def bind_geo(self):
        joints = []
        pm.select(clear= True)
        for bound_geo in self.bound_geo_instances:
            joint = bound_geo.get_joint()
            joints.append(joint)
        self.skin_cluster = pm.skinCluster(joints, self.combined_object,
                    skinMethod= 0, dropoffRate= 1, normalizeWeights= 1)
        
        #self.paint_weights()
    
    def paint_weights(self):
        print 'painting weights', self.skin_cluster
        #print self.skin_cluster
        #print self.vertex_checkers
        for vert_checker in self.vertex_checkers:
            #print vert_checker
            output = vert_checker.paint_weights(self.vertex_positions,
                                self.skin_cluster, self.combined_object)
            print 'painting weights ..........................'
            '''
            for o in output:
                try:
                    self.vertex_positions.remove(o)
                    print 'removed ', o
                except:
                    print 'could not remove ', o
            '''
                
            
            
    '''            
    def check_verts(self, vert):
        for vert_checker in self.vertex_checkers:
            print vert
            value = vert_checker.check(vert)
            if value == True:
                print value
                return value
                break
            else:
                continue
    '''
    
    def group_bound_geo(self):
        '''
        # this groups all the bound geometry
        # returns that group
        '''
            
        group = pm.group(self.combined_object, name= '%s_geo' % (self.name))
        return group
    
    def bake_simulation_to_joints(self):
        '''
        # this bakes the simulation to the joints
        '''
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
        
    def delete_system(self):
        '''
        # this deletes the system if true
        '''
        if self.delete == True:
            if self.group == True:
                pm.delete(self.main_group)
                self.kill()
            if self.group == False:
                joints = []
                #geometry = []
                for bound_geo in self.bound_geo_instances:
                    joint = bound_geo.get_joint()
                    joints.append('%s' % (joint))
                    
                
                pm.delete(joints, self.combined_object)
                self.kill()
            if self.root_joint == True:
                try:
                    pm.delete(self.world)
                    self.kill()
                except:
                    pass    
        
    def export_to_ma(self):
        '''
        # this exports to a new ma file if True
        '''
        if self.export == True:
            if self.group== True:
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
            if self.group == False:
                joints = []
                #geometry = []
                for bound_geo in self.bound_geo_instances:
                    joint = bound_geo.get_joint()
                    joints.append('%s' % (joint))
                    
                    
                pm.select(clear= True)
                pm.select(joints, self.combined_object)
                current_scene = pm.sceneName()
                dir_name = os.path.dirname(current_scene)
                new_scene_name = os.path.join(dir_name, self.name)
                try:
                    pm.exportSelected(new_scene_name, force= True, channels= True,
                                  type=  'mayaAscii')
                except:
                    pm.exportSelected(new_scene_name, force= True, channels= True,
                                  type=  'mayaBinary')

class Options_UI(object):
    '''
    # this creates a ui which contains options for the manager class
    # takes a list of rigid body objects and the name for the system
    '''
    def __init__(self, rigid_body_objects, name):
        self.rigid_body_objects = rigid_body_objects # rigid bpdy objects
        self.name = name # the name for the system
        
    def create_ui(self):
        '''
        # this creates the ui
        # returns the layout for the gui components
        '''
        self.layout = pm.columnLayout(adjustableColumn= True)
        self.root_joint = pm.checkBox(label='Create Root Joint')
        self.export = pm.checkBox(label='Export When Finished')
        self.delete = pm.checkBox(label='Delete When Finished')
        self.visibility = pm.checkBox(label='Visibility State', value= 1)
        self.group = pm.checkBox(label='Group System', value= 1)
        self.combine = pm.checkBox(label='Combine Meshes', value= 0,
                            changeCommand= pm.Callback(self.enable_tollerance))
        self.tollerance = pm.floatSliderGrp(label= 'Tollerance',
                        value= .000000000, field= True, maxValue= 10,
                        minValue= -10, step= .000000005,
                                        columnWidth3= [90, 90, 105])
        self.tollerance.setEnable(False)
        self.start_end_fields = pm.intFieldGrp( numberOfFields=2,
                        label=u'Start & End Frames', value1=0, value2=100,
                        columnWidth3= [105,90,90])
        pm.text(label= '')
        pm.button(label= 'Bake Simulation', height= 130,
                            command= pm.Callback(self.bake_simulation))
        
        return self.layout
        
    def enable_tollerance(self):
        if self.combine.getValue() == 1:
            self.tollerance.setEnable(True)
            
        else:
            self.tollerance.setEnable(False)
    
    def bake_simulation(self):
        '''
        # this creates an instances of the manager class
        # and ivokes it's create method
        '''
        start = self.start_end_fields.getValue1()
        end = self.start_end_fields.getValue2()
        root_joint = self.root_joint.getValue()
        export = self.export.getValue()
        delete = self.delete.getValue()
        visibility = self.visibility.getValue()
        group = self.group.getValue()
        combine = self.combine.getValue()
        tollerance = self.tollerance.getValue()
        
        if combine == 1:
            manager = Combined_Manager(rigid_body_objects= self.rigid_body_objects,
                        root_joint= root_joint, start= start, end= end,
                        export= export, delete= delete, visibility= visibility,
                        name= self.name, group= group, tollerance= tollerance)
        else:
            manager = Rigid_Body_Manager(rigid_body_objects= self.rigid_body_objects,
                            root_joint= root_joint, start= start, end= end,
                            export= export, delete= delete, visibility= visibility,
                            name= self.name, group= group)
        
        manager.create_system()
        self.delete_ui()
        
    def delete_ui(self):
        '''
        # this deletes the layout with all the components
        '''
        pm.deleteUI(self.layout)
        self.kill()
        
    def kill(self):
        '''
        # this deletes the object
        '''
        del self
        
def gui():
    '''
    # gui for the script
    '''
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
    '''
    # this creates an Options_ui instances and appends to the tab_layout
    '''
    pm.setParent(tab_layout)
    rigid_body_objects = obj_scroll_list.getAllItems()
    
    
    name = name_field.getText()
    
    ui = Options_UI(rigid_body_objects, name)
    
    layout = ui.create_ui()
    
    pm.tabLayout( tab_layout, edit=True, tabLabel=((layout, '%s' % (name)))) 