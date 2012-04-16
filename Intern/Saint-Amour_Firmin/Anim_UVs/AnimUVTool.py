'''

Author:
    Firmin Saint-Amour
    
Description:
    This creates polyMoveUV nodes and creates gui components to edit
    their animation curve nodes
    
How to run:
    import AnimUVTool
    AnimUVTool.gui()
    
'''


import pymel.core as pm


class Node_UI():
    '''
    # creates uis for the selected node
    # takes the node as a string arg
    # retuns none
    '''
    def __init__(self, node):
        self.node = node # the polymove UV node
        
        self.layout = pm.frameLayout(label= '%s' % (self.node),  width= 340,
                                     collapsable= True)
        
        pm.button(label= 'Delete UI', command= pm.Callback(self.delete_ui))

    def delete_ui(self):
        # deletes the main frameLayout
        pm.deleteUI(self.layout)
    
    def insert_key(self, attr, value):
        '''
        # this inserts a key at the given position
        # take the attr to key and the position in time
        # attr example: 'pCube1.translateX'
        '''
        print attr, value.getValue(), attr, value.getValue()
        
        pm.setKeyframe('%s' % (attr), time= int(value.getValue()) )
        
        # reinvoking the create to add the uis for the new keys
        print 'recreating'
        pm.deleteUI(self.temp_layout)
        self.create()
        
    def delete_key(self, attr, index):
        '''
        # this delete the key at the given index
        # take the attr from which keys will be removed
        # attr example: 'pCube1.translateX'
        '''
        print attr, index.getValue(), attr, index.getValue()
        
        pm.cutKey('%s' % (attr), index= (index.getValue(),index.getValue()), clear= True)

        
        # reinvoking the create to add the uis for the new keys
        print 'recreating'
        pm.deleteUI(self.temp_layout)
        self.create()
        
    def create(self):
        '''
        this creates the gui components for the node
        '''
        
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
        
        
        pm.setParent(self.layout)
        self.temp_layout = pm.columnLayout(adjustableColumn= False, width= 340)
        
        # if the counts < 1 than the Anim curve node doesnt exist
        # the if statements just check which nodes exist
        
        if self.count_TU >= 1:
            pm.setParent(self.temp_layout)
            TU = Anim_UI(node= '%s_translateU' % (self.node), count = self.count_TU)
            TU.create()
            # index key
            pm.setParent('..')
            pm.text(label= 'Insert Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Key Position')
            insert_field = pm.intField()
            pm.button(label= 'Insert', command= pm.Callback(self.insert_key,
               attr= '%s.translateU' % (self.node), value= insert_field))
            
            
            # delete key
            pm.setParent('..')
            pm.text(label= 'Delete Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Key Index')
            delete_field = pm.intField()
            pm.button(label= 'Delete', command= pm.Callback(self.delete_key,
               attr= '%s.translateU' % (self.node), index= delete_field))

            
        if self.count_TV >= 1:
            pm.setParent(self.temp_layout)
            TV = Anim_UI(node= '%s_translateV' % (self.node), count = self.count_TV)
            TV.create()
            # insert key
            pm.setParent('..')
            pm.text(label= 'Insert Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Key Position')
            insert_field = pm.intField()
            pm.button(label= 'Insert', command= pm.Callback(self.insert_key,
               attr= '%s.translateV' % (self.node), value= insert_field))
            
            
            # delete key
            pm.setParent('..')
            pm.text(label= 'Delete Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Key Index')
            delete_field = pm.intField()
            pm.button(label= 'Delete', command= pm.Callback(self.delete_key,
               attr= '%s.translateV' % (self.node), index= delete_field))

            
        if self.count_RA >= 1:
            pm.setParent(self.temp_layout)
            RA = Anim_UI(node= '%s_rotationAngle' % (self.node), count = self.count_RA)
            RA.create()
            # insert key
            pm.setParent('..')
            pm.text(label= 'Insert Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Key Position')
            insert_field = pm.intField()
            pm.button(label= 'Insert', command= pm.Callback(self.insert_key,
               attr= '%s.rotationAngle' % (self.node), value= insert_field))
            
            
            # delete key
            pm.setParent('..')
            pm.text(label= 'Delete Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Key Index')
            delete_field = pm.intField()
            pm.button(label= 'Delete', command= pm.Callback(self.delete_key,
               attr= '%s.rotationAngle' % (self.node), index= delete_field))

        if self.count_PU >= 1:
            pm.setParent(self.temp_layout)
            PU = Anim_UI(node= '%s_pivotU' % (self.node), count = self.count_PU)
            PU.create()
            
            # index key
            pm.setParent('..')
            pm.text(label= 'Insert Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Key Position')
            insert_field = pm.intField()
            pm.button(label= 'Insert', command= pm.Callback(self.insert_key,
               attr= '%s.pivotU' % (self.node), value= insert_field))
            
            # delete key
            pm.setParent('..')
            pm.text(label= 'Delete Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Key Index')
            delete_field = pm.intField()
            pm.button(label= 'Delete', command= pm.Callback(self.delete_key,
               attr= '%s.pivotU' % (self.node), index= delete_field))
            
        if self.count_PV >= 1:
            pm.setParent(self.temp_layout)
            PV = Anim_UI(node= '%s_pivotV' % (self.node), count = self.count_PV)
            PV.create()
            
            # index key
            pm.setParent('..')
            pm.text(label= 'Insert Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Key Position')
            insert_field = pm.intField()
            pm.button(label= 'Insert', command= pm.Callback(self.insert_key,
               attr= '%s.pivotV' % (self.node), value= insert_field))
            
            # delete key
            pm.setParent('..')
            pm.text(label= 'Delete Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Key Index')
            delete_field = pm.intField()
            pm.button(label= 'Delete', command= pm.Callback(self.delete_key,
               attr= '%s.pivotV' % (self.node), index= delete_field))
            
        if self.count_SU >= 1:
            pm.setParent(self.temp_layout)
            SU = Anim_UI(node= '%s_scaleU' % (self.node), count = self.count_SU)
            SU.create()
            
            # index key
            pm.setParent('..')
            pm.text(label= 'Insert Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Key Position')
            insert_field = pm.intField()
            pm.button(label= 'Insert', command= pm.Callback(self.insert_key,
               attr= '%s.scaleU' % (self.node), value= insert_field))
            
            # delete key
            pm.setParent('..')
            pm.text(label= 'Delete Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Key Index')
            delete_field = pm.intField()
            pm.button(label= 'Delete', command= pm.Callback(self.delete_key,
               attr= '%s.scaleU' % (self.node), index= delete_field))
            
        if self.count_SV >= 1:
            pm.setParent(self.temp_layout)
            SV = Anim_UI(node= '%s_scaleV' % (self.node), count = self.count_SV)
            SV.create()
            
            # index key
            pm.setParent('..')
            pm.text(label= 'Insert Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Key Position')
            insert_field = pm.intField()
            pm.button(label= 'Insert', command= pm.Callback(self.insert_key,
               attr= '%s.scaleU' % (self.node), value= insert_field))
            
            # delete key
            pm.setParent('..')
            pm.text(label= 'Delete Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Key Index')
            delete_field = pm.intField()
            pm.button(label= 'Delete', command= pm.Callback(self.delete_key,
               attr= '%s.scaleV' % (self.node), index= delete_field))
            
        if self.count_R >= 1:
            pm.setParent(self.temp_layout)
            random = Anim_UI(node= '%s_random' % (self.node), count = self.count_R)
            random.create()
            
            # index key
            pm.setParent('..')
            pm.text(label= 'Insert Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Key Position')
            insert_field = pm.intField()
            pm.button(label= 'Insert', command= pm.Callback(self.insert_key,
               attr= '%s.random' % (self.node), value= insert_field))
            
            # delete key
            pm.setParent('..')
            pm.text(label= 'Delete Key')
            pm.rowColumnLayout(numberOfColumns= 3, columnWidth= ([1,113], [2,113], [3,113]))
            pm.text(label= 'Key Index')
            delete_field = pm.intField()
            pm.button(label= 'Delete', command= pm.Callback(self.delete_key,
               attr= '%s.random' % (self.node), index= delete_field))
                 
