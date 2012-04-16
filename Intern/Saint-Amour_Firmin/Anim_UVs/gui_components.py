'''
module of ui components for Anim UV Tool

'''

import pymel.core as pm


class Time_int():
    def __init__(self, index, node):
        self.node = node
        self.index = index
        
    def create(self):
        current_time = pm.keyframe( '%s' % (self.node) , query=True, index= (self.index, self.index), timeChange= True )[0]
        self.int_field = pm.intField(value= int(current_time), changeCommand= pm.Callback(self.change_time))
        
    def change_time(self):
        pm.keyframe('%s' % (self.node), option='over', index=(int(self.index), int(self.index)), absolute= True, timeChange=int(self.int_field.getValue()))

class Value_int():
    def __init__(self, index, node):
        self.node = node
        self.index = index
        
    def create(self):
        current_time = pm.keyframe( '%s' % (self.node) , query=True, index= (self.index, self.index), valueChange= True )[0]
        self.int_field = pm.floatField(value= int(current_time), changeCommand= pm.Callback(self.change_value))
        
    def change_value(self):
        pm.keyframe('%s' % (self.node), option='over', index=(int(self.index), int(self.index)), absolute= True, valueChange=float(self.int_field.getValue()))
        
        
class In_Tangent():
    def __init__(self, index, node):
        self.node = node
        self.index = index
        
    def create(self):
        current_type = pm.keyTangent( '%s' % (self.node) , query=True, index= (self.index, self.index), inTangentType= True )[0]
        self.text_field = pm.textField(text= '%s' % (current_type), enterCommand= pm.Callback(self.change_type))
        
    def change_type(self):
        pm.keyTangent('%s' % (self.node), index= (self.index, self.index), inTangentType= '%s' % (self.text_field.getText()))
        

class Out_Tangent():
    def __init__(self, index, node):
        self.node = node
        self.index = index
        
    def create(self):
        current_type = pm.keyTangent( '%s' % (self.node) , query=True, index= (self.index, self.index), outTangentType= True )[0]
        self.text_field = pm.textField(text= '%s' % (current_type), enterCommand= pm.Callback(self.change_type))
        
    def change_type(self):
        pm.keyTangent('%s' % (self.node), index= (self.index, self.index), outTangentType= '%s' % (self.text_field.getText()))
       
        
        