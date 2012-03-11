'''
Tags:
#xml #oop #layout #guiWidget

Info:
Layout Tool
layout_tool.py

Description:

Updates:
    - Initial build - mclavan

Known issues:
    - None

How to use:

import layout_tool
layout_tool.gui()
'''

# python modules
import os.path
import xml.etree.ElementTree as ET
# maya modules
import maya.cmds as cmds
import pymel.core as pm
# 3rd party

print 'Layout Tool Activated.'

class Asset():
    '''
    self.artist_texture = None
    self.artist_modeler = None
    self.artist_setup = None
    self.mov_file = None
    self.img_file = None
    '''
    
    def __init__(self, name, type, location, mod_art, txt_art=None, setup_art=None):
        self.asset_type = type
        self.asset_name = name
        self.location = location
        self.artist_modeler = mod_art
        self.artist_texture = txt_art
        self.artist_setup = setup_art
        self.mov_file = os.path.join(location, 'mov')
        self.img_file = os.path.join(location, 'img')
        
    def __str__(self):
        line = 'AssetName: %s Type: %s Location: %s\nArtist Mod: %s Txt: %s Rig: %s' % (self.asset_name, self.asset_type, self.location, self.artist_modeler, self.artist_texture, self.artist_setup)
        return line

class Asset_Store():
    '''
    Organizes all the possible assets.
    '''
    def __init__(self):
        self.all_assets = []
        self.props = []
        self.characters = []
        self.enviroments = []
    
    def add_asset(self, name, type, location, mod_art, txt_art=None, setup_art=None):
        current_asset = Asset(name, type, location, mod_art, txt_art, setup_art)
        self.all_assets.append(current_asset)
        if current_asset.asset_type == 'prop':
            self.props.append(current_asset)
        elif current_asset.asset_type == 'character':
            self.characters.append(current_asset)
        elif current_asset.asset_type == 'env':
            self.enviroments.append(current_asset)
    
        
current_store = Asset_Store()    

def load_xml(xml_file, xml_path=''):
    '''
    Loads an content from an xml
    XML Documention - http://effbot.org/zone/element-index.htm    

    '''
    if not xml_path:
        xml_path = os.path.split(__file__)[0]
    
    # Load xml
    file_info = open(os.path.join(xml_path, xml_file), 'r')
    tree = ET.parse(file_info)
    elem = tree.getroot()
    
    # current_store = Asset_Store()
    # Create Asset Store
    for e in elem:
        current_store.add_asset(e.get('name'), e.tag, e.get('location'), e.get('mod'), e.get('txt'), e.get('rig'))
        print e.get('name')
    


'''
Notes
import maya.cmds as cmds
import pymel.core as pm
import sys
sys.path.append('/Volumes/RBA/students/Technical_Arts_Group/projects/Layout_Tool')


import layout_tool
reload(layout_tool)
layout_tool.gui()

'''