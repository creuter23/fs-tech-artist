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
from accounts.models import UserProfile, Disc, Category, Art_Test
# 
from django.contrib import auth
# Import form from form.py
from form import SignupForm

# Registration Stuff....
# Load Registration stuff
from django import forms as forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.template import loader, Context
from django.contrib.auth.models import User

#===============================================================================
#  Functions to handle main login/profile 
#===============================================================================


#--------------------SIGNUP----------------------------------------- 
def signup(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        #print request.POST
        if form.is_valid():
            new_user = form.save()
#            new_user.first_name = form.data['first_name']
#            new_user.last_name = form.data['last_name']
#            new_user.save()
            return HttpResponseRedirect("/accounts/profile/")
        else:
            print'Form Not Valid'
            #print(form.data['last_name'])
            #print(dir(form))
    else:
        form = SignupForm()
        print 'BAD ATTEMPT, MUST BE POST'
    return render_to_response('signup.html', { 'form': form })
#--------------------SIGNUP END--------------------------------------




#--------------------LOGIN----------------------------------------- 
def login(request):
    if request.method != 'POST':
        raise Http404('Only POSTs are allowed')
    try:
        m = request.POST['user_name']
        m = UserProfile.objects.get(username=request.POST['user_name'])
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



#--------------------PROFILE----------------------------------------
@login_required
def profile(request):
    ''' default after login '''
    userdata = {'username':request.user, 'is':request.user.is_authenticated(), 'email':request.user.email}
    print request.user, request.user.is_authenticated()
    print type(request)
    if request.user.is_authenticated():
        t = get_template(r'registration/profile.html')
        c = Context({'userdata':userdata, 'all_data':userdata})
        html =  t.render(c)
        return HttpResponse(html)
    else:
        return HttpResponseRedirect("/login/")
#--------------------PROFILE END------------------------------------


#--------------------EDIT PROFILE------------------------------------

@login_required
def edit_profile(request):
    ''' default after login '''
    print('DO SOMETHING WITH THIS>>>><<<')
#--------------------EDIT PROFILE----------------------------------------



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
        m = UserProfile.objects.get(username=request.POST['username'])
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
        username_frm = UserProfile.objects.get(username=username_form)
        studentID_frm = UserProfile.objects.get(username=studentID_form)
    except UserProfile.DoesNotExist:
        print "UserProfile doesn't current exists.  Adding student to system."
        
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
        new_student = UserProfile(name=name_frm ,username=username_form ,password=password_frm ,email=email_frm ,
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