'''
Excel Pull
excel.py

Description:
This function has a series of function to pull information from an excel file.
Without opening excel itself.

However, you must have the xlrd module included in the site packages folder for 
the version of maya you are currently using.
http://www.python-excel.org/


How to Run:

import excel
reload( excel )

# current location of the excel sheet.
filePath = '/Users/michaelclavan/Desktop/Baseball_Template.xls'
cols = ['a', 'c', "i", "j", "k", "l"]
tags = ['name', 'salary','wins','era','saves','k']
line = excel.baseballExport( filePath, "pitcher", 1, 37, cols, tags )

print(line)


cols = ['n', 'p', "r", "s", "t", "u"]
tags = ['name', 'salary','hr','rbi','sb','ave']	
line = excel.baseballExport( filePath, "3rdbase", 1, 12, cols, tags )

print(line)


'''

import xlrd
import os.path
import maya.cmds as cmds

"""
filePath = '/Users/michaelclavan/Desktop/Baseball_Template.xls'

book = xlrd.open_workbook( filePath )

print( "This number of work sheets is %s." %book.nsheets )

print "Worksheet name(s):", book.sheet_names()
sh = book.sheet_by_index(0)

print sh.name, sh.nrows, sh.ncols
print "Cell A2 is", sh.cell_value(rowx=29, colx=3)
print( "Cell A2 is %s" %sh.cell_value( rowx=2, colx=0 ) )
 
player = "pitcher"
line = "<%sS>\n" % player.upper()
for i in range(1, 37):
	line += "\t<%s>\n" %player
	name = sh.cell_value( rowx=i, colx=0 )
	salary = int(sh.cell_value( rowx=i, colx=2 ))
	wins = int(sh.cell_value( rowx=i, colx=8 ))
	era = int(sh.cell_value( rowx=i, colx=9 ))
	saves = int(sh.cell_value( rowx=i, colx=10 ))
	k = int(sh.cell_value( rowx=i, colx=11 ))

	line += "\t\t<name>%s</name>\n" %name 
	line += "\t\t<salary>%s</salary>\n" %salary 
	line += "\t\t<wins>%s</wins>\n" %wins 
	line += "\t\t<era>%s</era>\n" %era 
	line += "\t\t<saves>%s</saves>\n" %saves 
	line += "\t\t<k>%s</k>\n" %k 
	line += "\t</%s>\n" %player

line += "</%sS>\n" % player.upper()

print(line)
"""

'''
cols = ['a', 'c', "i", "j", "k", "l"]
tags = ['name', 'salary','wins','era','saves','k']

cols = []
tags = []
'''
alpha = {"a" : 1, "b" : 2, "c" : 3, "d" : 4, "e" : 5, "f" : 6, "g" : 7, "h" : 8, "i" : 9, "j" : 10, "k" : 11, "l" : 12, "m" : 13, "n" : 14, "o" : 15, "p" : 16, "q" : 17, "r" : 18, "s" : 19, "t" : 20, "u" : 21, "v" : 22, "w" : 23, "x" : 24, "y" : 25, "z" : 26 }

def promptExport( pos, start, end, cols, tags ):
	'''
	File prompt is given
	'''
	results = cmds.fileDialog(  m=0, dm='*.xls' )
	if( results ):
		temp = baseballExport( results, pos, start, end, cols, tags )
		return temp
	else:
		print("Cancelled.")

