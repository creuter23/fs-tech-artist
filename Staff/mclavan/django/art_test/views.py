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
from accounts.models import UserProfile, Disc, Category, Art_Test, Art_Test_Attempt
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
from django.contrib.auth import authenticate, login, logout
#Handles the email...
from django.core.mail import send_mail


#===============================================================================
#  Functions to handle main login/profile 
#===============================================================================
CURRENT_MONTH = '1203'

#--------------------SIGNUP----------------------------------------- 
def signup(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        #print request.POST
        if form.is_valid():
            new_user = form.save()
            
            subject = 'User Registration'
            message = 'Thank you for registering. \nYour username is: %s\nYour Password is %s' %(form.data['username'],form.data['password'])
            from_email = 'fspccdocs@gmail.com'
            to_email = [form.data['email']]
            
            send_mail(subject, message, from_email, to_email, fail_silently=False)
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


import os

@login_required
def site_status(request):
    user_profile = request.user.get_profile()

    user_data = {'fname': user_profile.user.first_name, 'lname': user_profile.user.last_name,'user':user_profile.user.username, 'level':user_profile.user_level, 'disc':user_profile.disc.name}
    print user_data
    
    if user_profile.user_level == 's':
        # User is a student
        return student_area(request, user_profile)
    else:
        return staff_art_area(request, user_profile)
        '''
        t = get_template(r'testTemp/logged_in.html')
        html = t.render(Context({'user_data':user_data}))
        return HttpResponse(html)
        '''

@login_required
def site_status2(request):
    user_profile = request.user.get_profile()

    user_data = {'fname': user_profile.user.first_name, 'lname': user_profile.user.last_name,'user':user_profile.user.username, 'level':user_profile.user_level, 'disc':user_profile.disc.name}
    print user_data
    
    """
    if user_profile.user_level == 's':
        # User is a student
        return student_area(request, user_profile)
    else:
        return staff_art_area(request, user_profile)
        '''
        t = get_template(r'testTemp/main.html')
        html = t.render(Context({'user_data':user_data}))
        return HttpResponse(html)
        '''
    """
    # Get current projects.
    attempts = Art_Test_Attempt.objects.filter(student=user_profile).exclude(month=CURRENT_MONTH)
    current = Art_Test_Attempt.objects.filter(student=user_profile, month=CURRENT_MONTH)
    print user_profile, attempts
    art_test_apply = True
    
    t = get_template(r'testTemp/main.html')
    html = t.render(Context({'user_data':user_data, 'current': len(current),
                             'attempts':current, 'previous':attempts}))
    
    return HttpResponse(html)
    
@login_required
def student_area(request, user_profile):
    # Directs the student to the correct area of the site.
    user_data = {'user':user_profile.user.username, 'level':user_profile.user_level, 'disc':user_profile.disc.name}
    
    # Get current projects.
    attempts = Art_Test_Attempt.objects.filter(student=user_profile).exclude(month=CURRENT_MONTH)
    current = Art_Test_Attempt.objects.filter(student=user_profile, month=CURRENT_MONTH)
    print user_profile, attempts
    art_test_apply = True
    
    t = get_template(r'testTemp/art_test_student.html')
    html = t.render(Context({'user_data':user_data, 'current': len(current),
                             'attempts':current, 'previous':attempts}))
    

    
    # Update apply button.
    return HttpResponse(html)
    
@login_required
def staff_art_area(request, user_profile):
    # Directs the student to the correct area of the site.
    user_data = {'user':user_profile.user.username, 'level':user_profile.user_level, 'disc':user_profile.disc.name}
    
    # Get current projects.
    disc_items = {}
    for item in Disc.objects.all():
        disc_items[item.name] = Art_Test_Attempt.objects.filter(disc_name=item, month=CURRENT_MONTH)
        

    print disc_items
    t = get_template(r'testTemp/logged_in.html')
    html = t.render(Context({'user_data':user_data, 'art_test':disc_items}))
  
    # Update apply button.
    return HttpResponse(html)
    
@login_required
def site_logout(request):
    '''
    Logging off the site.
    '''
    user_profile = request.user.get_profile()

    logout(request)
    html = '%s has been logged out.' %(user_profile.user.username)
    t = get_template(r'testTemp/light_test.html')
    html = t.render(Context({'base_path':'http://www.fs-tag.com'}))
    # html = t.render(Context({'user_data':user_data}))    
    
    # return HttpResponseRedirect('testTemp/light_test.html')
    return HttpResponse(html)

#--------------------LOGIN----------------------------------------- 
@login_required
def login(request):
    
    user_profile = request.user.get_profile()
    html = 'Username: %s<br>Class Id: %s' %(user_profile.user.username, user_profile.class_id)
    # logout(request)
    return HttpResponseRedirect('/main_page/')
    
    print 'testing'
    if request.method != 'POST':
        raise Http404('Only POSTs are allowed')
    try:
        user_profile = request.user.get_profile()
        print user_profile.class_id
        m = request.POST['user_name']
        # print m
        m = UserProfile.objects.get(username=request.POST['user_name'])
        # print 'checking: ' + m
        result = m.password == request.POST['password']
        print result
        
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
#--------------------SIGNUP START------------------------------------
# User cannot be allowed for fourth art test.  That must be created by the admin.
DISC_NAMES = (( u'ANI', u'Animation'), (u'SAL', u'Shading And Lighting'), (u'VFX', u'Visual FX'), 
             (u'VEM', u'Vehicle Modeling'), (u'ARC', u'Architectural Modeling'),
             (u'CMD', u'Character Modeling'),(u'RIG', u'Rigging'), (u'COMP', u'Compositing'))

@login_required
def apply_check(request):
    user_profile = request.user.get_profile()
    # This function checks through the user to see if they have allotted their max amout of art test attempts.
    
    for disc in DISC_NAMES:
        if '%s_sub' % disc[0] in request.POST:
            signup(user_profile, disc[0], CURRENT_MONTH)
    
    status = 0
    # If they are under there max amount return turn.
    return student_area(request, user_profile)  

@login_required
def signup(user_profile, art_test, current_month):
    # data
    result = False  
    
    disc_info = Disc.objects.filter(name=art_test)
    print disc_info
    if disc_info:
        attempts = Art_Test_Attempt.objects.filter(student=user_profile, disc_name=disc_info[0])
        print attempts
        if len(attempts) < 3:
            result = True   

    if result and disc_info:
        art_obj = Art_Test_Attempt(student=user_profile, AT_status=str(len(attempts)+1), disc_name=disc_info[0],
                        month=current_month, asset_status='c', assesment=0)
        art_obj.save()
    
    # Refresh page.
    return result
       
#--------------------SIGNUP END------------------------------------

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
    t = get_template(r'apply.html')
    html = t.render(Context({"valid_login": False}))
    
    return HttpResponse(html)

def bad_gateway(request):
    print 'Poor Choice.'
    t = get_template(r'apply.html')
    html = t.render(Context({"valid_login": True}))
    return HttpResponse(html)



#===============================================================================
# Panel Review Functions
#===============================================================================
####This should be its own app... 


STUDENTS = [
{'name': 'Django Reinhardt', 'disc': 'VFX',    'courseid': 'ANP' },
{'name': 'Jimi Hendrix',     'disc': 'SAL',    'courseid': 'ANP' },
{'name': 'Louis Armstrong',  'disc': 'VFX',    'courseid': 'PCC' },
{'name': 'Pete Townsend',    'disc': 'SAL',    'courseid': 'PCC' },
{'name': 'Yanni',            'disc': 'ANI',    'courseid': 'ANP' },
{'name': 'Wesley Willis',    'disc': 'ANI',    'courseid': 'ANP' },
{'name': 'John Lennon',      'disc': 'SAL',    'courseid': 'PCC' },
{'name': 'Bono',             'disc': 'SAL',    'courseid': 'ANP' },
{'name': 'Garth Brooks',     'disc': 'ANI',    'courseid': 'ANP' },
{'name': 'Duke Ellington',   'disc': 'VFX',    'courseid': 'PCC' },
{'name': 'William Shatner',  'disc': 'COMP',   'courseid': 'ANP' },
{'name': 'Madonna',          'disc': 'COMP',   'courseid': 'ANP' }
]

def panel(request):
    students = []
    for s in STUDENTS:
        students.append({
                         'name': s['name'],
                         'disc': s['disc'],
                         'courseid': s['courseid'],
                         'is_important': s['name'] in ('disc')
                         })
        
    return render_to_response('panels.html', {'students': STUDENTS})


testStudInfo = (['joe','user','sal','anp','monday'], ['tom','someguy','vfx','pcc','thursday'])


def panels(request):
    t = get_template(r'panels.html')
    html = t.render(Context({"title": "Panel Review 2.1", "studentList": testStudInfo }))
    return HttpResponse(html)






#'is_important': s[disc] in ('VFX', 'SAL'),

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