"""
Comment Class

Author: Jennifer Conley
Date Modified: 1/29/12

This is a class designed to work with the grading scripts for the 3DF course as Full Sail University.

The class will give a scrollField the ability to have a right click menu, which will allow for easily adding in grading comments.
Custom comments will be able to be added by clicking on the 'Custom' option on the right click menu. This will launch a new window
where the user can enter a new display label for the comment as well as the comment itself. The user will also be able to dictate
the grade associated with the comment.

"""

import maya.cmds as cmds
import pymel.core as pm

file_name = '/Users/critnkitten/Library/Preferences/Autodesk/maya/scripts/file_submission.txt'

class Comment_Widget():
    def __init__(self):
        self.mainScroll = cmds.scrollField(ww=True, w=220)
        self.menu_item_comments()

 

    def menu_item_comments(self, *args):
        '''
        Creates the menu items for the comment field
        '''
        self.rmc = cmds.popupMenu(parent=self.mainScroll)
        cmds.menuItem(l='Custom', c=self.create_comment)

                
        self.comments = open(file_name, 'r')
        comment_data = self.comments.readlines()
        self.comments.close()
        
        num_lines = len(comment_data)
        lable = 0
        x = 1
        
        while x < num_lines:
            cmds.menuItem(l=comment_data[lable], c=pm.Callback(self.adding_text, comment_data[x]))

            lable += 2
            x += 2
    
 
    def create_comment(self, *args):
        '''
        Creats the gui for the 'Custom' comment window
        '''
        
        global win_name
        win_name = 'comment_win'
        
        if (cmds.window(win_name, ex=True)):
            cmds.deleteUI(win_name)
        if (cmds.windowPref(win_name, ex=True)):
            cmds.windowPref(win_name, r=1)
            
        cmds.window(win_name)
        cmds.columnLayout()
        cmds.rowColumnLayout(nc=2)
        cmds.text(l='Comment Lable')
        self.new_lableField = cmds.textField()
        cmds.setParent('..')
        cmds.text(l='Enter in new comment')
        self.new_comment_field = cmds.scrollField()
        add = cmds.button(l='Add', c=self.add_comment)
        cmds.showWindow(win_name)
 
        
    def add_comment(self, *args):
        '''
        Adds the newly created lable and comment to the comment file.
        '''
        
        self.new_lable = cmds.textField(self.new_lableField, q=True, tx=True)
        self.new_comment = cmds.scrollField(self.new_comment_field, q=True, tx=True)
        
        comment_file = open(file_name, 'a')
        comment_file.write(self.new_lable + '\n')
        comment_file.write(self.new_comment + '\n')
        comment_file.close()
        
        cmds.deleteUI(win_name)
        cmds.deleteUI(self.rmc)
        self.menu_item_comments()

        

    def adding_text(self, comment):
        '''
        Adds comments to the scrollField
        '''
        
        cmds.scrollField(self.mainScroll, e=True, it=comment)
        
