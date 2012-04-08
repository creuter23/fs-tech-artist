'''
Layout generator
layout_gen.py


How to Run:
import layout_gen
layout_gen.gui()

'''

import pymel.core as pm

class Asset_Widget():
    '''
    Widget Interface - Contains information
    '''
    
    def __init__(self, current_parent, asset_name):
        '''
        Init asset class
        '''
        self.asset_name = asset_name
        self.parent = current_parent
        self.asset_widget(self.parent, self.asset_name)
    
    def reference_asset(self, res='low'):
        print '%s has been added @ %s.' % (self.asset_name, res)
    
    
        
    def asset_widget(self, current_parent, asset_name):
        '''
        Single asset widget.
        '''
        self.main = pm.frameLayout(labelVisible=False,
                              parent=current_parent)
        self.form = pm.formLayout()
        # Creating Components
        self.asset_image = pm.button(width=48, height=48)
        self.asset_text = pm.text(height=48, width=125, align='left', 
                    label=asset_name)
        self.asset_low = pm.button(height=26, width=75, label='Low',
                                   command=pm.Callback(self.reference_asset, 'low'))
        self.asset_med = pm.button(height=26, width=75, label='Medium',
                                   command=pm.Callback(self.reference_asset, 'medium'))
        self.asset_high = pm.button(height=26, width=75, label='High',
                                   command=pm.Callback(self.reference_asset, 'high'))
        
        # Positioning Components.
        # Symbol Button
        self.form.attachForm(self.asset_image, 'top', 5)
        self.form.attachForm(self.asset_image, 'left', 5)
        
        # asset text
        self.form.attachForm(self.asset_text, 'top', 5)
        self.form.attachForm(self.asset_low, 'top', 15)
        self.form.attachForm(self.asset_med, 'top', 15)
        self.form.attachForm(self.asset_high, 'top', 15)
        
        
        self.form.attachControl(self.asset_text, 'left', 15, self.asset_image)
        # form.attachControl(asset_text, 'right', 5, asset_low)
    
        self.form.attachControl(self.asset_low, 'left', 5, self.asset_text)
        self.form.attachControl(self.asset_med, 'left', 5, self.asset_low)
        self.form.attachControl(self.asset_high, 'left', 5, self.asset_med)
    
        self.form.attachForm(self.asset_high, 'right', 5)
        self.form.attachForm(self.asset_image, 'bottom', 5)
    
        # res buttons
        
        
        # Return parent to orginal layout
        pm.setParent(current_parent)
      
    

def gui():
    '''
    Main Interface
    '''
    win = pm.window(w=300)
    main = pm.columnLayout()
    scroll = pm.scrollLayout(w=400, height=200)
    
    global asset_1, asset_2, asset_3
    asset_1 = Asset_Widget(scroll, 'trafficLight1')
    asset_2 = Asset_Widget(scroll, 'mailBox1')
    asset_3 = Asset_Widget(scroll, 'mailBox2')

    
    '''
    asset_widget(scroll)
    asset_widget(scroll)
    asset_widget(scroll)
    asset_widget(scroll)
    '''
    win.show()
    
def asset_widget(current_parent):
    '''
    Single asset widget.
    '''
    main = pm.frameLayout(labelVisible=False,
                          parent=current_parent)
    form = pm.formLayout()
    # Creating Components
    asset_image = pm.button(width=48, height=48)
    asset_text = pm.text(height=48, width=125,
                label='streetLight1')
    asset_low = pm.button(height=32)
    asset_med = pm.button(height=32)
    asset_high = pm.button(height=32)
    
    # Positioning Components.
    # Symbol Button
    form.attachForm(asset_image, 'top', 5)
    form.attachForm(asset_image, 'left', 5)
    
    # asset text
    form.attachForm(asset_text, 'top', 5)
    form.attachForm(asset_low, 'top', 15)
    form.attachForm(asset_med, 'top', 15)
    form.attachForm(asset_high, 'top', 15)
    
    
    form.attachControl(asset_text, 'left', 5, asset_image)
    # form.attachControl(asset_text, 'right', 5, asset_low)

    form.attachControl(asset_low, 'left', 5, asset_text)
    form.attachControl(asset_med, 'left', 5, asset_low)
    form.attachControl(asset_high, 'left', 5, asset_med)

    form.attachForm(asset_high, 'right', 5)
    form.attachForm(asset_image, 'bottom', 5)

    # res buttons
    
    
    # Return parent to orginal layout
    pm.setParent(current_parent)
    
    return main
    
    
    