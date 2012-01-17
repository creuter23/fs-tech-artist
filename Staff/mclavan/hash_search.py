import maya.cmds as cmds
cmds.addAttr(ln='layout_hash', dt='string')

cmds.setAttr('.layout_hash', '#backGround', type='string')

'''
Create a script to get all the available hash codes from particual attributes
in the scene.
Build a list.
'''

'''
Loops through all selected objects looking for a particular attribute.
Using pymel.

If the given hashCodes are present in the attribute it will be added to
to a given list.
'''
import pymel.core as pm

selected = pm.ls(sl=True)
background = []
hash = '#hero'
attr_name = 'layout_hash'
hashCodes = ['#tree', '#hero', '#backGround']
# hashCodes = ['#backGround']

for sel in selected:
    pieces = sel.attr(attr_name).get().split()
    valid = True   
    for hash in hashCodes:
        if hash not in pieces:
            valid = False
    if valid:            
        background.append(sel)
        
print background

# Recursive algo to stack hash codes together.

def hash_find(objects, attr_name, hash_codes=[]):
    hash_objects = []
      
    for obj in objects:
        valid = True  
        pieces = obj.attr(attr_name).get().split()
        for hash_item in hash_codes:
            if hash_item not in pieces:
                valid = False
        print valid
        if valid: 
            hash_objects.append(obj)
    return hash_objects
        
# detected_hash = hash_find(pm.ls(sl=True), 'layout_hash', ['#backGround'])

def test_gui():
    cmds.window()
    cmds.columnLayout()
    global attr_txt, hash_txt, search_txt
    cmds.text(l='attr')
    attr_txt = cmds.textField(w=100, text='layout_hash')
    
    cmds.text(l='hash#')
    hash_txt = cmds.textField(w=100, text='#backGround', cc=select_hash)
    
    cmds.text(l='search')
    search_txt = cmds.textField(w=100, text='pm.ls("*_world")')
    
    cmds.button(l='Apply', w=100, c=select_hash)
    cmds.showWindow()

def select_hash(*args):
    import maya.cmds as cmds
    import pymel.core as pm
    
    attr_name = cmds.textField(attr_txt, q=1, text=True)
    hash_str = cmds.textField(hash_txt, q=1, text=True)
    search_val = cmds.textField(search_txt, q=1, text=True)
    

    search_obj = eval(search_val)
    hash_list = hash_str.split()
    detected_hash = hash_find(search_obj, attr_name, hash_list)
    pm.select(detected_hash, r=True)
 
  