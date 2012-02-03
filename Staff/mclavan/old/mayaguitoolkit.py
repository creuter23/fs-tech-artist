#!/usr/bin/env python
#---------------------------------------------------------------------------------
#HEADER_START --------------------------------------------------------------------

#PUBLISHTO /data/film/apps/reelfx/maya/python/
#SETMODE 777

"""
NAME: mayaguitoolkit.py

AUTHOR: Justin Barrett

CATEGORY: General

SYNOPSIS: GUI helper classes.  Makes Maya GUI design and management in Python
        a little easier...I hope.

OPTIONS:

RETURN VALUE:

EXAMPLES:

NOTES:

BUG HISTORY:

REVISIONS:
    2008-10-xx  JBarrett    2.0     Initial release
    2009-01-09  JBarrett    1.1     added "getSelected" for RadioCollection
                                    RadioButton can take an instance as a radio collection
    2009-01-21  JBarrett    1.2     added instance support for IconTextRadioButton
                                        and menu items that are radio buttons
                                    added "getSelected" for IconTextRadioCollection and
                                        RadioMenuItemCollection
    2009-05-08  JBarrett    1.3     added instance support for "tabLabel" flag on TabLayout
                                    added "whichKey" function
    2009-05-11  JBarrett    1.4     added "replaceIndex" method to TextScrollList
    2009-05-27  JBarrett    1.5     added preset feature to ConfirmDialog

TO DO'S:

"""
#HEADER_END ----------------------------------------------------------------------

#---------------------------------------------------------------------------------#
# imports
#---------------------------------------------------------------------------------#
import maya.cmds as mc
import maya.mel as mm
import new

import os
import types

#---------------------------------------------------------------------------------#
# constants
#---------------------------------------------------------------------------------#

MAIN_MAYA_WINDOW = mm.eval("global string $gMainWindow;$tmpWin = $gMainWindow;")

#---------------------------------------------------------------------------------#
# public functions
#---------------------------------------------------------------------------------#

def error(message, confirm=True):
    if confirm:
        ConfirmDialog(p=MAIN_MAYA_WINDOW, title="RFX Error", message=message)
    raise Exception(message)
  
def warning(message, confirm=True):
    if confirm:
        ConfirmDialog(p=MAIN_MAYA_WINDOW, title="RFX Warning", message=message)
    if '"' in message:
        message = message.replace('"', '\\"')
    if "'" in message:
        message = message.replace("'", "\\'")
    mm.eval('warning("%s")' % message)

def confirm_yn(title="Confirm", message="Are you sure?"):
    # Creates simple Yes/No prompt; returns True or False based on result
    prompt = ConfirmDialog(t=title, m=message, button=["Yes","No"], defaultButton="Yes", cancelButton="No", dismissString="No")
    if prompt.result == "Yes":
        return True
    return False

def whichKey(kwds, keyList):
    for key in keyList:
        if key in kwds:
            return key
    return ""
    
#---------------------------------------------------------------------------------#
# private functions
#---------------------------------------------------------------------------------#

def _splitArgs(kwds):
    parts = []
    func = {}
    for (k,v) in kwds.iteritems():
        if type(v) in types.StringTypes:
            if "'" in str(v):
                v = v.replace("'", "\\'")
            parts.append("%s='%s'" % (k,str(v)))
        elif type(v) in [types.MethodType, types.FunctionType]:
            func[k] = v
        else:
            parts.append("%s=%s" % (k,str(v)))
    final = ",".join(parts)
    return final,func

def _swapOutObjs(options):
    if len(options) < 1:
        return options
    def doSwap(item):
        if isinstance(item, GuiElement):
            return repr(item)
        else:
            return item
    multiParse = False
    if type(options[0]) is types.ListType or type(options[0]) is types.TupleType:
        multiParse = True
    if multiParse:
        newList = []
        for option in options:
            _swapOutObjs(option)
            newList.append(option)
        return newList
    else:
        newList = []
        for option in options:
            newList.append(doSwap(option))
        return newList


