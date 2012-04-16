


import pymel.core as pm

import gui_components as gc
reload(gc)

class Node_UI():
    '''
    # creates uis for the selected node
    # takes the node as a string arg
    # retuns none
    '''
    def __init__(self, node):
        
        self.node = node # the polymove UV node
        
        self.layout = pm.frameLayout(label= '%s' % (self.node),  width= 340, collapsable= True)
        pm.button(label= 'Delete UI', command= pm.Callback(self.delete_ui))

    def delete_ui(self):
        pm.deleteUI(self.layout)
    
    def insert_key(self, attr, value):
        print attr, value.getValue(), attr, value.getValue()
        
        pm.setKeyframe('%s' % (attr), time= int(value.getValue()) )
        
        # reinvoking the create to add the uis for the new keys
        print 'recreating'
        pm.deleteUI(self.temp_layout)
        self.create()
        
    def create(self):
        print self.node
        
        # getting the amount of keys for each attr
        self.count_TU = pm.keyframe( '%s.translateU' % (self.node) , query=True,
                                    keyframeCount=True ) # translate U
        
        self.count_TV = pm.keyframe( '%s.translateV' % (self.node) , query=True,
                                    keyframeCount=True ) # translate V
        
        self.count_PU = pm.keyframe( '%s.pivotU' % (self.node) , query=True,
                                    keyframeCount=True ) # pivot U
        
        self.count_PV = pm.keyframe( '%s.pivotV' % (self.node) , query=True,
                                    keyframeCount=True ) # pivot V
        
        self.count_SU = pm.keyframe( '%s.scaleU' % (self.node) , query=True,
                                    keyframeCount=True ) # scale U
        
        self.count_SV = pm.keyframe( '%s.scaleV' % (self.node) , query=True,
                                    keyframeCount=True ) # scale V
        
        self.count_R = pm.keyframe( '%s.random' % (self.node) , query=True,
                                   keyframeCount=True ) # random
        
        self.count_RA = pm.keyframe( '%s.rotationAngle' % (self.node) , query=True,
                                    keyframeCount=True ) # rotation Angle
        
        
        #pm.frameLayout(label= '%s' % (self.node), width= 340)
        pm.setParent(self.layout)
        self.temp_layout = pm.columnLayout(adjustableColumn= False, width= 340)
        
        if self.count_TU >= 1:
            pm.setParent(self.temp_layout)
            TU = Anim_UI(node= '%s_translateU' % (self.node), count = self.count_TU)
            TU.create()
            pm.setParent('..')
            pm.text(label= 'Insert Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Position')
            my_field = pm.intField()
            pm.button(label= 'Insert', command= pm.Callback(self.insert_key,
               attr= '%s.translateU' % (self.node), value= my_field))
            
        if self.count_TV >= 1:
            pm.setParent(self.temp_layout)
            TV = Anim_UI(node= '%s_translateV' % (self.node), count = self.count_TV)
            TV.create()
            pm.setParent('..')
            pm.text(label= 'Insert Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Position')
            my_field = pm.intField()
            pm.button(label= 'Insert', command= pm.Callback(self.insert_key,
               attr= '%s.translateU' % (self.node), value= my_field))
            
        if self.count_RA >= 1:
            pm.setParent(self.temp_layout)
            RA = Anim_UI(node= '%s_rotationAngle' % (self.node), count = self.count_RA)
            RA.create()
            pm.setParent('..')
            pm.text(label= 'Insert Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Position')
            my_field = pm.intField()
            pm.button(label= 'Insert', command= pm.Callback(self.insert_key,
               attr= '%s.translateU' % (self.node), value= my_field))
            
        if self.count_PU >= 1:
            pm.setParent(self.temp_layout)
            PU = Anim_UI(node= '%s_pivotU' % (self.node), count = self.count_PU)
            PU.create()
            pm.setParent('..')
            pm.text(label= 'Insert Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Position')
            my_field = pm.intField()
            pm.button(label= 'Insert', command= pm.Callback(self.insert_key,
               attr= '%s.translateU' % (self.node), value= my_field))
            
        if self.count_PV >= 1:
            pm.setParent(self.temp_layout)
            PV = Anim_UI(node= '%s_pivotV' % (self.node), count = self.count_PV)
            PV.create()
            pm.setParent('..')
            pm.text(label= 'Insert Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Position')
            my_field = pm.intField()
            pm.button(label= 'Insert', command= pm.Callback(self.insert_key,
               attr= '%s.translateU' % (self.node), value= my_field))
            
        if self.count_SU >= 1:
            pm.setParent(self.temp_layout)
            SU = Anim_UI(node= '%s_scaleU' % (self.node), count = self.count_SU)
            SU.create()
            pm.setParent('..')
            pm.text(label= 'Insert Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Position')
            my_field = pm.intField()
            pm.button(label= 'Insert', command= pm.Callback(self.insert_key,
               attr= '%s.translateU' % (self.node), value= my_field))
            
        if self.count_SV >= 1:
            pm.setParent(self.temp_layout)
            SV = Anim_UI(node= '%s_scaleV' % (self.node), count = self.count_SV)
            SV.create()
            pm.setParent('..')
            pm.text(label= 'Insert Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Position')
            my_field = pm.intField()
            pm.button(label= 'Insert', command= pm.Callback(self.insert_key,
               attr= '%s.translateU' % (self.node), value= my_field))
            
        if self.count_R >= 1:
            pm.setParent(self.temp_layout)
            random = Anim_UI(node= '%s_random' % (self.node), count = self.count_R)
            random.create()
            pm.setParent('..')
            pm.text(label= 'Insert Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Position')
            my_field = pm.intField()
            pm.button(label= 'Insert', command= pm.Callback(self.insert_key,
               attr= '%s.translateU' % (self.node), value= my_field))
            
            
        
        
        
     