class Anim_UI():
    '''
    # this creates a frame layout for the given Anim curve node
    # node = animCurve node
    # count = the amount of keys
    # returns none
    '''
    
    def __init__(self, node, count):
        self.node = node
        self.count = count
    
    def create(self):
        '''
        this function creates the components
        '''
        self.layout = pm.frameLayout(label= str(self.node), width= 340, collapsable= True, collapse= True )
        pm.attrEnumOptionMenu( label='Pre Infinity ', attribute='%s.preInfinity' % (self.node) )
        pm.attrEnumOptionMenu( label='Post Infinity ', attribute='%s.postInfinity' % (self.node) )

        pm.rowColumnLayout(numberOfColumns= 5, columnWidth= ([1, 10], [2, 50], [3, 50], [4, 115], [5, 115]))
        pm.text(label= '')
        pm.text(label= 'Time')
        pm.text(label= 'Value')
        pm.text(label= 'inTan Type')
        pm.text(label= 'OutTan Type')
        
        # create components for each key
        for num in xrange(self.count):
            pm.text(label= str(num))
            
            time = Time_int(index= num, node= self.node)
            time.create()
            
            value = Value_float(index= num, node= self.node)
            value.create()
            
            in_tan = In_Tangent(index= num, node= self.node)
            in_tan.create()
            
            out_tan = Out_Tangent(index= num, node= self.node)
            out_tan.create()
        
