'''

Author:
    Firmin Saint-Amour
    
Description:
    Shading and Lighting quiz maker script

'''
import shutil
import os
import pymel.core as pm
try:
    import cPickle as pickle
except:
    import pickle
    

class Error01(object):
    '''
    # creates a warning window
    # gets invokes when errors are incountered 
    '''
    def __init__(self):
        win = 'portal_pose_library_warning'
        if pm.window(win, exists= True):
            pm.deleteUI(win)
        
        if pm.windowPref(win, exists= True):
            pm.windowPref(win, remove= True)
        
        
        self.window = pm.window(win, title= 'Warning', width= 400, height= 300,
                       sizeable= False)
        pm.columnLayout(adjustableColumn= True)
        pm.text(label= 'ERROR', bgc= [1, 0, 0], align= 'center', height= 25)
        pm.text(label = 'ALREADY A CORE QUESTION',
                            align= 'center')
        pm.text(label = '')
        pm.button(label= 'CLOSE', command= pm.Callback(self.close))
        self.window.show()
    
    def close(self):
        pm.deleteUI(self.window)
        del self
class Error02(Error01):

    def __init__(self):
        win = 'portal_pose_library_warning'
        if pm.window(win, exists= True):
            pm.deleteUI(win)
        
        if pm.windowPref(win, exists= True):
            pm.windowPref(win, remove= True)
        
        
        self.window = pm.window(win, title= 'Warning', width= 400, height= 300,
                       sizeable= False)
        pm.columnLayout(adjustableColumn= True)
        pm.text(label= 'ERROR', bgc= [1, 0, 0], align= 'center', height= 25)
        pm.text(label = 'ALREADY A RANDOM QUESTION',
                            align= 'center')
        pm.text(label = '')
        pm.button(label= 'CLOSE', command= pm.Callback(self.close))
        self.window.show()

