'''

Author:
    Firmin Saint-Amour
    
Description:
    Shading and Lighting quiz grading script

'''
from __future__ import division
try:
    import cPickle as pickle
except:
    import pickle
    
import pymel.core as pm
import os
import glob


def gui():
    
    dir_name = os.path.dirname(__file__)
    file_path = os.path.join(dir_name, 'Startup', 'grade.path')
    f = open(file_path, 'r')
    pickle_data = pickle.load(f)
    f.close()
    
    
    win = 'quiz_grading'
    if pm.window(win, exists= True):
        pm.deleteUI(win)
        
    if pm.windowPref(win, exists= True):
        pm.windowPref(win, remove= True)
        
    global scroll_field, scroll_list, path_field, open_check_box
    my_win = pm.window(win, title= 'Quiz Grading', toolbox= True,
                       width= 600, height= 400)
    god_layout = pm.columnLayout()
    pm.text(label= '')
    path_field = pm.textFieldButtonGrp(label= 'Ouput Path', 
                buttonCommand= pm.Callback(get_path), buttonLabel= '<<<',
                text= pickle_data, columnWidth3= [100, 400, 100])
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
    pm.setParent(god_layout)
    pm.rowColumnLayout(numberOfColumns= 2,
                                     columnWidth= ([1, 200], [2, 400]))
    open_check_box = pm.checkBox(label= 'Open File When Done', value= 1)
    pm.button(label= 'Ouput To Text File', command= pm.Callback(ouput_to_text), 
        height= 35)
    list_quizzes()
    
    my_win.show()

def ouput_to_text():
    open_file = open_check_box.getValue()
    text_to_ouput = scroll_field.getText()
    student_name = scroll_list.getSelectItem()[0]
    path = path_field.getText()
    file_path = os.path.join(path, '%s.txt' % (student_name))
    text_file = open(file_path, 'w')
    text_file.write(text_to_ouput)
    text_file.close()
    if open_file == True:
        pm.util.shellOutput(r"open  %s " % (file_path))

def get_path():
        path = pm.fileDialog2(fileMode= 3)[0]
        path_field.setText(path)
        dir_name = os.path.dirname(__file__)
        file_path = os.path.join(dir_name, 'Startup', 'grade.path')
        f = open(file_path, 'w')
        pickle_data = pickle.dump(path, f)
        f.close()

def read_quiz():
    '''
    amount = len(output)
        percentage = amount / 100
        right = 0
        for data in output:
            if 'Correct' in data[-1]:
                right += 1
        dialogCheck=pm.confirmDialog( title='RESULTS',
                        message='You got %s right out of %s\n' % (right, amount)
                        + 'Final score %s' % float((float(right / amount))* 100))
    '''
    student_name = scroll_list.getSelectItem()[0]
    file_name = scroll_list.getSelectItem()[0] + '.quiz'
    dir_path = os.path.dirname(__file__)
    full_path = os.path.join(dir_path, 'To_Grade', file_name)
    f = open(full_path, 'r')
    info = pickle.load(f)
    f.close()
    scroll_field.clear()
    right = 0
    amount = len(info)
    percentage = amount / 100

    scroll_field.insertText('Student Name: %s\n\n------------------------\n'
                             % (student_name))
    for data in info:
        for d in data:
            if 'Correct' in d:
                right += 1

            if d == data[2]:
                scroll_field.insertText('  -'+d+'\n'+
                                        '------------------------\n')
            else:
                scroll_field.insertText(d)
    final_score = float((float(right / amount))* 100)
    scroll_field.insertText('Got %s right of %s\n' % (right, amount))
    scroll_field.insertText('Final Score: %s' % (final_score))
    
                
        
    
def list_quizzes():
    dir_path = os.path.dirname(__file__)
    full_path = os.path.join(dir_path, 'To_Grade', '*.quiz')
    quizzes = glob.glob(full_path)
    scroll_list.removeAll()
    for quiz in quizzes:
        quiz_basename = os.path.basename(quiz)
        quiz_name = quiz_basename.split('.')[0]
        
        scroll_list.append(quiz_name)
        
        