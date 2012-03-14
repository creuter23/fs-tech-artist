'''
#lockAndHide #loops #attributes

Michael Clavan
attr_script.py

Description:
    Various different tools for the rigging process.
'''


'''
Lock and Hide

Locking and Hiding attributes.
'''
import pymel.core as pm

def lock_and_hide(lock=True):
    # Get selected objects in the scene.
    selected = pm.ls(sl=True)
    
    # Decide which attributes to lock and hide or bring back.
    attrs = ['tx', 'ty', 'tz']
    
    # Loop through selected
    for sel in selected:
        # Loop through attributes
        for attr in attrs:   
            # Get attribute object
            attr_obj = sel.attr(attr)
            
            # Lock or Show
            if lock:
                # Look at the Attribute helpdocs under pymel.core.general.Attribute
                attr_obj.lock()
                attr_obj.set(k=False, cb=False)
            else:
                # The channelBox flag and keyable have a history of not working together nicely.
                #    So, I've seperated them.
                attr_obj.set(cb=True)
                attr_obj.set(k=True)
                attr_obj.unlock()






'''
Creating Attributes
Below are a few ways of creating attribute quickly.
'''


# CREATE ATTRIBUTE ON FIRST SELECTED OBJECT
selected = pm.ls(sl=True)
# Creating a custom attribute on a single object.
# attributeType = double, min -10, max 10, defaultValue 0, keyable True
selected[0].addAttr('index_curl', at='double', min=-10, max=10, dv=0, k=1)

# integer type (long) visible in the channelBox but not keyable
selected[0].addAttr('geo_vis', at='long', min=0, max=1, dv=0, k=1)
selected[0].attr('geo_vis').set(keyable=0, channelBox=1)

# ENUM (SEPARATOR)
attr = selected[0].addAttr('FINGERS', at='enum', en='-------------:', k=1 ) 
selected[0].attr('FINGERS').lock()

# CREATING ATTRIBUTES ON MULTIPLE OBJECTS
# Creating multiple attribute on selected objects.
selected = pm.ls(sl=True)
for sel in selected:
    selected[0].addAttr('strech', at='double', dv=0, k=1)


'''
Variable Practice
'''

'''
Rename
'''
