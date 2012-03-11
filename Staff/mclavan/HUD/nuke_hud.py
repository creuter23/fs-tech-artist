'''
Hud Tool
Michael Clavan
nuke_hud.py


'''

import nuke


# nuke.toNode('nodeName')
"""
Example Data
seq_shot == 'Prop'
asset == 'Bench'
name == 'David Spade'
production == 'Awesome Clip'
department == 'Modeling'
date == '10/4/11'

import sys
sys.path.append('/Users/mclavan/Documents/Projects/HUD')
"""


def nuke_hud(label_data, node_name, read_data, write_name, write_data):
    '''
    Generates a hud in nuke.
    label_data (dict):
        Each key is the name of a text node in nuke.  The value contained in
        each key will be replacing the message data.
    read_data (dict):
        Updates the read node with current asset renders
    '''
    for text_node in label_data.keys():
        
        try:
            base_node = nuke.toNode(text_node)
            temp_knob = base_node.knob('message')
            temp_knob.setValue(label_data[text_node])
            print 'Node: %s --> %s' % (text_node, label_data[text_node])
        except AttributeError:
            print 'Node: %s: Error name mismatch!' % (text_node)
    
    base_node = nuke.toNode(node_name)

    for read_node in read_data.keys():
        try:
            temp_knob = base_node.knob(read_node)
            temp_knob.setValue(read_data[read_node])
        except AttributeError:
            print 'Attr: %s: %s Error name mismatch!' % (read_node, read_data[read_node])        
   
    # Update read data
    write_node = nuke.toNode(write_name)

    for write_node_info in write_data.keys():
        try:
            temp_knob = write_node.knob(write_node_info)
            temp_knob.setValue(write_data[write_node_info])
        except AttributeError:
            print 'Attr: %s: %s Error name mismatch!' % (write_node, write_data[write_node_info])        
    
    render_knob = write_node.knob('Render')
    render_knob.execute()
 
# Current data   
test_data = {'artist': 'David Spade', 'asset': 'Bench', 'seq_shot': 'Prop',
             'production': 'Awesome Clip', 'department': 'Modeling','date': '10/4/11'}
test_read = {'file': '/Users/mclavan/Documents/Projects/HUD/img/FireHydrant_LightTest.%03d.iff',
             'first': 1, 'last': 100}
file_name = 'current_test_2.mov'
test_write = {'file': '/Users/mclavan/Documents/Projects/HUD/img/%s' % file_name}

# Execute data
nuke_hud(test_data, 'Read5', test_read, 'write_high', test_write)

default_data = {'name': 'Katie Neylon', 'asset': 'Fire Hydrant', 'seq_shot': 'Prop',
             'production': 'TBA', 'department': 'Modeling','date': '09/30/11'}

"""
tag_names = ['asset', 'date', 'department', 'artist', 'production', 'seq_shot']
tag_objects = []
for tag_name in tag_names:
    tag_objects.append(nuke.toNode(tag_name))
    
# Get the knob
base_node = nuke.toNode('asset')
temp_knob = base_node.knob('message')
# Print out value
# temp_knob.value()
# Set Value
temp_knob.setValue('Fire Hydrant')
"""

'''
Test Code
import nuke

c = nuke.toNode('asset')
c.fullName()
help(c)

c.knobs()
help(c.knob('message')).toScript()

knob = c.knob('message')
knob.toString()
help(knob)
knob['message']

nuke.

print c.knob('message').name()
help(knob)
knob.value()
knob.setValue('Fire Hydrant')


'''
    
