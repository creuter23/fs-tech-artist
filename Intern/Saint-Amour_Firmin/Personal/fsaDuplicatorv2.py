"""
Author : Firmin Saint-Amour

Description : creates 'stuff' based on the postion of follicles
also picks a random object in the 'stuff' list

import fsaDuplicator
fsaDuplicator.gui()

"""

import pymel.core as pm
import maya.mel as mel
import random


class Main():
    bar = None
    
    def __init__( self , geo , u , v ):
        self.u = u
        self.v = v
        self.geo = geo
        pm.select( self.geo )
        print self.geo
        mel.eval( 'createHair '+str(u)+' '+str(v)+' 2 0 0 0 0 0 0 2 2 1' )
        pm.Callback( self.cleanUp() )
        
        
   
            
    
        
    def window(self):
        self.win = 'progresswin'
        self.num = (len(self.folls)/100)
        if(pm.window(self.win, ex = True)):
            pm.deleteUI(self.win)
        
        if(pm.windowPref(self.win, ex = True)):
            pm.windowPref(self.win, remove = True)
        progressWin = pm.window(self.win, title = '' , sizeable = False, width = 300, backgroundColor = [.5, .5, .5])
        pm.columnLayout(adjustableColumn = True)
        self.bar = pm.progressBar(minValue = 0, maxValue=100, width=300, step=1)
        progressWin.show()
    
    def delete(self):
        if(pm.window(self.win, ex = True)):
            pm.deleteUI(self.win)
            
    def edit(self):
        
        pm.progressBar(self.bar, edit = True, step = int(self.num))
        
        self.num += self.num
        
        
    # duplicates an object and places where the follicle is also does a parentConstraint()    
    def populate( self , obj = [] ):
        
        customRange = len(obj)
        self.obj = obj
        
        pm.select( '%sFollicle*' % self.geo )
        pm.select( '%sFollicleShape*' % self.geo , d=1 )
        self.folls = pm.ls( selection = True)
        
        self.window()
        
        # finding the name of the hair system to name the group() that all the duplicated objects will be parented to
        pm.select('%sFollicle*' % self.geo)
        pm.select('%sFollicleShape*' % self.geo, d = 1 )
        folls = pm.ls( selection = True )
        myHair = folls[0].getParent()
        system = myHair.split( 'F' )
        mySystem = system[0]
        
        # the group() for the duplicated geo
        self.geoPad = pm.group(name = '%s_geo' % mySystem, em= True)
        # creating a pop up window to show the progress
        print self.obj , customRange
        
        
        
        for foll in self.folls:
            # picking a random number between 0 and 4
            # this number will be plugged into a list[rand] to pick a random object
            self.rand = random.randrange(int(customRange))
            
            # this section will randomize the transformations
            sx = random.uniform( xScaleFieldMin.getValue() , xScaleFieldMax.getValue() )
            sy = random.uniform( yScaleFieldMin.getValue() , yScaleFieldMax.getValue() )
            sz = random.uniform( zScaleFieldMin.getValue() , zScaleFieldMax.getValue() )
            
            tx = random.uniform( xTranslateFieldMin.getValue() , xTranslateFieldMax.getValue() )
            ty = random.uniform( yTranslateFieldMin.getValue() , yTranslateFieldMax.getValue() )
            tz = random.uniform( zTranslateFieldMin.getValue() , zTranslateFieldMax.getValue() )
            
            rx = random.uniform( xRotateFieldMin.getValue() , xRotateFieldMax.getValue() )
            ry = random.uniform( yRotateFieldMin.getValue() , yRotateFieldMax.getValue() )
            rz = random.uniform( zRotateFieldMin.getValue() , zRotateFieldMax.getValue() )
            
            #print self.bar
            
            # duplicating the object
            newobj = pm.duplicate( self.obj[ self.rand ] , rr = True )
            point = pm.pointConstraint( foll , newobj )
            pm.delete( point )
            pm.makeIdentity( newobj , apply = True , t = 1 , r = 1 , s = 1 , n = 0 )
            # apllying the random Transforms
            pm.scale( newobj , [ sx , sy , sz ]  )
            pm.move( newobj , [ tx , ty , tz ]  )
            pm.rotate( newobj , [ rx , ry , rz ] )
            # parentConstraint() to the follicle
            print rx, ry, rz, tx, tz, ty, sx, sy, sz
            pm.parentConstraint( foll , newobj, mo = True )
            # parenting the objects to the group
            pm.parent(newobj , self.geoPad)
            
            self.edit()
        
        self.delete()
            
            
    
    
    # this function gets rid of the uneeded objects like the hairSystem, and the outputCurves group, cause we just need the follicles        
    def cleanUp(self):
        pm.select('%sFollicle*' % self.geo)
        pm.select('%sFollicleShape*' % self.geo , d = 1 )
        folls = pm.ls( selection = True )
        myHair = folls[0].getParent()
        system = myHair.split( 'F' )
        mySystem = system[0]
        
        pm.delete( '%sOutputCurves' % mySystem )
        pm.delete( mySystem )
            
    
    
