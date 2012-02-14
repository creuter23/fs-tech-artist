#===============================================================================
#  Imports
#===============================================================================
# art_test_login.html
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect, Http404


# validation
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect

# Accessing data from a Template
from django.template import Template, Context

# Form based
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

# Database access
from accounts.models import Student, Disc, Category, Art_Test, Art_Director
# 
from django.contrib import auth
# Import form from form.py
from form import SignupForm



#===============================================================================
#  Functions to handle main login/profile 
#===============================================================================


#--------------------SIGNUP----------------------------------------- 
def signup(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        print request.POST
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/accounts/profile/")
        else:
            print'NOT RIGHT'
    else:
        form = SignupForm()
        print 'BAD ATTEMPT'
    return render_to_response('signup.html', { 'form': form })
#--------------------SIGNUP END--------------------------------------




#--------------------LOGIN----------------------------------------- 
def login(request):
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
        login_correct = False
        return HttpResponseRedirect('/bad_gateway/')
    except:
        login_correct = False
        return HttpResponseRedirect('/bad_gateway/')
        return HttpResponseRedirect('<script>')
#--------------------LOGIN END--------------------------------------





#===============================================================================
#  ART TEST RELATED
#===============================================================================

#--------------------APPLY----------------------------------------- 
def apply(request):
    # Opens up the main web page.
    t = get_template(r'apply.html')
    html = t.render(Context())
    return HttpResponse(html)




#===============================================================================
#  General Functions
#===============================================================================
def gateway(request):
    # Opens up the main web page.
    t = get_template(r'login.html')
    html = t.render(Context({"valid_login": False}))
    
    return HttpResponse(html)

def bad_gateway(request):
    print 'Poor Choice.'
    t = get_template(r'login.html')
    html = t.render(Context({"valid_login": True}))
    return HttpResponse(html)







#///////////////////////////////////////////////////////////////////////////////
#===============================================================================
#  UNUSED -----> Delete before production
#===============================================================================
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


##########UNUSED###########
    #From signup
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
    
    
    
    
'''
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
    
    
'''
    
    
    
'''
def index(request):
    return render_to_response('index.html', {
        'categories': Category.objects.all(),
        'posts': Blog.objects.all()[:5]
    })

def view_post(request, slug):   
    return render_to_response('view_post.html', {
        'post': get_object_or_404(Blog, slug=slug)
    })

def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render_to_response('view_category.html', {
        'category': category,
        'posts': Blog.objects.filter(category=category)[:5]
    })

'''