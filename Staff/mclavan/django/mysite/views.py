from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Template, Context

# Form based
from django.shortcuts import render_to_response
from django.core.mail import send_mail

import datetime

# django-admin.py startproject
# python manage.py runserver
# python manage.py shell
# Database check
# from django.db import connection
# cursor = connection.cursor()

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
    Passing data to a Template.
    '''
    # Setting up the template
    '''
    fp = open(r'templates/value_test.html')
    t = Template(fp.read())
    fp.close()
    '''
    t = get_template(r'value_test.html')
    # Preparing Data
    # Basic Data
    blah = 'Michael Clavan'
    more_blah = 'Student information.'
    # Dictionaries
    # Dictionaries can be access though dot notations.
    student1 = {'first_name':'Michael', 'last_name':'Clavan', 'student_number':55555, 'class':'RBA1202'}
    student2 = {'first_name':'John', 'last_name':'Doe', 'student_number':1111, 'class':'RBA1201'}
    student3 = {'first_name':'Jane', 'last_name':'Doe', 'student_number':3333, 'class':'RBA1201'}
    student4 = {'first_name':'Ken', 'last_name':'Norman', 'student_number':7777, 'class':'RBA1203'}
    
    # Grouping dictionaries for template looping
    student_info = [student1, student2, student3, student4]

    # The context will pass information back to the template.
    # Context are setup as dictionaries.
    # {'key':value} 
    data1 = Context({'path':request.get_host(),'blah':'%s %s' %(student2['first_name'], student2['last_name']),
                     'more_blah':student2['student_number'], 'students':student_info})
    
    # Passing data into template.
    html = t.render(Context(data1))
    return HttpResponse(html)

    
'''
Catching data from a template.
'''
# Form Test
def getting_data(request):
    return render_to_response('form_test.html')

def search(request):
    if 'q' in request.GET:
        message = 'You searched for : %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

def contact(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a subject')
        if not request.POST.get('message', ''):
            errors.append('Enter a message')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            send_mail(
                request.POST['subject'],
                request.POST['message'],
                request.POST.get('email', 'noreply@example.com'),
                ['siteowner@example.com'],                
            )
            return HtpResponseRedirect('/contact/thanks/')
    return render_to_response('contact_form.html', {'errors': errors})


'''
Getting information from a model.
'''
    