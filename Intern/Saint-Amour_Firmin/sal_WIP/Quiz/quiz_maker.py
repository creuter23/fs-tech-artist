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
    
class Quiz_Maker(object):
    
    def __init__(self, questions_file):
        self.file = open(questions_file, 'r')
        self.questions = self.file.readlines()
        self.file.close()
        self.main_layout = pm.columnLayout()
        self.name_field = pm.textFieldGrp(label= 'Quiz Name')
        self.layout = pm.rowColumnLayout(numberOfColumns= 2,
                                     columnWidth= ([1, 75], [2, 475]))
        pm.columnLayout()
        pm.text(label= 'Questions')
        self.question_scroll_list = pm.textScrollList(width= 60, height= 400,
                          selectCommand= pm.Callback(self.read_questions),
                          allowMultiSelection= True)
        
        pm.setParent(self.layout)
        pm.columnLayout()
        pm.text(label= 'Questions Info')
        self.question_scroll_field = pm.scrollField(wordWrap= True,
                                                    height= 400, width= 475)
        
        pm.setParent(self.main_layout)
        pm.button(label= 'Create Quiz', command= pm.Callback(self.create_quiz),
                  width= 550, height= 50)
        
        self.list_questions()
        
    def read_questions(self):
        questions = self.question_scroll_list.getSelectItem()
        self.question_scroll_field.clear()
        for question in questions:
            index = int(question)
            self.question_scroll_field.insertText(self.questions[index])
            self.question_scroll_field.insertText(self.questions[index+1])
            self.question_scroll_field.insertText(self.questions[index+2])
            self.question_scroll_field.insertText(self.questions[index+3])
            self.question_scroll_field.insertText(self.questions[index+4]+'\n')
            self.question_scroll_field.insertText('------------------------\n')
        
    def get_question_info(self):
        questions = self.question_scroll_list.getSelectItem()
        questions_info = []
        for question in questions:
            output = []
            index = int(question)
            output.append(self.questions[index])
            output.append(self.questions[index+1])
            output.append(self.questions[index+2])
            output.append(self.questions[index+3])
            output.append(self.questions[index+4])
            questions_info.append(output)
            
        return questions_info
    
    def get_images(self):
        questions = self.question_scroll_list.getSelectItem()
        questions_images = []
        file_path = os.path.dirname(__file__)
        for question in questions:
            index = int(question)
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
        questions_info = self.get_question_info()
        images_paths = self.get_images()
        quiz_name = self.name_field.getText()
        file_path = os.path.dirname(__file__)
        new_directory = os.path.join(file_path, quiz_name)
        os.makedirs(new_directory)
        images_dir = os.path.join(new_directory, 'Images')
        os.makedirs(images_dir)
        #os.makedirs(new_dir)
        #shutil.move(new_location, self.characters)
        
        f = open(os.path.join(new_directory, '%s.questions' % (quiz_name)), 'w')
        pickle_data = pickle.dump(questions_info, f)
        f.close()
        
        source_init_file = os.path.join(file_path, 'Source', '__init__.pyc')
        source_quiz_file = os.path.join(file_path, 'Source', 'quiz.pyc')
        
        shutil.copy(source_init_file, new_directory)
        shutil.copy(source_quiz_file, new_directory)
        #print 'about to copy'
        #print images_paths
        self.copy_images(images_paths, images_dir)
        
    def list_questions(self):
        i = 0
        while i < len(self.questions):
            self.question_scroll_list.append('%s' % (i))
            i += 5
            
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