class Quiz_Maker(object):
    '''
    # .questions pattern [number of random questions, [core questions], 
                                            [random questions]]
    '''
    def __init__(self, questions_file):
        
        dir_name = os.path.dirname(__file__)
        file_path = os.path.join(dir_name, 'Startup', 'start.path')
        f = open(file_path, 'r')
        pickle_data = pickle.load(f)
        f.close()
        


        
        self.file = open(questions_file, 'r')
        self.questions = self.file.readlines()
        self.file.close()
        self.main_layout = pm.columnLayout()
        self.path_field = pm.textFieldButtonGrp(label= 'Quiz Path', 
                buttonCommand= pm.Callback(self.get_path), buttonLabel= '<<<',
                text= pickle_data)
        self.name_field = pm.textFieldGrp(label= 'Quiz Name', text= 'Lab01')
        self.layout = pm.rowColumnLayout(numberOfColumns= 2,
                                     columnWidth= ([1, 100], [2, 450]))
        pm.columnLayout()
        pm.text(label= 'Questions')
        self.question_scroll_list = pm.textScrollList(width= 95, height= 300,
                          selectCommand= pm.Callback(self.read_questions),
                          allowMultiSelection= True)
        
        pm.setParent(self.layout)
        pm.columnLayout()
        pm.text(label= 'Questions Info')
        self.question_scroll_field = pm.scrollField(wordWrap= True,
                                                    height= 300, width= 440)
        
        pm.setParent(self.main_layout)
        self.lower_layout = pm.rowColumnLayout(numberOfColumns= 3,
                                     columnWidth= ([1, 100], [2, 100], [3, 350]))
        pm.columnLayout()
        pm.text(label= 'Core')
        self.core_list = pm.textScrollList(width= 95, height= 300,
                          allowMultiSelection= True)
        pm.rowColumnLayout(numberOfColumns= 2)
                                     #columnWidth= ([1, 50], [2, 50]))
        pm.button(label= '+', width= 45, command= pm.Callback(self.add_core))
        pm.button(label= '-', width= 45, command= pm.Callback(self.remove_core))
        pm.setParent(self.lower_layout)
        pm.columnLayout()
        pm.text(label= 'Random')
        self.random_list = pm.textScrollList(width= 95, height= 300,
                          allowMultiSelection= True)
        pm.rowColumnLayout(numberOfColumns= 2)
                                     #columnWidth= ([1, 50], [2, 50]))
        pm.button(label= '+', width= 45, command= pm.Callback(self.add_random))
        pm.button(label= '-', width= 45, command= pm.Callback(self.remove_random))
        pm.setParent(self.lower_layout)
        pm.columnLayout()
        pm.text(label= 'Quiz Info')
        self.preview_scroll_field = pm.scrollField(wordWrap= True,
                                                    height= 300, width= 340)
        pm.rowColumnLayout(numberOfColumns= 2)
        pm.text(label= 'Random Amount', width= 200)
        self.random_int_field = pm.intField(min= 1, value= 1, width= 50)

        pm.setParent(self.main_layout)
        pm.button(label= 'Create Quiz', command= pm.Callback(self.create_quiz),
                  width= 550, height= 50)
        
        self.list_questions()

    def get_path(self):
        self.path = pm.fileDialog2(fileMode= 3)[0]
        self.path_field.setText(self.path)
        dir_name = os.path.dirname(__file__)
        file_path = os.path.join(dir_name, 'Startup', 'start.path')
        f = open(file_path, 'w')
        pickle_data = pickle.dump(self.path, f)
        f.close()
        

    def preview_quiz(self):
        self.preview_scroll_field.clear()
        core = self.core_list.getAllItems()
        random = self.random_list.getAllItems()
        for c in core:
            index = int(c.split('-')[-1])
            #print index, index+1, index+2, index+3, index+4
            #print self.questions[index]
            #print len(self.questions)
            self.preview_scroll_field.insertText(self.questions[index])
            self.preview_scroll_field.insertText(self.questions[index+1])
            self.preview_scroll_field.insertText(self.questions[index+2])
            self.preview_scroll_field.insertText(self.questions[index+3])
            self.preview_scroll_field.insertText(self.questions[index+4]+'\n')
            self.preview_scroll_field.insertText('------------------------\n')

        for r in random:
            index = int(r.split('-')[-1])
            #print index, index+1, index+2, index+3, index+4
            #print self.questions[index]
            #print len(self.questions)
            self.preview_scroll_field.insertText(self.questions[index])
            self.preview_scroll_field.insertText(self.questions[index+1])
            self.preview_scroll_field.insertText(self.questions[index+2])
            self.preview_scroll_field.insertText(self.questions[index+3])
            self.preview_scroll_field.insertText(self.questions[index+4]+'\n')
            self.preview_scroll_field.insertText('------------------------\n')

    def add_core(self):
        core = self.core_list.getAllItems()
        random = self.random_list.getAllItems()
        selected = self.question_scroll_list.getSelectItem()
        for sel in selected:
            if sel in random:
                win = Error02()
            if sel in core:
                win = Error01()
            if sel not in core and sel not in random:
                self.core_list.append(sel)
        self.preview_quiz()

    def remove_core(self):
        selected = self.core_list.getSelectItem()
        for sel in selected:
            self.core_list.removeItem(sel)
        self.preview_quiz()

    def add_random(self):
        core = self.core_list.getAllItems()
        random = self.random_list.getAllItems()
        selected = self.question_scroll_list.getSelectItem()
        for sel in selected:
            if sel in core:
                win = Error01()
            if sel in random:
                win = Error02()
            if sel not in core and sel not in random:
                self.random_list.append(sel)
        self.preview_quiz()

    def remove_random(self):
        selected = self.random_list.getSelectItem()
        for sel in selected:
            self.random_list.removeItem(sel)
        self.preview_quiz()

    def read_questions(self):
        questions = self.question_scroll_list.getSelectItem()
        self.question_scroll_field.clear()
        for question in questions:
            index = int(question.split('-')[-1])
            #print index, index+1, index+2, index+3, index+4
            #print self.questions[index]
            #print len(self.questions)
            self.question_scroll_field.insertText(self.questions[index])
            self.question_scroll_field.insertText(self.questions[index+1])
            self.question_scroll_field.insertText(self.questions[index+2])
            self.question_scroll_field.insertText(self.questions[index+3])
            self.question_scroll_field.insertText(self.questions[index+4]+'\n')
            self.question_scroll_field.insertText('------------------------\n')
        
    def get_question_info(self):
        core = self.core_list.getAllItems()
        random = self.random_list.getAllItems()
        core_info = []
        random_info = []
        for c in core:
            output = []
            index = int(c.split('-')[-1])
            output.append(self.questions[index])
            output.append(self.questions[index+1])
            output.append(self.questions[index+2])
            output.append(self.questions[index+3])
            output.append(self.questions[index+4])
            core_info.append(output)

        for r in random:
            output = []
            index = int(r.split('-')[-1])
            output.append(self.questions[index])
            output.append(self.questions[index+1])
            output.append(self.questions[index+2])
            output.append(self.questions[index+3])
            output.append(self.questions[index+4])
            random_info.append(output)
            
        return [core_info, random_info]
    
    def get_images(self):
        core = self.core_list.getAllItems()
        random = self.random_list.getAllItems()
        questions_images = []
        file_path = os.path.dirname(__file__)
        for c in core:
            index = int(c.split('-')[-1])
            try:
                image01 = self.questions[index+1].split('==')
                image02 = self.questions[index+2].split('==')
                image03 = self.questions[index+3].split('==')
                image04 = self.questions[index+4].split('==')
                print image01[2], image02[2], image03[2], image04[2]
                image01_path = os.path.join(file_path, 'Images', image01[1])
                image02_path = os.path.join(file_path, 'Images', image02[1])
                image03_path = os.path.join(file_path, 'Images', image03[1])
                image04_path = os.path.join(file_path, 'Images',image04[1])
                questions_images.append(image01_path)
                questions_images.append(image02_path)
                questions_images.append(image03_path)
                questions_images.append(image04_path)
            except:
                pass

        for r in random:
            index = int(r.split('-')[-1])
            try:
                image01 = self.questions[index+1].split('==')
                image02 = self.questions[index+2].split('==')
                image03 = self.questions[index+3].split('==')
                image04 = self.questions[index+4].split('==')
                print image01[2], image02[2], image03[2], image04[2]
                image01_path = os.path.join(file_path, 'Images', image01[1])
                image02_path = os.path.join(file_path, 'Images', image02[1])
                image03_path = os.path.join(file_path, 'Images', image03[1])
                image04_path = os.path.join(file_path, 'Images',image04[1])
                questions_images.append(image01_path)
                questions_images.append(image02_path)
                questions_images.append(image03_path)
                questions_images.append(image04_path)
            except:
                pass
            
        return questions_images
    
    def copy_images(self, images, destination):
        for image in images:
            try:
                #print destination
                shutil.copy(image, destination)
            except:
                print image
    
    def create_quiz(self):
        self.path = self.path_field.getText()
        file_path = os.path.dirname(__file__)
        questions_info = self.get_question_info()
        images_paths = self.get_images()
        quiz_name = self.name_field.getText()
        print 'booya kasha arshztrjy'
        print self.path
        new_directory = os.path.join(self.path, quiz_name)
        print 'booya kasha'
        os.makedirs(new_directory)
        images_dir = os.path.join(new_directory, 'Images')
        os.makedirs(images_dir)
        #os.makedirs(new_dir)
        #shutil.move(new_location, self.characters)
        number_random = self.random_int_field.getValue()
        info_to_pickle = [number_random, questions_info[0], questions_info[1]]
        
        f = open(os.path.join(new_directory, '%s.questions' % (quiz_name)), 'w')
        pickle_data = pickle.dump(info_to_pickle, f)
        f.close()
        
        source_init_file = os.path.join(file_path, 'Source', '__init__.py')
        source_quiz_file = os.path.join(file_path, 'Source', 'quiz.py')
        
        shutil.copy(source_init_file, new_directory)
        shutil.copy(source_quiz_file, new_directory)
        #print 'about to copy'
        #print images_paths
        self.copy_images(images_paths, images_dir)
        
    def list_questions(self):
        x = 1
        i = 0
        while i < len(self.questions):
            self.question_scroll_list.append('Question %s -%s' % (x, i))
            i += 5
            x += 1
            
def gui():
    win = 'quiz_maker'
    if pm.window(win, exists= True):
        pm.deleteUI(win)
        
    if pm.windowPref(win, exists= True):
        pm.windowPref(win, remove= True)
    
    global scroll_field, scroll_list
    my_win = pm.window(win, title= 'Quiz Maker', toolbox= True,
                       width= 550, height= 400)
    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(dir_path, 'questions.txt')
    main_layout = pm.columnLayout()
    maker = Quiz_Maker(file_path)
    my_win.show()