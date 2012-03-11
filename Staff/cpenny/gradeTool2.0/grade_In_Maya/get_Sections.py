
#import re
import xlrd
class Get_Sections:
	def __init__(self, start_Range = 2, end_Range = 8,
		     start = 0, end = 1,
		     file_loc = '/Users/ChrisP/template.xls'):
		
	
		self.file_loc = file_loc
		self.main_Sections = []
		self.sub_Sections = []
		self.spaces = 0
		self.start_Range = start_Range
		self.end_Range = end_Range
		self.start = start
		self.end = end
	
	def get_info(self, value,  *args):
		xls_Doc = xlrd.open_workbook(self.file_loc)
		xls_Sheet = xls_Doc.sheet_by_index(0) 
		
		for r in range(xls_Sheet.nrows)[value : self.end]:
			row = xls_Sheet.row_values(r)
			
			main_Info = []
			counter = 0
			percentage = []
			stud_Info = []

			stud_Grade = []
			for value in row:
				#print value
				if counter == 0:
					main_Info.append(value)
					print 'Adding: %s to Main Info' %value
				elif counter == 1:

					percentage.append(value)
				
				elif counter == 6:
					stud_Grade.append(value)
				else:
					stud_Info.append(value)

				counter +=1

			main_Info.append(percentage)
			main_Info.append(stud_Info)
			main_Info.append(stud_Grade)
		return  main_Info
	
	def get_sections(self,*args):

		xls_Doc = xlrd.open_workbook(self.file_loc)
		xls_Sheet = xls_Doc.sheet_by_index(0) 

		counter = 0
		for r in range(xls_Sheet.ncols)[ self.start : self.end  ]:	
			line = xls_Sheet.col_values(r)
		
			for value in line:
		
				#seperate values into a list of sections of a list sub_sections 
				if value == '':
					#print "EMPTY"
					self.spaces +=1
				
				if self.spaces == self.start_Range:
					if not value == '':
						self.main_Sections.append(value)
						print "Adding ' %s ' to Main Sections" %value
						
	
				elif  self.spaces > self.start_Range  and self.spaces < self.end_Range:
					#print value
					if not value == '':
						
						row = xls_Sheet.row_values(counter)
						main_Info = []
						index = 0
						percentage = []
						stud_Info = []
			
						stud_Grade = []
						for value in row:
							#print value
							if index == 0:
								main_Info.append(value)
								print 'Adding: %s to Main Info' %value
							elif index == 1:
			
								percentage.append(value)
							
							elif index == 6:
								stud_Grade.append(value)
							else:
								stud_Info.append(value)
			
							index +=1
			
						main_Info.append(percentage)
						main_Info.append(stud_Info)
						main_Info.append(stud_Grade)
						
						self.sub_Sections.append(main_Info)
				counter += 1

			self.main_Sections.append(self.sub_Sections)
		return self.main_Sections
	


'''
row1 = Get_Sections(start_Range = 4, end_Range = 6, start = 8, end = 9)
row1 = row1.get_info()
print row1
second_Col = []
second_Col_First_Sec = Get_Sections(start_Range = 2, end_Range = 8, start = 0, end = 1)
second_Col_Second_Sec = Get_Sections(start_Range = 4, end_Range = 6, start =1, end =2)
first_section = second_Col_First_Sec.get_sections()
second_section = second_Col_Second_Sec.get_sections()

second_Col.append(first_section)
second_Col.append(second_section)

print 'Second Column: %s' %second_Col

'''
