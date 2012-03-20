'''
Lecture 4 - Data

Description:
    Lecture 4 consists of developing basic tools.
    Students will learn how to research and convert commands into python.
    Students will also learn how to break down complex system and replicate them in code.
    Topics Covered:
        - Variables
        - Lists
        - Maya Command Anatomy
        - Automating systems
        - Functions args and returns statment
'''

'''
Variables
Storing Data
'''

# = is an assignment operator (NOT equals)
# == is equals
win_name = 'toolset_win'
win_width = 200
win_height = 400

# Adding Variables
win_width = win_width + 100
print win_width # Results 300

# Adding Strings
# Podcast available (Book Chapter 2, google "python string concatination")
object = 'body_geo'
attr = 'ty'
print object + attr  # 'body_geoty'
print object + '.' + attr # 'body_geo.ty'

# Practical Example
def gui():
    win_name = 'toolset_win'
    win_width = 200
    win_height = 300
    
    win = pm.window(win_name, width=win_width, height=win_height)
    main = pm.columnLayout()
    pm.button(width=win_width, label='Button 1')
    pm.button(width=win_width, label='Button 1')
    pm.button(width=win_width, label='Button 1')
    win.show()
    

'''
Cool Stuff
'''