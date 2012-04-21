'''
classes for light rigs
'''


import pymel.core as pm

class Light_directional():
    
    def __init__(self, light):
        
        self.light = light
        
    def create(self):
        
        
        self.main_layout = pm.columnLayout(adjustableColumn= True, width= 400)
       
        main_frame = pm.frameLayout( label='%s' % (self.light), collapsable= True)
        pm.frameLayout( label='Light Attributes', collapsable= True)
        pm.attrColorSliderGrp( at='%s.color' % (self.light), columnWidth4= [100, 75, 175, 50])
        pm.attrFieldSliderGrp(at='%s.intensity' % (self.light), columnWidth4= [100, 75, 175, 50])
       
        
        pm.setParent(main_frame)
        pm.frameLayout(label= 'Shadows', collapsable= True)
        pm.attrColorSliderGrp( at='%s.shadowColor' % (self.light),
                              columnWidth4= [100, 75, 175, 50])
        self.check_box = pm.checkBox(label= 'Use Ray Trace Shadows',
                        changeCommand= pm.Callback(self.shadows))
        
        self.light_angle = pm.attrFieldSliderGrp( at='%s.lightAngle' %(self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
        
        self.shadow_rays = pm.attrFieldSliderGrp( at='%s.shadowRays' % (self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
        
        self.ray_depth = pm.attrFieldSliderGrp( at='%s.rayDepthLimit' % (self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
       
        pm.setParent(main_frame)
        pm.rowColumnLayout(numberOfColumns= 2, columnWidth= [200, 200])
        pm.button(label= 'Select Light', width= 200, command= pm.Callback(self.select))
        pm.button(label= 'Delete UI', width= 200, command= pm.Callback(self.delete))
        pm.button(label= 'Hide', command= pm.Callback(self.hide))
        pm.button(label= 'Show',  command= pm.Callback(self.show))
        return self.main_layout
        
    def delete(self):
        pm.deleteUI(self.main_layout)
      
    def select(self):
        pm.select('%s' % (self.light))
        
    def show(self):
        pm.showHidden('%s' % (self.light))

    def hide(self):
        pm.hide('%s' % (self.light))
        
    def shadows(self):
        value = self.check_box.getValue()
        pm.setAttr('%s.useRayTraceShadows' % (self.light), int(value))
        #print '%s.decayRate' % light
        if value == 1:
            self.light_angle.setEnable(True)
            self.shadow_rays.setEnable(True)
            self.ray_depth.setEnable(True)
        
        if value == 0:
            self.light_angle.setEnable(False)
            self.shadow_rays.setEnable(False)
            self.ray_depth.setEnable(False)
    
class Light_ambient(Light_directional):
    
   def create(self):
        
        
        self.main_layout = pm.columnLayout(adjustableColumn= True, width= 400)
       
        main_frame = pm.frameLayout( label='%s' % (self.light), collapsable= True)
        pm.frameLayout( label='Light Attributes', collapsable= True)
        pm.attrColorSliderGrp( at='%s.color' % (self.light), columnWidth4= [100, 75, 175, 50])
        pm.attrFieldSliderGrp( at='%s.intensity' % (self.light), columnWidth4= [100, 75, 175, 50])
        pm.attrFieldSliderGrp(at='%s.ambientShade' % (self.light), columnWidth4= [100, 75, 175, 50])
       
        
        pm.setParent(main_frame)
        pm.frameLayout(label= 'Shadows', collapsable= True)
        pm.attrColorSliderGrp( at='%s.shadowColor' % (self.light),
                              columnWidth4= [100, 75, 175, 50])
        self.check_box = pm.checkBox(label= 'Use Ray Trace Shadows',
                        changeCommand= pm.Callback(self.shadows))
        
        self.shadow_radius = pm.attrFieldSliderGrp( at='%s.shadowRadius' %(self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
        
        self.shadow_rays = pm.attrFieldSliderGrp( at='%s.shadowRays' % (self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
        
        self.ray_depth = pm.attrFieldSliderGrp( at='%s.rayDepthLimit' % (self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
       
        pm.setParent(main_frame)
        pm.rowColumnLayout(numberOfColumns= 2, columnWidth= [200, 200])
        pm.button(label= 'Select Light', width= 200, command= pm.Callback(self.select))
        pm.button(label= 'Delete UI', width= 200, command= pm.Callback(self.delete))
        pm.button(label= 'Hide', command= pm.Callback(self.hide))
        pm.button(label= 'Show',  command= pm.Callback(self.show))
        return self.main_layout
    
   def shadows(self):
        value = self.check_box.getValue()
        pm.setAttr('%s.useRayTraceShadows' % (self.light), int(value))
        
        if value == 1:
            self.shadow_radius.setEnable(True)
            self.shadow_rays.setEnable(True)
            self.ray_depth.setEnable(True)
        
        if value == 0:
            self.shadow_radius.setEnable(False)
            self.shadow_rays.setEnable(False)
            self.ray_depth.setEnable(False)
        
class Light_spot():
    
    def __init__(self, light):
        
        self.light = light
        
    def create(self):
        
        
        
        self.main_layout = pm.columnLayout(adjustableColumn= True, width= 400)
       
        main_frame = pm.frameLayout( label='%s' % (self.light), collapsable= True)
        pm.frameLayout( label='Light Attributes', collapsable= True)
        pm.attrColorSliderGrp( at='%s.color' % (self.light), columnWidth4= [100, 75, 175, 50])
        pm.attrFieldSliderGrp(at='%s.intensity' % (self.light), columnWidth4= [100, 75, 175, 50])
        pm.attrFieldSliderGrp(at='%s.coneAngle' % (self.light), columnWidth4= [100, 75, 175, 50])
        pm.attrFieldSliderGrp(at='%s.penumbraAngle' % (self.light), columnWidth4= [100, 75, 175, 50])
        pm.attrFieldSliderGrp(at='%s.dropoff' % (self.light), columnWidth4= [100, 75, 175, 50])
        pm.attrEnumOptionMenu( label='Decay Rate', attribute='%s.decayRate' % (self.light) )
        
        pm.setParent(main_frame)
        pm.frameLayout(label= 'Shadows', collapsable= True)
        pm.attrColorSliderGrp( at='%s.shadowColor' % (self.light),
                              columnWidth4= [100, 75, 175, 50])
        self.check_box = pm.checkBox(label= 'Use Ray Trace Shadows',
                        changeCommand= pm.Callback(self.shadows))
        
        self.light_radius = pm.attrFieldSliderGrp( at='%s.lightRadius' % (self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
        
        self.shadow_rays = pm.attrFieldSliderGrp( at='%s.shadowRays' % (self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
        
        self.ray_depth = pm.attrFieldSliderGrp( at='%s.rayDepthLimit' % (self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
       
        pm.setParent(main_frame)
        pm.rowColumnLayout(numberOfColumns= 2, columnWidth= [200, 200])
        pm.button(label= 'Select Light', width= 200, command= pm.Callback(self.select))
        pm.button(label= 'Delete UI', width= 200, command= pm.Callback(self.delete))
        pm.button(label= 'Hide', command= pm.Callback(self.hide))
        pm.button(label= 'Show',  command= pm.Callback(self.show))
        return self.main_layout
        
        
    def delete(self):
        pm.deleteUI(self.main_layout)
        
    def select(self):
        pm.select('%s' % (self.light))
        
    def show(self):
        pm.showHidden('%s' % (self.light))

    def hide(self):
        pm.hide('%s' % (self.light))
        
    def shadows(self):
        value = self.check_box.getValue()
        pm.setAttr('%s.useRayTraceShadows' % (self.light), int(value))
        
        if value == 1:
            self.light_radius.setEnable(True)
            self.shadow_rays.setEnable(True)
            self.ray_depth.setEnable(True)
        
        if value == 0:
            self.light_radius.setEnable(False)
            self.shadow_rays.setEnable(False)
            self.ray_depth.setEnable(False)
                        
class Light_point(Light_spot):
    def create(self):
        
        
        
        self.main_layout = pm.columnLayout(adjustableColumn= True, width= 400)
       
        main_frame = pm.frameLayout( label='%s' % (self.light), collapsable= True)
        pm.frameLayout( label='Light Attributes', collapsable= True)
        pm.attrColorSliderGrp( at='%s.color' % (self.light), columnWidth4= [100, 75, 175, 50])
        pm.attrFieldSliderGrp(at='%s.intensity' % (self.light), columnWidth4= [100, 75, 175, 50])
        
        pm.attrEnumOptionMenu( label='Decay Rate', attribute='%s.decayRate' % (self.light) )
        
        pm.setParent(main_frame)
        pm.frameLayout(label= 'Shadows', collapsable= True)
        pm.attrColorSliderGrp( at='%s.shadowColor' % (self.light),
                              columnWidth4= [100, 75, 175, 50])
        self.check_box = pm.checkBox(label= 'Use Ray Trace Shadows',
                        changeCommand= pm.Callback(self.shadows))
        
        self.light_radius = pm.attrFieldSliderGrp( at='%s.lightRadius' % (self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
        
        self.shadow_rays = pm.attrFieldSliderGrp( at='%s.shadowRays' % (self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
        
        self.ray_depth = pm.attrFieldSliderGrp( at='%s.rayDepthLimit' % (self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
       
        pm.setParent(main_frame)
        pm.rowColumnLayout(numberOfColumns= 2, columnWidth= [200, 200])
        pm.button(label= 'Select Light', width= 200, command= pm.Callback(self.select))
        pm.button(label= 'Delete UI', width= 200, command= pm.Callback(self.delete))
        pm.button(label= 'Hide', command= pm.Callback(self.hide))
        pm.button(label= 'Show',  command= pm.Callback(self.show))
        return self.main_layout
    
class Light_area(Light_spot):
    def create(self):
        
        
        
        self.main_layout = pm.columnLayout(adjustableColumn= True, width= 400)
       
        main_frame = pm.frameLayout( label='%s' % (self.light), collapsable= True)
        pm.frameLayout( label='Light Attributes', collapsable= True)
        pm.attrColorSliderGrp( at='%s.color' % (self.light), columnWidth4= [100, 75, 175, 50])
        pm.attrFieldSliderGrp(at='%s.intensity' % (self.light), columnWidth4= [100, 75, 175, 50])
        
        
        pm.attrEnumOptionMenu( label='Decay Rate', attribute='%s.decayRate' % (self.light) )
        
        pm.setParent(main_frame)
        pm.frameLayout(label= 'Shadows', collapsable= True)
        pm.attrColorSliderGrp( at='%s.shadowColor' % (self.light),
                              columnWidth4= [100, 75, 175, 50])
        self.check_box = pm.checkBox(label= 'Use Ray Trace Shadows',
                        changeCommand= pm.Callback(self.shadows))
        
        self.shadow_rays = pm.attrFieldSliderGrp( at='%s.shadowRays' % (self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
        
        self.ray_depth = pm.attrFieldSliderGrp( at='%s.rayDepthLimit' % (self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
        
        pm.setParent(main_frame)
        pm.frameLayout(label= 'Mental Ray', collapsable= True)
        pm.frameLayout(label= 'Area Light', collapsable= True)
        self.checkbox_shape = pm.checkBox(label= 'Use Light Shape',
                        changeCommand= pm.Callback(self.use_shape))
        
        # setAttr "areaLightShape1.areaType" 1; areaHiSamples areaHiSampleLimit areaLoSamples
        pm.attrEnumOptionMenu( label='Type', attribute='%s.areaType' % (self.light))
        # areaVisible
        pm.attrFieldGrp(attribute='%s.areaHiSamples' % (self.light), enable= False)
        pm.attrFieldGrp(attribute='%s.areaHiSampleLimit' % (self.light), enable= False)
        pm.attrFieldGrp(attribute='%s.areaLoSamples' % (self.light), enable= False)
        # areaShapeIntensity
        self.checkbox_vis = pm.checkBox(label= 'Visible',
                        changeCommand= pm.Callback(self.visibility))
        
        pm.attrFieldSliderGrp( at='%s.areaShapeIntensity' % (self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])


       
        pm.setParent(main_frame)
        pm.rowColumnLayout(numberOfColumns= 2, columnWidth= [200, 200])
        pm.button(label= 'Select Light', width= 200, command= pm.Callback(self.select))
        pm.button(label= 'Delete UI', width= 200, command= pm.Callback(self.delete))
        pm.button(label= 'Hide', command= pm.Callback(self.hide))
        pm.button(label= 'Show',  command= pm.Callback(self.show))
        return self.main_layout
    
    def shadows(self):
        value = self.check_box.getValue()
        pm.setAttr('%s.useRayTraceShadows' % (self.light), int(value))
        #print '%s.decayRate' % light
        if value == 1:
            #self.light_radius.setEnable(True)
            self.shadow_rays.setEnable(True)
            self.ray_depth.setEnable(True)
        
        if value == 0:
            #self.light_radius.setEnable(False)
            self.shadow_rays.setEnable(False)
            self.ray_depth.setEnable(False)
        
class Light_volume(Light_spot):
    def create(self):
        
        self.main_layout = pm.columnLayout(adjustableColumn= True, width= 400)
       
        main_frame = pm.frameLayout( label='%s' % (self.light), collapsable= True)
        pm.frameLayout( label='Light Attributes', collapsable= True)
        pm.attrColorSliderGrp( at='%s.color' % (self.light), columnWidth4= [100, 75, 175, 50])
        pm.attrFieldSliderGrp(at='%s.intensity' % (self.light), columnWidth4= [100, 75, 175, 50])
        
        pm.attrEnumOptionMenu( label='Light Shape', attribute='%s.lightShape' % (self.light) )
        
        pm.setParent(main_frame)
        pm.frameLayout(label= 'Shadows', collapsable= True)
        pm.attrColorSliderGrp( at='%s.shadowColor' % (self.light),
                              columnWidth4= [100, 75, 175, 50])
        self.check_box = pm.checkBox(label= 'Use Ray Trace Shadows',
                        changeCommand= pm.Callback(self.shadows))
        
        self.light_angle = pm.attrFieldSliderGrp( at='%s.lightAngle' % (self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
        
        self.light_radius = pm.attrFieldSliderGrp( at='%s.lightRadius' % (self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
        
        self.shadow_rays = pm.attrFieldSliderGrp( at='%s.shadowRays' % (self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
        
        self.ray_depth = pm.attrFieldSliderGrp( at='%s.rayDepthLimit' % (self.light),
                                enable= False, columnWidth4= [100, 75, 175, 50])
       
        pm.setParent(main_frame)
        pm.rowColumnLayout(numberOfColumns= 2, columnWidth= [200, 200])
        pm.button(label= 'Select Light', width= 200, command= pm.Callback(self.select))
        pm.button(label= 'Delete UI', width= 200, command= pm.Callback(self.delete))
        pm.button(label= 'Hide', command= pm.Callback(self.hide))
        pm.button(label= 'Show',  command= pm.Callback(self.show))
        return self.main_layout
    
    
            
    def shadows(self):
        value = self.check_box.getValue()
        pm.setAttr('%s.useRayTraceShadows' % (self.light), int(value))
        #print '%s.decayRate' % light
        if value == 1:
            self.light_angle.setEnable(True)
            self.light_radius.setEnable(True)
            self.shadow_rays.setEnable(True)
            self.ray_depth.setEnable(True)
        
        if value == 0:
            self.light_angle.setEnable(False)
            self.light_radius.setEnable(False)
            self.shadow_rays.setEnable(False)
            self.ray_depth.setEnable(False)
        
class IBL_UI():
    def __init__(self, obj):
        self.obj = obj
        
        
    def create(self):
        
        main_layout = pm.columnLayout(adjustableColumn= True, width= 400)
        main_frame = pm.frameLayout( label='%s' % (self.obj), collapsable= True)
        pm.columnLayout(adjustableColumn= False, width= 400)
        self.mapping_menu = pm.optionMenu( label='Mapping', width= 150,
                changeCommand= pm.Callback(self.mapping_type, self.obj))
        pm.menuItem( label='Spherical')
        pm.menuItem( label='Angular')
        
        pm.setParent(main_frame)
        self.type_menu = pm.optionMenu( label='Type', width= 150,
                changeCommand= pm.Callback(self.file_type, self.obj))
        pm.menuItem( label='Image File')
        pm.menuItem( label='Texture')
        
        self.image_field = pm.textFieldButtonGrp(label= 'Image Name', editable= False, columnWidth3= [100,200,100],
                buttonLabel= '<<<', buttonCommand= pm.Callback(self.load_image, self.obj))
        
        
        self.list_field = pm.textScrollList(allowMultiSelection= False ,
                    width= 100, height= 100)
        pm.attrColorSliderGrp( at='%s.color' % (self.obj),
                              columnWidth4= [100, 75, 175, 50])
        
        pm.rowColumnLayout(numberOfColumns= 2, columnWidth= ([1, 200], [2, 200]))
        pm.button(label= 'List Ramps', command= pm.Callback(self.list_textures))
        pm.button(label= 'Link Ramps', command= pm.Callback(self.link_texture, self.obj))
        pm.button(label= 'Edit Ramps', command= pm.Callback(self.edit_ramp))
        pm.button(label= 'Create Ramps', command= pm.Callback(self.create_ramp))
        
        
    def edit_ramp(self):
        selected = self.list_field.getSelectItem()[0]
        
        # pm.rampColorPort( node=selected )
        
        self.customWin = 'editramps'
        if (pm.window(self.customWin, exists=True)):
            pm.deleteUI(self.customWin)
        
        if (pm.windowPref(self.customWin, exists=True)):
            pm.windowPref(self.customWin, remove = True)
            
        myWin = pm.window(self.customWin, title = 'EDIT RAMPS', width = 400, height = 150, backgroundColor=[.5,.5,.5])
        pm.columnLayout(adjustableColumn=True)
        colors = pm.attrColorSliderGrp(columnWidth4= [100, 75, 175, 50])
        my_port = pm.rampColorPort(node= selected, sc= colors)
        
        
        
        
        
        
        myWin.show()
        
        
    def create_ramp(self):
        
        my_ramp = pm.shadingNode('ramp', asTexture= True)
        
        
        self.customWin = 'customramps'
        if (pm.window(self.customWin, exists=True)):
            pm.deleteUI(self.customWin)
        
        if (pm.windowPref(self.customWin, exists=True)):
            pm.windowPref(self.customWin, remove = True)
            
        myWin = pm.window(self.customWin, title = 'CUSTOM RAMPS', width = 200, height = 150, backgroundColor=[.5,.5,.5])
        pm.columnLayout(adjustableColumn=True)
        
        colors = pm.attrColorSliderGrp(columnWidth4= [100, 75, 175, 50])
        my_port = pm.rampColorPort(node= my_ramp, sc= colors)
        self.ramp_field = pm.textFieldButtonGrp(label= 'ramp name', buttonLabel= 'rename', buttonCommand= pm.Callback(self.rename, my_ramp),
                             columnWidth3= [150,100,150])
        
        myWin.show()
    
    def rename(self, obj):
        pm.rename(obj, self.ramp_field.getText())
        
        
        
    def mapping_type(self, obj):
        selected = self.mapping_menu.getSelect()
            # setAttr mentalrayIblShape1.mapping 1; angular
            # setAttr mentalrayIblShape1.mapping 0; spherical
        print selected
        if selected == 1:
            pm.setAttr('%s.mapping' % (str(obj)), 0 ) # spherical
            
        if selected == 2:
            pm.setAttr('%s.mapping' % (str(obj)), 1 ) # angular
            
            
    def file_type(self, obj):
        selected = self.type_menu.getSelect()
            # setAttr mentalrayIblShape1.type 1; texture
            # setAttr mentalrayIblShape1.type 0; image file
        print selected
        
        if selected == 1:
            pm.setAttr('%s.type' % (str(obj)), 0 ) # image file
            
        if selected == 2:
            pm.setAttr('%s.type' % (str(obj)), 1 ) # texture
            
            
    def load_image(self, obj):
        image = pm.fileDialog2(dialogStyle= 2, fileMode= 1)[0]
        self.image_field.setText('%s' % (str(image)))
        pm.setAttr('%s.texture' %(str(obj)), r'%s' %(image), type= 'string')
        
    def list_textures(self):
        textures = pm.ls(type= ['ramp'])
        self.list_field.removeAll()
        for texture in textures:
            
            self.list_field.append('%s' % (str(texture)))
            
            
    def link_texture(self, obj):
        selected = self.list_field.getSelectItem()[0]
        # connectAttr -f ramp1.outColor mentalrayIblShape1.color;
        print selected
        pm.connectAttr('%s.outColor' % (str(selected)), '%s.color' % (str(obj)), force= True)
        
        

    
                
            
        
        
        #cmds.setAttr('%s.texture'  % mentalrayIblShape1 ,r'/Users/Fearman/Desktop/dre.png', type= 'string')

            