win = 'duplicatorWin'    
def gui():
    global objList, myScrollField
    global obj01Field , obj02Field , obj03Field , obj04Field , geoField , uSlider , vSlider 
    global xRotateFieldMax , yRotateFieldMax , zRotateFieldMax , xTranslateFieldMax , yTranslateFieldMax , zTranslateFieldMax , xScaleFieldMax , yScaleFieldMax, zScaleFieldMax
    global xRotateFieldMin , yRotateFieldMin , zRotateFieldMin , xTranslateFieldMin , yTranslateFieldMin , zTranslateFieldMin , xScaleFieldMin , yScaleFieldMin, zScaleFieldMin
    objList = []
    if(pm.window(win, ex = True)):
        pm.deleteUI(win)
        
    if(pm.windowPref(win, ex = True)):
        pm.windowPref(win, remove = True)
        
    myWin = pm.window(win, title = 'fsaDuplicator', sizeable = False, mnb = True, width = 280 , backgroundColor = [.5, .5, .5])
    
    main = pm.rowColumnLayout()
    pm.text(label = 'surface')
    
    pm.separator(style = 'in', height = 15)
    geoField = pm.textFieldButtonGrp( text='surface', buttonLabel='<<<', bc=loadGeo, ed=0 , width = 280 )
    pm.separator(style = 'in', height = 15)
    pm.text(label = 'objects')
    '''
    obj01Field = pm.textFieldButtonGrp( text = 'obj01' , buttonLabel = '<<<' , bc = loadObj01 , ed = 0 , width = 280 )
    obj02Field = pm.textFieldButtonGrp( text = 'obj02' , buttonLabel = '<<<' , bc = loadObj02 , ed = 0 , width = 280 )
    obj03Field = pm.textFieldButtonGrp( text = 'obj03' , buttonLabel = '<<<' , bc = loadObj03 , ed = 0 , width = 280 )
    obj04Field = pm.textFieldButtonGrp( text = 'obj04' , buttonLabel = '<<<' , bc = loadObj04 , ed = 0 , width = 280 )
    '''
    pm.button(label = 'add objects', command = addobj)
    myScrollField = pm.scrollField(w = 280, height = 50, wordWrap = True)
    
    pm.separator(style = 'in', height = 15)
    pm.text(label = 'u density')
    uSlider = pm.intSliderGrp( min = 1 , max = 100, field = True , width = 280 )
    pm.text(label = 'v density')
    vSlider = pm.intSliderGrp( min = 1 , max = 100, field = True , width = 280 )
    pm.separator(style = 'in', height = 15)
    pm.text(label = 'randomize transforms')
    
    rows = pm.rowColumnLayout( numberOfColumns = 6 , columnWidth = [ [ 1 , 43 ] , [ 2 , 50 ] , [ 3 , 43 ] , [ 4 , 50 ] , [ 5 , 43 ] , [ 6 , 50 ] ] )
    
    # creating 'separators'
    pm.text( label = '' )
    pm.text( label = '' )
    pm.text( label = '' )
    pm.text( label = '' )
    pm.text( label = '' )
    pm.text( label = '' )
    
    pm.text(label = 'sxMin')
    xScaleFieldMin = pm.floatField( min = -100, max = 100 , value = 1 , width = 50 )
    pm.text(label = 'syMin')
    yScaleFieldMin = pm.floatField( min = -100, max = 100 , value = 1 , width = 50 )
    pm.text(label = 'szMin')
    zScaleFieldMin = pm.floatField( min = -100, max = 100 , value = 1 , width = 50 )
    
    pm.text(label = 'sxMax')
    xScaleFieldMax = pm.floatField( min = -100, max = 100 , value = 1 , width = 50 )
    pm.text(label = 'syMax')
    yScaleFieldMax = pm.floatField( min = -100, max = 100 , value = 1 , width = 50 )
    pm.text(label = 'szMax')
    zScaleFieldMax = pm.floatField( min = -100, max = 100 , value = 1 , width = 50 )
    
    # creating 'separators'
    pm.text( label = '' )
    pm.text( label = '' )
    pm.text( label = '' )
    pm.text( label = '' )
    pm.text( label = '' )
    pm.text( label = '' )
    
    
    
    pm.text(label = 'rxMin')
    xRotateFieldMin = pm.floatField( min = -360, max = 360 , width = 50 )
    pm.text(label = 'ryMin')
    yRotateFieldMin = pm.floatField( min = -360, max = 360 , width = 50 )
    pm.text(label = 'rzMin')
    zRotateFieldMin = pm.floatField( min = -360, max = 360 , width = 50 )
    
    pm.text(label = 'rxMax')
    xRotateFieldMax = pm.floatField( min = -360, max = 360, width = 50 )
    pm.text(label = 'ryMax')
    yRotateFieldMax = pm.floatField( min = -360, max = 360 , width = 50 )
    pm.text(label = 'rzMax')
    zRotateFieldMax = pm.floatField( min = -360, max = 360 , width = 50 )
    
    # creating 'separators'
    pm.text( label = '' )
    pm.text( label = '' )
    pm.text( label = '' )
    pm.text( label = '' )
    pm.text( label = '' )
    pm.text( label = '' )
    
    pm.setParent( rows )
    pm.text(label = 'txMin')
    xTranslateFieldMin = pm.floatField( min = -100, max = 100 , width = 50 )
    pm.text(label = 'tyMin')
    yTranslateFieldMin = pm.floatField( min = -100, max = 100 , width = 50 )
    pm.text(label = 'tzMin')
    zTranslateFieldMin = pm.floatField( min = -100, max = 100 , width = 50 )
    
    pm.text(label = 'txMax')
    xTranslateFieldMax = pm.floatField( min = -100, max = 100 , width = 50 )
    pm.text(label = 'tyMax')
    yTranslateFieldMax = pm.floatField( min = -100, max = 100 , width = 50 )
    pm.text(label = 'tzMax')
    zTranslateFieldMax = pm.floatField( min = -100, max = 100 , width = 50 )
    
    pm.setParent( main )
    pm.separator(style = 'in', height = 15)
    
    pm.button( label = 'replicate' , command = replicateFunction )
    
    myWin.show()

# instances the Main() class
def replicateFunction(* args):
    
    instance = Main( geo = str(geoField.getText()) , u = uSlider.getValue() , v = vSlider.getValue() ).populate( obj = objList )
  

# loads the selected object into the matching text field        
def addobj(* args):
    x = pm.ls( sl = 1 )[0]
    myScrollField.insertText( x+',' )
    objList.append(x)

# loads the selected object into the matching text field        
def loadGeo(* args):
    x = pm.ls( sl = 1 )[0]
    geoField.setText( x )

def loadObj02(* args):
    x = pm.ls( sl = 1 )[0]
    obj02Field.setText( x )
    
def loadObj03(* args):
    x = pm.ls( sl = 1 )[0]
    obj03Field.setText( x )
                
def loadObj04(* args):
    x = pm.ls( sl = 1 )[0]
    obj04Field.setText( x )
