'''

Author:
    Firmin Saint-Amour
    
Description:
    Shading and Lighting quiz grading script

'''

try:
    import cPickle as pickle
except:
    import pickle
    
import pymel.core as pm
import os
import glob


def gui():
    win = 'quiz_grading'
    if pm.window(win, exists= True):
        pm.deleteUI(win)
        
    if pm.windowPref(win, exists= True):
        pm.windowPref(win, remove= True)
        
    global scroll_field, scroll_list
    my_win = pm.window(win, title= 'Quiz Grading', toolbox= True,
                       width= 600, height= 400)
    
    main_layout = pm.rowColumnLayout(numberOfColumns= 2,
                                     columnWidth= ([1, 200], [2, 400]))
    
    pm.columnLayout()
    pm.text(label= 'Quizzes')
    scroll_list = pm.textScrollList(width= 200, height= 400,
                      selectCommand= pm.Callback(read_quiz))
    
    pm.setParent(main_layout)
    pm.columnLayout()
    pm.text(label= 'Result')
    scroll_field = pm.scrollField(wordWrap= True, height= 400, width= 400)
    
    list_quizzes()
    
    my_win.show()
    
def read_quiz():
    file_name = scroll_list.getSelectItem()[0] + '.quiz'
    dir_path = os.path.dirname(__file__)
    full_path = os.path.join(dir_path, 'To_Grade', file_name)
    f = open(full_path, 'r')
    info = pickle.load(f)
    f.close()
    scroll_field.clear()
    for data in info:
        for d in data:
            if d == data[2]:
                scroll_field.insertText('  -'+d+'\n'+
                                        '------------------------\n')
            else:
                scroll_field.insertText(d)
                
        
    
def list_quizzes():
    dir_path = os.path.dirname(__file__)
    full_path = os.path.join(dir_path, 'To_Grade', '*.quiz')
    quizzes = glob.glob(full_path)
    scroll_list.removeAll()
    for quiz in quizzes:
        quiz_basename = os.path.basename(quiz)
        quiz_name = quiz_basename.split('.')[0]
        
        scroll_list.append(quiz_name)
        
        