class Anim_UI():
    def __init__(self, node, count):
        self.node = node
        self.count = count
    
    def create(self):
        self.layout = pm.frameLayout(label= str(self.node), width= 340, collapsable= True )
        pm.attrEnumOptionMenu( label='Pre Infinity ', attribute='%s.preInfinity' % (self.node) )
        pm.attrEnumOptionMenu( label='Post Infinity ', attribute='%s.postInfinity' % (self.node) )

        pm.rowColumnLayout(numberOfColumns= 5, columnWidth= ([1, 10], [2, 50], [3, 50], [4, 115], [5, 115]))
        pm.text(label= '')
        pm.text(label= 'Time')
        pm.text(label= 'Value')
        pm.text(label= 'inTan Type')
        pm.text(label= 'OutTan Type')
        
        for num in xrange(self.count):
            pm.text(label= str(num))
            
            time = gc.Time_int(index= num, node= self.node)
            time.create()
            
            value = gc.Value_int(index= num, node= self.node)
            value.create()
            
            in_tan = gc.In_Tangent(index= num, node= self.node)
            in_tan.create()
            
            out_tan = gc.Out_Tangent(index= num, node= self.node)
            out_tan.create()
        
    
    
    

def gui():
    '''
    creates the gui for the tool
    '''
    win = 'uvtools'
    if(pm.window(win, ex = True)):
        pm.deleteUI(win)
        
    if(pm.windowPref(win, ex = True)):
        pm.windowPref(win, remove = True)
        
        
    global scroll_list, dyn_uis
        
    myWin = pm.window(win, title='Anim UV Tool' , sizeable = True, mnb = True, width = 500, height = 400, backgroundColor= [.68,.68,.68])
    pm.scrollLayout(width= 500)
    pm.button(label= 'Creates Nodes', command= create_nodes, width= 500)
    
    row_layout = pm.rowColumnLayout(numberOfColumns= 3, columnWidth= [[1, 150], [2, 10], [3, 340]])
    pm.columnLayout(adjustableColumn= False, width=150)
    scroll_list = pm.textScrollList(width= 150, height= 150, selectCommand= pm.Callback(create_ui))
    pm.button(label= 'List Nodes', command= list_nodes, width= 150)
    pm.setParent(row_layout)
   
    pm.text(label= '')

    dyn_uis = pm.columnLayout(adjustableColumn= False, width= 340)
    
    myWin.show()

def create_ui(*args):
    selected = scroll_list.getSelectItem()[0]
    print selected
    pm.setParent(dyn_uis)
    
    my_ui = Node_UI(node='%s' %(selected))
    my_ui.create()
    

def list_nodes(* args):
    nodes = pm.ls(type= ['polyMoveUV']) # listing all polyMoveUV nodes in the scene
    
    scroll_list.removeAll() # clearing the text scroll list first
    
    for node in nodes:
        scroll_list.append('%s' % (str(node))) # appending to the scroll list
    
def create_nodes(* args):
    '''
    creates polyMoveUV nodes for currently selected objects
    '''
    
    objects = pm.ls(selection= True)
    

    for obj in objects:
        num_uvs = pm.polyEvaluate(obj, uvcoord= True)
        obj_uvs = '%s.map[0:%i]' % (obj, num_uvs)
        
        try:
            my_node = pm.mel.eval("polyMoveUV -constructionHistory 1 -random 0 %s" % (obj_uvs))[0]
            print my_node
            
            my_node = pm.rename(my_node, '%s_uvNode' % (obj))
            
            pm.setKeyframe('%s' % (my_node), attribute='translateU', t=['0sec','0.5sec'] )
            pm.setKeyframe('%s' % (my_node), attribute='translateV', t=['0sec','0.5sec'] )
            pm.setKeyframe('%s' % (my_node), attribute='rotationAngle', t=['0sec','0.5sec'] )
            pm.setKeyframe('%s' % (my_node), attribute='pivotU', t=['0sec','0.5sec'] )
            pm.setKeyframe('%s' % (my_node), attribute='pivotV', t=['0sec','0.5sec'] )
            pm.setKeyframe('%s' % (my_node), attribute='scaleU', t=['0sec','0.5sec'] )
            pm.setKeyframe('%s' % (my_node), attribute='scaleV', t=['0sec','0.5sec'] )
            pm.setKeyframe('%s' % (my_node), attribute='random', t=['0sec','0.5sec'] )
            
        except:
            print '# error'

    
    