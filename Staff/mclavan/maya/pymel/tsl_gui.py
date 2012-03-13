'''
#pymel #oop #textScrollList

Michael Clavan
tsl_gui.py

Description:

How To Run:


'''
import pymel.core as pm

class TSL():
    def __init__(self, cur_width=200, cur_height=300, items=[]):
        self.width = cur_width
        self.height = cur_height
        self.items = items
        self.tsl = pm.textScrollList(w=self.width, h=self.height, append=self.items)
        self.tsl_items = self.tsl.getAllItems()
        self.current_limit = ''
        
        
    def limit(self, item):
        import re
        self.tsl.removeAll()
        temp = []
        if item:
            self.current_limit = item
            pattern = '%s' % item
            for tsl_item in self.tsl_items:
                if re.search(pattern, tsl_item):
                    temp.append(tsl_item)
                    
            self.tsl.append(temp)
        else:
            self.tsl.append(self.tsl_items)
            
    def append(self, items=[]):
        self.tsl_items.extend(items)
        self.tsl.removeAll()
        for item in items:
            self.tsl.append(item)
        self.clear_filter()
        
    def clear_filter(self):
        self.tsl.removeAll()
        self.tsl.append(self.tsl_items)        
        if self.limit:
            self.limit(self.current_limit)
            
        

def gui():
    win = pm.window()
    main = pm.columnLayout()
    global tsl, filter_field, add_field
    tsl = TSL()
    pm.rowColumnLayout(nc=2, cw=[[1,125], [2,75]])
    add_field = pm.textField()
    pm.button(label='Add', c=pm.Callback(add_items))    
    filter_field = pm.textField(cc=pm.Callback(filter))
    pm.button(label='Clear', c=pm.Callback(tsl.limit,''))
    
    win.show()

def add_items():
    tsl.append([add_field.getText()])
    
def filter():
    tsl.limit(filter_field.getText())