#---------------------------------------------------------------------------------#
# GuiElement (parent of all other GUI classes)
#---------------------------------------------------------------------------------#

class GuiElement(object):
    """
    Parent class for all Maya GUI classes
    
    This class contains an instance attribute named "reservedAtts", which is a list
    of reserved attributes that are checked when any attribute is set.  Subclasses
    that add custom instance attributes will need to create this same attribute, and
    the default items will be appended upon creation.
    """
    def __init__(self, *args, **kwds):
        nm = self.__class__.__name__
        self.mayacommand = "mc." + nm[0].lower() + nm[1:]
        name = ""
        if args:
            name = "'%s'," % args[0]
        parent = ""
        addKill = False
        if "onKill" in kwds:
            killCmd = kwds.pop("onKill")
            addKill = True
        x = whichKey(kwds, ["p","parent"])
        if x:
            p = kwds.pop(x)
            if isinstance(p, GuiElement):
                p = repr(p)
            parent = "p='%s'," % p
        kw, func = _splitArgs(kwds)
        kw = name + parent + kw
        if len(kwds) == 0 and args != () and eval("%s('%s',ex=True)" % (self.mayacommand, args[0])):
            self.mayaname = args[0]
        else:
            if "\n" in kw:
                kw = kw.replace("\n", "\\n")
            if "\t" in kw:
                kw = kw.replace("\t", "\\t")
            self.mayaname = eval("%s(%s)" % (self.mayacommand, kw))
        if len(func):
            for (k,v) in func.iteritems():
                #print '%s(self.mayaname,e=True,%s=v)' % (self.mayacommand,k)
                eval('%s(self.mayaname, e=True, %s=v)' % (self.mayacommand,k))
        if addKill:
            sj = mm.eval('scriptJob -uid %s %s;' % (self.mayaname, killCmd))
            
    def __getattr__(self,name):
        try:
            return eval("%s(self.mayaname, q=True, %s=True)" % (self.mayacommand,name))
        except TypeError:
            if not "altcommand" in self.__dict__:
                print "No alt command specified for %s" % self.mayacommand
            else:
                return eval("%s(self.mayaname, q=True, %s=True)" % (self.altcommand,name))
    
    def __setattr__(self,name,value):
        # if name is "args", parse value (dictionary) and set each one appropriately
        if name == "args":
            for item in value:
                exec("self.%s=value[item]" % item)
            return
        # if value is an instance, replace it with the UI element's name
        if isinstance(value, GuiElement):
            value = repr(value)
        # if value is a list or tuple, replace all instances with the UI element's name
        if type(value) is types.ListType or type(value) is types.TupleType:
            value = _swapOutObjs(value)
        if name in ["mayaname","mayacommand","altcommand","customData"]:
            object.__setattr__(self, name, value)
        else:
            #print "name,value:",name,value
            try:
                eval("%s(self.mayaname, e=True, %s=value)" % (self.mayacommand, name))
            except TypeError:
                if not "altcommand" in self.__dict__:
                    print "Unknown argument: '%s'.  No alt command specified for %s" % (name, self.mayacommand)
                else:
                    eval("%s(self.mayaname, e=True, %s=value)" % (self.altcommand, name))
            
    
    def __getitem__(self, key):
        return eval("%s(self.mayaname, q=True, %s=True)" % (self.mayacommand, key))
    
    def __setitem__(self, key, value):
        if type(value) in types.StringTypes:
            eval("%s(self.mayaname, e=True, %s='%s')" % (self.mayacommand, key, value))
        elif type(value) in [types.MethodType, types.FunctionType]:
            eval("%s(self.mayaname, e=True, %s=value)" % (self.mayacommand, key))
        else:
            eval("%s(self.mayaname, e=True, %s=value)" % (self.mayacommand, key))
    
    def __call__(self, **kwds):
        args, func = _splitArgs(kwds)
        eval("%s(self.mayaname, e=True, %s)" % (self.mayacommand,args))
        if len(func):
            for (k,v) in func.iteritems():
                eval('%s(self.mayaname, e=True, %s=v)' % (self.mayacommand,k))
    
    def __repr__(self):
        return self.mayaname
    
    def delete(self, name=None):
        #print self.mayaname
        mc.deleteUI(self.mayaname)
        if name:
            try:
                mc.deleteUI(name)
            except RuntimeError:
                raise Exception("UI element not found: %s" % name)
    
    def setFocus(self):
        "Set focus to maya control/panel"
        mc.setFocus(self.mayaname)
        
      

