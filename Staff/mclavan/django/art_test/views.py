# art_test_login.html
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect, Http404

# validation
from django.core.context_processors import csrf
from django.shortcuts import render_to_response


# Accessing data from a Template
from django.template import Template, Context

# Form based
from django.core.mail import send_mail

# Database access
from users.models import Student

def gateway(request):
    # Opens up the main web page.
    t = get_template(r'login.html')
    html = t.render(Context())
    return HttpResponse(html)
    
def login(request):
    
    '''
    if request.method != 'POST':
        raise Http404('Only POSTs are allowed')
    try:
        m = Student.objects.get(username=request.POST['username'])
        if m.password == request.POST['password']:
            request.session['member_id'] = m.id
            return HttpResponseRedirect('/you-are-logged-in/')
    except Member.DoesNotExist:
        return HttpResponse("Your username and password didn't match.")
    '''
    # c = {}
    # c.update(csrf(request))
    if request.method != 'POST':
        raise Http404('Only POSTs are allowed')
    try:
        m = request.POST['user_name']
        
        
        m = Student.objects.get(username=request.POST['user_name'])
        
        result = m.password == request.POST['password']
        print m.password, request.POST['password'], result
        if m.password == request.POST['password']:
                request.session['student_id'] = m.student_id
                return HttpResponseRedirect('/apply/')
        
        return HttpResponse("Your response is %s" %m)
        
    except:
        # Database access
        m = Student.objects.get(username=request.POST['user_name'])
        
        user = m.username
        pasw = m.password
        return HttpResponse("Your username and password didn't match. %s, %s, %s" % (m, user, pasw))
    # return render_to_response("Your username and password didn't match.", c)
    

def apply(request):
    # Opens up the main web page.
    t = get_template(r'apply.html')
    html = t.render(Context())
    return HttpResponse(html)
    
def signup(request):
    if request.method != 'POST':
        raise Http404('Only POSTs are allowed')
    t = get_template(r'signup.html')
    html = t.render(Context())
    return HttpResponse(html)    

def user_check(request):
    errors = []
    if request.method != 'POST':
        raise Http404('Only POSTs are allowed')
    # Check for user name in the database
    username_form = request.POST['username']
    studentID_form = request.POST['studentID']    
    name_frm = request.POST['name']
    password_frm = request.POST['password']
    email_frm = request.POST['email']
    class_frm = request.POST['classID']
    username_frm = ''
    studentID_frm = ''
    try:
        # Getting data from form.    
        username_frm = Student.objects.get(username=username_form)
        studentID_frm = Student.objects.get(username=studentID_form)
    except Student.DoesNotExist:
        print "Student doesn't current exists.  Adding student to system."
        
    if username_frm or studentID_frm:
        # User profile already exists.
        return HttpResponse('Account allready exists.')
    else:
        # update database
        print 'Validate Form.'
        if not username_form:
            errors.append('Missing user name.')
        if not studentID_form:
            errors.append('Missing student ID.')
        if not name_frm:
            errors.append('Missing name.')            
        if not password_frm:
            errors.append('Missing password.')
        if not email_frm:
            errors.append('Missing email.')
        if not class_frm:
            errors.append('Missing class ID.')            
    # Check for student number in the database


        
        
    if not errors:
        # Add user to the database
        new_student = Student(name=name_frm ,username=username_form ,password=password_frm ,email=email_frm ,
                classid=class_frm ,student_id=studentID_form, disc='', comments='')
        new_student.save()
        return HttpResponseRedirect('/apply/')
    else:
        error_line = 'Whoops, you left out some fields.<br>'
        for error in errors:
            error_line += '%s<br>' % error 
        return HttpResponse(error_line)
    