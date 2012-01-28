from django.http import HttpResponse
from django.template import Template, Context

import datetime

# django-admin.py startproject
# python manage.py runserver
def hello(request):
    return HttpResponse('Hello, World')
    
def hours_ahead(request, offset):
    
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = '<html><body>In %s hour(s), it will be %s.</body></html>' %(offset, dt)
    return HttpResponse(html)
    
def fill_data(request):
    '''
    Fill out data in the forum.
    '''
    fp = open(r'templates/value_test.html')
    t = Template(fp.read())
    fp.close()
    student1 = {'first_name':'Michael', 'last_name':'Clavan', 'student_number':55555, 'class':'RBA1202'}
    student2 = {'first_name':'John', 'last_name':'Doe', 'student_number':1111, 'class':'RBA1201'}
    student3 = {'first_name':'Jane', 'last_name':'Doe', 'student_number':3333, 'class':'RBA1201'}
    student4 = {'first_name':'Ken', 'last_name':'Norman', 'student_number':7777, 'class':'RBA1203'}
    
    student_info = [student1, student2, student3, student4]
    blah = 'Michael Clavan'
    
    more_blah = 'Student information.'
    data1 = Context({'blah':'%s %s' %(student2['first_name'], student2['last_name']),
                     'more_blah':student2['student_number']})
    html = t.render(Context(data1))
    return HttpResponse(html)
    
    