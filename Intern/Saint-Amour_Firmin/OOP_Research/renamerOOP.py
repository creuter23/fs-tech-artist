# # # # # # # # # # # #
#                     #
#  Firmin Saint-Amour #
#                     #
#  pymel renamer      #
#                     #
#  import renamerOOP  #
#  renamerOOP.gui()   #
#                     #
# # # # # # # # # # # #

from pymel.core import *

class Renamer(object):
    def __init__(self, objList=[]):
        self.objList=objList
    
    # replace  function takes what to search for and what to replace with   
    def replaceFunction(self, search, replace):
        i = 0
        while i != len(self.objList):
            newname = self.objList[i].replace('%s' % search,'%s' % replace)
            k = rename(self.objList[i], newname)
            
            i += 1
            
        return k
            
    
    # renames the object         
    def renameFunction(self, newname, counter, pad):
        x = '0'
        padding = x * pad
        end = padding + str(counter)
        
        i = 0
        while i != len(self.objList):
            
            k = rename(self.objList[i], '%s' % newname+str(end))
            
            i += 1
            counter += 1 
            
        return k
    
    # adds a suffix    
    def suffixFunction(self, suffix):
        i = 0
        while i != len(self.objList):
            k = rename(self.objList[i], '%s' % self.objList[i]+suffix )
            
            i += 1
            
        return k
            
    
    # adds a prefix
    def prefixFunction(self, prefix):
        i = 0
        while i != len(self.objList):
            k = rename(self.objList[i], '%s' % prefix+self.objList[i])
            
            i += 1
            
        return k
            

# the name of the window
win = 'renamerWindow'

def gui():
    
    global renameField, searchField, replaceField, prefixField, suffixField, counterSlider, padSlider

    if(window(win, ex = True)):
        deleteUI(win)
        
    if(windowPref(win, ex = True)):
        windowPref(win, remove = True)
        
    window(win, title = 'renamer', sizeable = False, mnb = True, width = 150, backgroundColor = [.5, .5, .5])
    # window layout
    mainLayout = columnLayout(adjustableColumn = True)
    
    text(label = 'select objects ')
    
    separator(style = 'in', height = 15)
    
    renameField = textField(text = 'newname')
    text(label = 'startNumber')
    counterSlider = intSliderGrp(min = 0, max = 250, field = True)
    text(label = 'pad')
    padSlider = intSliderGrp(min = 0, max = 10, field = True)
    button(label = 'rename', command = renameFunction)
    
    separator(style = 'in', height = 15)
    
    text(label = 'type suffix below')
    separator(style = 'in', height = 5)
    suffixField = textField(text = 'Suffix')
    separator(style = 'in', height = 5)
    button(label = 'addSuffix', command = suffixFunction)

    separator(style = 'in', height = 15)
    
    text(label = 'type prefix below')
    separator(style = 'in', height = 5)
    prefixField = textField(text = 'prefix')
    separator(style = 'in', height = 5)
    button(label = 'addPrefix', command = prefixFunction)
    
    separator(style = 'in', height = 15)
    
    text(label = 'type in fields below')
    separator(style = 'in', height = 5)
    searchField = textField(text = 'search')
    separator(style = 'in', height = 5)
    replaceField = textField(text = 'replace')
    separator(style = 'in', height = 5)
    button(label = 'replace', command = replaceFunction)
    
    showWindow()
    
def renameFunction(*args):
    # listing objects
    myList = ls(sl = True)
    # instancing Renamer object
    rename = Renamer(myList)
    # invoking Renamer.renameFunction method
    rename.renameFunction( renameField.getText(), counterSlider.getValue(), padSlider.getValue())

def suffixFunction(*args):
    # listing objects
    myList = ls(selection = True)
    # instancing Renamer object
    suffix = Renamer(myList)
    # invoking Renamer.suffixFunction method
    suffix.suffixFunction(suffixField.getText())
    
def prefixFunction(*args):
    # listing objects
    myList = ls(selection = True)
    # instancing Renamer object
    prefix = Renamer(myList)
    # invoking Renamer.prefixFunction method
    prefix.prefixFunction(prefixField.getText())
    
def replaceFunction(*args):
    # listing objects
    myList = ls(selection = True)
    # instancing Renamer object
    replace = Renamer(myList)
    # invoking Renamer.replaceFunction method
    replace.replaceFunction(searchField.getText(), replaceField.getText())
    
    

    
