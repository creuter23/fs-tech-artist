'''
Access to all things excel
'''

# Modules for reading and writing to excel docs (xls)
import xlrd
import xlwt

# Module for access data from a excel doc (xlsx)
import openpyxl


print 'testing'

# Get all student names and numbers from excel scheet.


'''
book = xlrd.open_workbook('RBA1201.xls')
# print book


# 1st sheet
attend = book.sheet_by_index(1)
# 1st student name
attend.cell_value(5,0)
# 1st student value
attend.cell_value(5,1)
'''

def get_student_info(excel_file='RBA1201.xls'):
    book = xlrd.open_workbook(excel_file)
    
    student_info = {}
    student_names = []
    student_ids = []
    attend = book.sheet_by_index(1)
    current_cell = 5
    cell_count = 0
    while attend.cell_value(current_cell,0) != '':
        student_info[current_cell - 5] = [attend.cell_value(current_cell,0), int(attend.cell_value(current_cell,1))]
        
        # student_names.append(attend.cell_value(current_cell,0))
        # student_ids.append(int(attend.cell_value(current_cell,1)))
        # print student_names[-1], student_ids[-1]
        current_cell += 1
    

# Check till the end of the 
# attend.cell_value(26,0) == ''

# Convert into a sqlite database

# What, new information.

# Research how sqlite3 is differnet from mysql
# Blah, blah, and blah