class Time_int():
    '''
    # this creates an int field that will display and modify the time attr of
        key frames
    # takes the index for the key frame, and the anim curve node the key frame
        belongs to
    # returns none
    '''
    
    def __init__(self, index, node):
        self.node = node
        self.index = index
        
    def create(self):
        '''
        # this creates the int field
        '''
        current_time = pm.keyframe( '%s' % (self.node) , query=True,
                        index= (self.index, self.index), timeChange= True )[0]
        
        self.int_field = pm.intField(value= int(current_time), annotation= 'change the time for the keyframe',
                                changeCommand= pm.Callback(self.change_time))
        
    def change_time(self):
        '''
        # this function will change the time for the key frame
        '''
        pm.keyframe('%s' % (self.node), option='over', index=(int(self.index), int(self.index)), absolute= True, timeChange=int(self.int_field.getValue()))

class Value_float():
    '''
    # this creates a float field to display and change the value that was keyed
        on a key frame
      
    # takes the index of the keyframes, and the node for said keyframe    
    '''
    
    def __init__(self, index, node):
        self.node = node
        self.index = index
        
    def create(self):
        '''
        # this creates the float field
        '''
        current_time = pm.keyframe( '%s' % (self.node) , query=True, index= (self.index, self.index), valueChange= True )[0]
        self.int_field = pm.floatField(value= float(current_time), annotation= 'change the value for the keyframe',
                                changeCommand= pm.Callback(self.change_value))
        
    def change_value(self):
        '''
        this changes the value
        '''
        pm.keyframe('%s' % (self.node), option='over', index=(int(self.index), int(self.index)), absolute= True, valueChange=float(self.int_field.getValue()))
                
class In_Tangent():
    '''
    # this creates a text field which will display the in tangent type attr
        of a key frame
    # takes the index for the key frame and the respective node
    '''
    def __init__(self, index, node):
        self.node = node
        self.index = index
        
    def create(self):
        # this creates the text field
        current_type = pm.keyTangent( '%s' % (self.node) , query=True, index= (self.index, self.index), inTangentType= True )[0]
        self.text_field = pm.textField(text= '%s' % (current_type),
            changeCommand= pm.Callback(self.change_type), editable= True,
                annotation= "Use spline, clamped, linear, flat, step, stepnext,plateau, fixed or auto.")
    
    def change_type(self):
        # this changes the in tangent type
        pm.keyTangent('%s' % (self.node), index= (self.index, self.index), inTangentType= '%s' % (self.text_field.getText()))
        print 'in_tangent', self.node, self.text_field.getText()
        
class Out_Tangent():
    '''
    # this creates a text field which will display the out tangent type attr
        of a key frame
    # takes the index for the key frame and the respective node
    '''
    def __init__(self, index, node):
        self.node = node
        self.index = index
        
    
    def create(self):
        # this creates the field
        current_type = pm.keyTangent( '%s' % (self.node) , query=True, index= (self.index, self.index), outTangentType= True )[0]
        self.text_field = pm.textField(text= '%s' % (current_type),
            changeCommand= pm.Callback(self.change_type), editable= True,
                annotation= "Use spline, clamped, linear, flat, step, stepnext, plateau, fixed or auto.")
        
    def change_type(self):
        # this changes the out tangent type
        pm.keyTangent('%s' % (self.node), index= (self.index, self.index), outTangentType= '%s' % (self.text_field.getText()))
        print 'out_tangent', self.node, self.text_field.getText()
    
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
    scroll_list = pm.textScrollList(width= 150, height= 200, selectCommand= pm.Callback(create_ui))
    pm.button(label= 'List Nodes', command= list_nodes, width= 148)
    pm.setParent(row_layout)
   
    pm.text(label= '')

    dyn_uis = pm.columnLayout(adjustableColumn= False, width= 340)
    
    myWin.show()

def create_ui(*args):
    '''
    creates uis for the selected node from the text scroll list
    '''
    
    selected = scroll_list.getSelectItem()[0]
    print selected
    pm.setParent(dyn_uis)
    
    my_ui = Node_UI(node='%s' %(selected))
    my_ui.create()
    
def list_nodes(* args):
    '''
    # lists and appends all the polyMoveUV nodes in the scene
        to the text scroll list
    '''
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
        num_uvs = pm.polyEvaluate(obj, uvcoord= True) # getting all the uvs
        obj_uvs = '%s.map[0:%i]' % (obj, num_uvs)
        
        # just in case the wrong object type is selected
        try:
            my_node = pm.mel.eval("polyMoveUV -constructionHistory 1 \
                                  -random 0 %s" % (obj_uvs))[0]
            
            # renaming the node based on the object
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

    
    