def baseballExport( filePath, pos, start, end, cols, tags ):
	'''
	# Current file path
	curPath = os.path.split( __file__ )[0]
	# xls file name
	filePath = os.path.join( curPath, fileName )
	'''
	
	# Opening xls file (Returns book)
	book = xlrd.open_workbook( filePath )
	# Getting the sheet (Cells are contained there)
	sh = book.sheet_by_index(0)
	
	player = pos
	line = "<%sS>\n" % player.upper()
	
	# colNum( alpha, "aa" )
	colNum = lambda alpha, cell : (len(cell) - 1) * 26 + (alpha[cell[-1]])  
	
	# Looping through the given range converting text to fit for xml format.
	for i in range(start, end):
		line += "\t<%s>\n" %player
		for m, col in enumerate(cols):
			temp=""
			
			if(m == 0):
				temp = sh.cell_value( rowx=i, colx=colNum(alpha, col)-1 )
			else:
				temp = int(sh.cell_value( rowx=i, colx=colNum(alpha, col)-1 ))
			
			#temp = sh.cell_value( rowx=i, colx=colNum(alpha, col)-1 )

			line += "\t\t<%s>%s</%s>\n" %(tags[m],temp, tags[m]) 
		'''
		if(pos == "pitcher"):
			name = sh.cell_value( rowx=i, colx=0 )
			salary = int(sh.cell_value( rowx=i, colx=2 ))
			wins = int(sh.cell_value( rowx=i, colx=8 ))
			era = int(sh.cell_value( rowx=i, colx=9 ))
			saves = int(sh.cell_value( rowx=i, colx=10 ))
			k = int(sh.cell_value( rowx=i, colx=11 ))
		
			line += "\t\t<name>%s</name>\n" %name 
			line += "\t\t<salary>%s</salary>\n" %salary 
			line += "\t\t<wins>%s</wins>\n" %wins 
			line += "\t\t<era>%s</era>\n" %era 
			line += "\t\t<saves>%s</saves>\n" %saves 
			line += "\t\t<k>%s</k>\n" %k 
			line += "\t</%s>\n" %player
		else:
			name = sh.cell_value( rowx=i, colx=0 )
			salary = int(sh.cell_value( rowx=i, colx=2 ))
			hr = int(sh.cell_value( rowx=i, colx=8 ))
			rbi = int(sh.cell_value( rowx=i, colx=9 ))
			sb = int(sh.cell_value( rowx=i, colx=10 ))
			ave = int(sh.cell_value( rowx=i, colx=11 ))
		
			line += "\t\t<name>%s</name>\n" %name 
			line += "\t\t<salary>%s</salary>\n" %salary 
			line += "\t\t<hr>%s</hr>\n" %hr 
			line += "\t\t<rbi>%s</rbi>\n" %rbi 
			line += "\t\t<sb>%s</sb>\n" %sb 
			line += "\t\t<ave>%s</ave>\n" %ave 
		'''
	
	line += "</%sS>\n" % player.upper()
	
	
	return line
'''	
alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"] 	

["name", "salary", "hr", "rbi", "sb", "ave"]
'''

def writeXML(data):

	# prepare path, it will print out in the same path of the script.)
	#curPath = os.path.split( __file__ )[0]
	#xmlFile = os.path.join( curPath, fileName )
	
	results = cmds.fileDialog( m=1, dm="*.xls" )
	if(results):
		fileInfo = open( results, "w" )
		
		fileInfo.write(data)
		fileInfo.close()
	else:
		print("Cancelled.")

def getData():
	#filePath = '/Users/michaelclavan/Desktop/Baseball_Template.xls'
	results = cmds.fileDialog( m=0, dm="*.xls" )

	if(results):
		cols = ['a', 'c', "i", "j", "k", "l"]
		tags = ['name', 'salary','wins','era','saves','k']
		line = baseballExport( results, "pitcher", 1, 37, cols, tags )
	
		cols = ['n', 'p', "r", "s", "t", "u"]
		tags = ['name', 'salary','hr','rbi','sb','ave']	
		line += baseballExport( results, "3rdbase", 1, 12, cols, tags )
		
		line += baseballExport( results, "2ndbase", 17, 27, cols, tags )
		line += baseballExport( results, "shortstop", 32, 41, cols, tags )
		
		cols = ['z', 'ab', "ad", "ae", "af", "ag"]
		line += baseballExport( results, "1stbase", 1, 12, cols, tags )
		line += baseballExport( results, "catcher", 17, 27, cols, tags )

		cols = ['aj', 'al', "an", "ao", "ap", "aq"]
		line += baseballExport( results, "outfielder", 1, 28, cols, tags )	
		return line
		
