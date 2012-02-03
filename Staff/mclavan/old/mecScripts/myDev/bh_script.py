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
