'''
Lecture 5 - Logic

Description:
    Lecture 5 main focus is learning how to do different logic techniques such as
        if statments and loops to build better tools
    Students will learn how to use if statments to alter their tools depending upon a users actions.
    Students will also learn how to use loops along with functions to automate tasks.
    The overall point of this lecture is to learn how to make their scripts more robust and save time.
    
    Topics Convered:
        - IF statments
        - error handeling
        - loops
        - renaming
        - lock and hide

    What should I know after looking at this script?
        - You should be able to create different types of if statments.
        - The difference between = and ==.
        
        
    Questions you should ask yourself:
        - Is the else statement manditory, when creating an if statment?
        - What about when the elif statment is used?
        
'''


# IF Statments
# IF Statments are covered in more detain in the book (Chapter ? Mainly the entire chapter.)
if condition:
    print 'Condition True'
    
# Branching IF statment
# What if I can more than one path (True path, False path)
if condition:
    print 'Condition True'
else:
    print 'Condition False'
    
# Multiple branches
# Give as many branches as possible.
if condition:
    print 'Condition 1 True'
elif condition:
    print 'Condition 2 True'
else:
    print 'All Conditions false'
    
    
# Practical Applications:
# -----------------------------------------------------------------------------
# Picking an os
# -----------------------------------------------------------------------------

# Problem:
# I built three different interfaces for operating systems (osx, windows, and linux)
import pymel.core as pm

def gui_osx():
    print 'Run OSX Interface.'

def gui_win():
    print 'Run Windows Interface'
    
def gui_linux():
    print 'Run Linus Interface'
    
def gui_test():
    '''
    This function will run the function that has the correct interface
    for the desired interface.
    '''
    os_type = pm.about(os=True)
    
    if os_type == 'nt':
        gui_win()
    elif os_type == 'mac':
        gui_osx()
    else:
        gui_linux()
        
    # Question: Is the else statement really looking for the linux operation system?
    # What would happen if someone runs this script under a fouth operating system (solaris or irux)
    
# -----------------------------------------------------------------------------
# Making sure the user selects two object in maya
# -----------------------------------------------------------------------------
'''
Available Operators
<       less than   
>       greater than
<=      less than or equal to
>=      greater than or equal to
!=      not equal to
==      equal to
and     logical and
or      logical or
not     logical not
'''



# -----------------------------------------------------------------------------
# Deleting an existing window.
# Why?  Two windows cannot exists with the same name.
#   This will cause an error when trying to execute a script multiple times.
# Result:  Delete the window if it already exists.
# -----------------------------------------------------------------------------

# Deleting an interface.
# Interface must exist to use the command, or it will generate an error.
# pm.deleteUI('interface_name')

# Much check to see if the window exists first.

win_exists = pm.window(win_name, exists=True)
if win_exists:
    pm.deleteUI(win_name)



# -----------------------------------------------------------------------------
# Check to see if an attribute object exists
# -----------------------------------------------------------------------------

attribute_name = 'index_curl'
selected = pm.ls(sl=True)[0]
attr_exists = pm.attributeQuery(attr_name, node=selected[0], exists=True)


# -----------------------------------------------------------------------------
# Rename first and last item of a list.
# -----------------------------------------------------------------------------

selected = pm.ls(sl=True)
# len command returns how many items are inside of a list. (Chapter 4)
if len(selected) > 1:
    selected[0].rename('first')
    selected[-1].rename('last') # -1 index works from the end of the list. (Chapter 4)
    

# -----------------------------------------------------------------------------
# Converting Values
# radioButtonGrp example
# -----------------------------------------------------------------------------

 
  
# -----------------------------------------------------------------------------  
# Cool Stuff
# -----------------------------------------------------------------------------

# Running terminal commands
# This is normally done through the subprocess module in python (Google subprocess)
# Pymel has a built in version
import pymel.core as pm
import pymel.internal as pyi

os_type = pm.about(os=True)

if os_type == 'nt':
    # Windows
    output = pyi.shellOutput('dir')
else:
    # Linux or Mac
    output = pyi.shellOutput('ls')

# Prints out of the contents of the current directory your in.
print output

# Try this instead
# Open and image (Yes, this can be done with pretty much any file.)
os_type = pm.about(os=True)

# The r stands for raw, meaning ignore backslashes (Research escape sequences for the reason.)
image_path = r'C:\Users\mclavan\Desktop\png\Add48.png'
if os_type == 'nt':
    # Windows
    pyi.shellOutput(image_path)
else:
    # Linux or Mac
    pyi.shellOutput(image_path)