#---------------------------------------------------------------------------------#
# Windows
#---------------------------------------------------------------------------------#

# make generic classes that will *not* receive custom updates
class ColorEditor(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class CreateEditor(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class DefaultNavigation(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class Editor(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class EditorTemplate(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class FontDialog(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class LayoutDialog(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class MinimizeApp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ScriptEditorInfo(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ShowSelectionInTitle(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ShowWindow(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ToggleWindowVisibility(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class WindowPref(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

# classes below have custom updates to add functionality

class ConfirmDialog(object):
    def __init__(self, *args, **kwds):
        self.result = mc.confirmDialog(*args, **kwds)


class PromptDialog(object):
    def __init__(self, *args, **kwds):
        self.result = mc.promptDialog(*args, **kwds)
    
    def __getattr__(self, name):
        if name == "tx" or name == "text":
            return mc.promptDialog(q=True, tx=True)


class Window(GuiElement):
    def __init__(self, *args, **kwds):
        if "force" in kwds:
            force = kwds.pop("force")
            if force:
                if args != ():
                    if mc.window(args[0],ex=True):
                        mc.deleteUI(args[0])
        GuiElement.__init__(self, *args, **kwds)

    def show(self):
        mc.showWindow(self.mayaname)
    
    def exists(self, name=None):
        if name is not None:
            # delete the default window made when calling the class,
            # then return the existence of the specified window name
            mc.deleteUI(self.mayaname)
            return bool(mc.window(name,exists=True))
        else:
            return bool(mc.window(self.mayaname,exists=True))
        
    def ex(self, name=None):
        return self.exists(name)
    

class ProgressWindow(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)
    
    def endProgress(self):
        mc.progressWindow(ep=True)
    
    def ep(self):
        self.endProgress()

#---------------------------------------------------------------------------------#
# Panels
#---------------------------------------------------------------------------------#

# make generic classes that will *not* receive custom updates
class ComponentEditor(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class GetPanel(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class HardwareRenderPanel(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class HyperGraph(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class HyperPanel(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class HyperShade(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ModelEditor(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ModelPanel(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class NewPanelItems(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class NodeOutliner(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class OutlinerEditor(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class OutlinerPanel(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class Panel(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class PanelConfiguration(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class PanelHistory(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ScriptedPanel(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ScriptedPanelType(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class SetEditor(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class SetFocus(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class SpreadSheetEditor(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ViewManip(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class Visor(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class WebBrowser(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class WebBrowserPrefs(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)



# classes below have custom updates to add functionality

#---------------------------------------------------------------------------------#
# Controls
#---------------------------------------------------------------------------------#

# make generic classes that will *not* receive custom updates
class AttrColorSliderGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class AttrControlGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class AttrFieldGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class AttrFieldSliderGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class AttrNavigationControlGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class Button(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class Canvas(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ChannelBox(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class CheckBox(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class CheckBoxGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class CmdScrollFieldExecuter(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class CmdScrollFieldReporter(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class CmdShell(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ColorIndexSliderGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ColorSliderButtonGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ColorSliderGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class CommandLine(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class Control(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class FloatField(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class FloatFieldGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class FloatScrollBar(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class FloatSlider(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class FloatSlider2(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class FloatSliderButtonGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class FloatSliderGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class GradientControl(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class GradientControlNoAttr(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class HelpLine(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class HudButton(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class HudSlider(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class HudSliderButton(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class IconTextButton(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class IconTextCheckBox(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class IconTextRadioButton(GuiElement):
    def __init__(self, *args, **kwds):
        if "cl" in kwds or "collection" in kwds:
            try:
                collection = kwds.pop("cl")
            except KeyError:
                collection = kwds.pop("collection")
            # if it's not a string of some kind, we can pretty much assume
            # that it's an instance of an object from this module
            if type(collection) not in types.StringTypes:
                kwds["collection"] = repr(collection)
                collection.addRadioButton(self)
        GuiElement.__init__(self, *args, **kwds)

class IconTextRadioCollection(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)
        self.customData = []
    
    def addRadioButton(self, radioButtonObj):
        self.customData.append(radioButtonObj)
        
    def getSelected(self):
        name = str(self.select)
        if len(self.customData) == 0:
            return name
        found = None
        for b in self.customData:
            newname = str(repr(b))
            if newname == name or newname.endswith(name):
                found = b
        return found

class IconTextScrollList(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class IconTextStaticLabel(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class Image(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class IntField(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class IntFieldGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class IntScrollBar(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class IntSlider(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class IntSliderGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class LayerButton(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class MessageLine(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class NameField(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class PalettePort(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class Picture(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ProgressBar(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class RadioButton(GuiElement):
    def __init__(self, *args, **kwds):
        clFlag = whichKey(kwds, ["cl", "collection"])
        if clFlag:
            # if it's not a string of some kind, we can pretty much assume
            # that it's an instance of an object from this module
            if type(kwds[clFlag]) not in types.StringTypes:
                collection = kwds.pop(clFlag)
                kwds["collection"] = repr(collection)
                collection.addRadioButton(self)
        GuiElement.__init__(self, *args, **kwds)

class RadioButtonGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class RadioCollection(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)
        self.customData = []
    
    def addRadioButton(self, radioButtonObj):
        self.customData.append(radioButtonObj)
        
    def getSelected(self):
        name = str(self.select)
        if len(self.customData) == 0:
            return name
        found = None
        for b in self.customData:
            newname = str(repr(b))
            if newname == name or newname.endswith(name):
                found = b
        return found

class RangeControl(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ScriptTable(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ScrollField(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class Separator(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ShelfButton(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ShellField(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class SoundControl(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class SwatchDisplayPort(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class SwitchTable(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class SymbolButton(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class SymbolCheckBox(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class Text(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class TextField(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class TextFieldButtonGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class TextFieldGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class TimeControl(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class TimePort(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ToolButton(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ToolCollection(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)


# classes below have custom updates to add functionality

class TextScrollList(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

    def append(self, item):
        self.a = item
        
    def appendList(self, items, sort=False):
        [self.append(item) for item in items]
        if sort:
            allitems = self.allItems
            if allitems is not None:
                allitems.sort()
                self.ra = True
                self.appendList(allitems)
    
    def move(self,direction):
        def moveItems(*args):
            orderDiff = []
            names = self.selectItem
            if not names:
                return
            numItems = self.numberOfItems
            self.deselectAll = True
            if direction == 1:
                names.reverse()
            firstname = names[0]
            for name in names:
                self.si = name
                index = self.selectIndexedItem[0]
                newIndex = index + direction
                if newIndex < 1 and name == firstname:
                    break
                if newIndex > 0 and newIndex <= numItems:
                    self.removeIndexedItem = index
                    self.appendPosition = [newIndex,name]
                    orderDiff.append([index,newIndex])
            self.deselectAll = True
            [self.select(item) for item in names]
            return orderDiff
        return moveItems
    
    def extract(self):
        names = self.selectItem
        if not names:
            return []
        else:
            [mc.textScrollList(self.mayaname, e=True, ri=name) for name in names]
            return names
    
    def replaceIndex(self, index, newData):
        "Replaces the indexed item (1-based index) with contents of newData"
        self.rii = index
        self.appendPosition = [index, newData]
        
    def select(self,item):
        self.selectItem = item
    
#---------------------------------------------------------------------------------#
# Layouts
#---------------------------------------------------------------------------------#

class ColumnLayout(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class FormLayout(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)
    
    def attachForm(self,options):
        """
        User may use default list format, or alternate dictionary format:
        
        form.attachForm({ctrl:"top left:0,bottom right:0"[,ctrl:"...",...]})
        
        where "ctrl" is either an instance of a Control class (Button, CheckBox, etc)
        or the full name of a control as a string
        """
        if type(options) is types.ListType or type(options) is types.TupleType:
            mc.formLayout(self.mayaname,e=True,af=_swapOutObjs(options))
        elif type(options) is types.DictionaryType:
            for (ctl,opts) in options.iteritems():
                name = ctl
                if type(ctl) is not type(""):
                    name = repr(ctl)
                for part in opts.split(","):
                    sides,offset = part.split(":")
                    for side in sides.split():
                        mc.formLayout(self.mayaname, e=True, af=[(name,side,int(offset))])
        else:
            raise TypeError,"Unknown type.  Expected <type 'dict'> or <type 'list'>, got " + repr(type(options))

    
    def af(self, options):
        """
        User may use default list format, or alternate dictionary format:
        
        form.af({ctrl:"top left:0,bottom right:0"[,ctrl:"...",...]})
        
        where "ctrl" is either an instance of a Control class (Button, CheckBox, etc)
        or the full name of a control as a string
        """
        self.attachForm(options)

    def attachOppositeForm(self,options):
        """
        User may use default list format, or alternate dictionary format:
        
        form.attachOppositeForm({ctrl:"top left:0,bottom right:0"[,ctrl:"...",...]})
        
        where "ctrl" is either an instance of a Control class (Button, CheckBox, etc)
        or the full name of a control as a string
        """
        if type(options) is types.ListType or type(options) is types.TupleType:
            mc.formLayout(self.mayaname, e=True, aof=_swapOutObjs(options))
        elif type(options) is types.DictionaryType:
            for (ctl,opts) in options.iteritems():
                name = ctl
                if type(ctl) is not type(""):
                    name = repr(ctl)
                for part in opts.split(","):
                    sides,offset = part.split(":")
                    for side in sides.split():
                        mc.formLayout(self.mayaname, e=True, aof=[(name,side,int(offset))])
        else:
            raise TypeError,"Unknown type.  Expected <type 'dict'> or <type 'list'>, got " + repr(type(options))

    
    def aof(self,options):
        """
        User may use default list format, or alternate dictionary format:
        
        form.af({ctrl:"top left:0,bottom right:0"[,ctrl:"...",...]})
        
        where "ctrl" is either an instance of a Control class (Button, CheckBox, etc)
        or the full name of a control as a string
        """
        self.attachOppositeForm(options)

    def attachControl(self,*options):
        """
        Augmented to allow GUI objects from this toolkit to be used in place of string names
        """
        for option in options:
            mc.formLayout(self.mayaname, e=True, ac=_swapOutObjs(list(option)))
    
    def ac(self,*options):
        """
        User may use default list format, or alternate dictionary format:
        
        form.ac({ctrl:"top left bottom right",...})
        
        where "ctrl" is either an instance of a Control class (Button, CheckBox, etc)
        or the full string name of a control
        """
        self.attachControl(*options)

    def attachOppositeControl(self,*options):
        """
        Augmented to allow GUI objects from this toolkit to be used in place of string names
        """
        for option in options:
            mc.formLayout(self.mayaname,e=True,aoc=_swapOutObjs(list(option)))
    
    def aoc(self,*options):
        """
        User may use default list format, or alternate dictionary format:
        
        form.ac({ctrl:"top left bottom right",...})
        
        where "ctrl" is either an instance of a Control class (Button, CheckBox, etc)
        or the full string name of a control
        """
        self.attachOppositeControl(*options)

    def attachNone(self,options):
        # form.attachControl({ctrl:"top left bottom right",...})
        # where "ctrl" is either an instance of a Control class (Button, CheckBox, etc)
        # or the full string name of a control
        if type(options) is not types.DictionaryType:
            raise TypeError("Expected <type 'dict'>, got " + repr(type(options)))
        for (ctl,opts) in options.iteritems():
            name = ctl
            if type(ctl) is not type(""):
                name = repr(ctl)
            for side in opts.split():
                mc.formLayout(self.mayaname, e=True, an=[(name,side)])
    
    def an(self,options):
        self.attachNone(options)

    def attachPosition(self,options):
        # form.attachPosition({ctrl:"left 5 10,right 5 90",...})
        # where "ctrl" is either an instance of a Control class (Button, CheckBox, etc)
        # or the full string name of a control
        if type(options) is not types.DictionaryType:
            raise TypeError,"Expected <type 'dict'>, got " + repr(type(options))
        for (ctl,opts) in options.iteritems():
            name = ctl
            if type(ctl) is not type(""):
                name = repr(ctl)
            for part in opts.split(","):
                side,offset,pos = part.split()
                mc.formLayout(self.mayaname, e=True, ap=[(name,side,int(offset),int(pos))])
    
    def ap(self,options):
        self.attachPosition(options)

class FrameLayout(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class GridLayout(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class Layout(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class MenuBarLayout(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class PaneLayout(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class RowColumnLayout(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class RowLayout(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ScrollLayout(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ShelfLayout(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class ShelfTabLayout(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class TabLayout(GuiElement):
    def __init__(self, *args, **kwds):
        tlFlag = whichKey(kwds, ["tl", "tabLabel"])
        if tlFlag:
            tabLabel = kwds[tlFlag]
            if isinstance(tabLabel[0], GuiElement):
                kwds.pop(tlFlag)
                kwds["tabLabel"] = [repr(tabLabel[0]), tabLabel[1]]
        GuiElement.__init__(self, *args, **kwds)

        

#---------------------------------------------------------------------------------#
# Menus
#---------------------------------------------------------------------------------#

class ArtBuildPaintMenu(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class AttrEnumOptionMenu(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class AttrEnumOptionMenuGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class AttributeMenu(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class HotBox(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class Menu(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class MenuEditor(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class MenuItem(GuiElement):
    def __init__(self, *args, **kwds):
        clFlag = whichKey(kwds, ["cl", "collection"])
        if clFlag:
            collection = kwds[clFlag]
            # if it's not a string of some kind, we can pretty much assume
            # that it's an instance of an object from this module
            if isinstance(collection, GuiElement):
                kwds.pop(clFlag)
                kwds["collection"] = repr(collection)
                collection.addRadioButton(self)
        pflag = whichKey(kwds, ["p", "parent"])
        if pflag:
            parent = kwds[pflag]
            if isinstance(parent, GuiElement):
                kwds.pop(pflag)
                kwds["parent"] = repr(parent)
                if "|optionMenuGrp" in repr(parent):
                    kwds["parent"] = repr(parent) + "|OptionMenu"
        GuiElement.__init__(self, *args, **kwds)
        if "sm" in kwds or "subMenu" in kwds:
            self.altcommand = "mc.menu"

class MenuSet(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class MenuSetPref(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class OptionMenu(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class OptionMenuGrp(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class PopupMenu(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)

class RadioMenuItemCollection(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)
        self.customData = []
    
    def addRadioButton(self, radioButtonObj):
        self.customData.append(radioButtonObj)
        
    def getSelected(self):
        found = None
        if len(self.customData) == 0:
            pass
        else:
            for menuItem in self.customData:
                if menuItem.rb:
                    found = menuItem
        return found

class SaveMenu(GuiElement):
    def __init__(self, *args, **kwds):
        GuiElement.__init__(self, *args, **kwds)
