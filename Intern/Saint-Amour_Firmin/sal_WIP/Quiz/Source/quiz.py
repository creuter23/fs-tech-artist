'''

Author:
    Firmin Saint-Amour
    
Description:
    Shading and Lighting quiz script

'''
from __future__ import division
import random
import os
import pymel.core as pm
try:
    import cPickle as pickle
except:
    import pickle

class Radio_Button(object):
    def __init__(self, button_info):
        info = button_info.split('==')
        self.label = info[0]
        self.state = info[1]
        self.radio_button = pm.radioButton(label= self.label)
        
    def get_state(self):
        return self.state
    
    def get_radio_button(self):
        output = self.radio_button.split('|')[-1]
        
        return output
    
    def get_label(self):
        return self.label
    
class Icon_Radio_Button(object):
    def __init__(self, button_info):
        info = button_info.split('==')
        dir_path = os.path.dirname(__file__)
        self.label = info[0]
        self.image = os.path.join(dir_path, 'Images', info[1])
        
        #print self.image
        self.state = info[2]
        self.radio_button = pm.iconTextRadioButton(style='iconOnly',
                                                   image= self.image)

        
    def get_state(self):
        return self.state
    
    def get_radio_button(self):
        output = self.radio_button.split('|')[-1]
        
        return output
    
    def get_label(self):
        return self.label
        
class Question(object):
    def __init__(self, info, parent):
        self.radio_objects = []
        self.question = info[0]
        self.radio_buttons = info[1:5]
        
        random.shuffle(self.radio_buttons)
        pm.setParent(parent)
        self.layout = pm.columnLayout(adjustableColumn= True)
        pm.scrollField(wordWrap= True, width= 400, text= self.question,
                          height= 75)
        #pm.text(label= self.question, align= 'left')
        self.radioCollection = pm.radioCollection()
        
        for radio_button in self.radio_buttons:
            obj = Radio_Button(radio_button)
            self.radio_objects.append(obj)
            
            
    def get_selected_radio_button(self):
        output = []
        selected = self.radioCollection.getSelect()
        for radio_button in self.radio_objects:
            button = radio_button.get_radio_button()
            if button == selected:
                label = radio_button.get_label()
                state = radio_button.get_state()
                output.append(label)
                output.append(state)
        return output
    
    def get_info(self):
        output = [self.question]
        selected = self.radioCollection.getSelect()
        for radio_button in self.radio_objects:
            button = radio_button.get_radio_button()
            if button == selected:
                label = radio_button.get_label()
                state = radio_button.get_state()
                output.append(label)
                output.append(state)
        return output
    
class Icon_Question(Question):
    def __init__(self, info, parent):
        self.radio_objects = []
        self.question = info[0]
        self.radio_buttons = info[1:5]
        
        random.shuffle(self.radio_buttons)
        pm.setParent(parent)
        self.layout = pm.columnLayout(adjustableColumn= True)
        pm.scrollField(wordWrap= True, width= 400, text= self.question,
                          height= 75)
        #pm.text(label= self.question, align= 'left')
        self.radioCollection = pm.iconTextRadioCollection()
        
        for radio_button in self.radio_buttons:
            obj = Icon_Radio_Button(radio_button)
            self.radio_objects.append(obj)
    
class Quiz(object):
    def __init__(self, questions_list):
        self.path = None
        self.question_instances = []
        self.questions = []
        self.icon_question_info = []
        self.question_info = []
        self.file_info = []
        random_amount = questions_list[0]
        core_questions = questions_list[1]
        random_questions = questions_list[2]
        for core in core_questions:
            self.questions.append(core)
        random.shuffle(random_questions)
        random.shuffle(random_questions)
        random_copy = random_questions[0:random_amount]
        for r in random_copy:
            self.questions.append(r)

        random.shuffle(self.questions)

        for question in self.questions:
            try:
                temp = question[1].split('==')
                print temp[2]
                self.icon_question_info.append(question)
            except:
                self.question_info.append(question)
           
        random.shuffle(self.question_info)
        random.shuffle(self.icon_question_info)
        
        self.create_questions()
        
    def get_path(self):
        self.path = pm.fileDialog2(fileMode= 3)[0]
        self.path_field.setText(self.path)
        

    def create_questions(self):
        self.layout = pm.columnLayout(adjustableColumn= True)
        self.path_field = pm.textFieldButtonGrp(label= 'Quiz Path', 
                buttonCommand= pm.Callback(self.get_path), buttonLabel= '<<<',
                text= '/Users/', columnWidth3= [100, 200, 100])
        self.name_field = pm.textFieldGrp(label= 'Name', 
            columnWidth2= [100,200], text= 'Student_Name')
        
        for info in  self.icon_question_info:
            #print info
            obj = Icon_Question(info, self.layout)
            self.question_instances.append(obj)
                
        for info in  self.question_info:
            obj = Question(info, self.layout)
            self.question_instances.append(obj)
        
    def get_info(self):
        output = []
        right = 0
        amount = len(self.questions)-1
        
        for question in self.question_instances:
            output.append(question.get_info())
            
        new_path = self.path_field.getText()
        file_name = self.name_field.getText() + '.quiz'
        full_path = os.path.join(new_path, file_name)
        
        
        f = open(full_path, 'w')
        pickle_data = pickle.dump(output, f)
        f.close()
        return output
    
def gui():
    
    file_path = os.path.dirname(__file__)
    basename = os.path.basename(file_path)
    file_name = '%s.questions' % (basename)
    #print file_name, basename, file_path
    questions_file = os.path.join(file_path, file_name)
    #print questions_file
    f = open(questions_file, 'r')
    info = pickle.load(f)
    f.close()
    win = 'quiz_win'
    if pm.window(win, exists= True):
        pm.deleteUI(win)
        
    if pm.windowPref(win, exists= True):
        pm.windowPref(win, remove= True)
        
    global quiz
    my_win = pm.window(win, title= basename, toolbox= True,
                       width= 400, height= 600)
    
    pm.scrollLayout()
    
    quiz = Quiz(info)
    
    
    
    pm.button(label= 'Done', height= 35, command= pm.Callback(check))
    
    my_win.show()
    
def get_result():
    #print quiz
    output = quiz.get_info()
    return output
    
def check():
    dialogCheck=pm.confirmDialog( title='Are you sure?',
                                 message='do you want to double check',
                                 button=['Yes',"I'm done"],
                                 defaultButton='Yes', cancelButton= "I'm done",
                                 dismissString="I'm done" )
    if dialogCheck == 'Yes':
            pass
    else:
        output = get_result()
        amount = len(output)
        percentage = amount / 100
        right = 0
        for data in output:
            if 'Correct' in data[-1]:
                right += 1
        dialogCheck=pm.confirmDialog( title='RESULTS',
                        message='You got %s right out of %s\n' % (right, amount)
                        + 'Final score %s' % float((float(right / amount))* 100))
    
    
    
    
    
    
    