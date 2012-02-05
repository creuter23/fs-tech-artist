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
from users.models import Student, Disc, Category
# 
from django.contrib import auth
# Import form from form.py
from form import SignupForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/accounts/profile/")
    else:
        form = SignupForm()
    return render_to_response('signup.html', { 'form': form })
# Load Registration stuff
from django import forms as forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.template import loader, Context
from django.contrib.auth.models import User


def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        data = request.POST.copy()
        errors = form.get_validation_errors(data)
        if not errors:
            new_user = form.save(data)
            return HttpResponseRedirect("/art_test/")
    else:
        data, errors = {}, {}
    return render_to_response("registration/register.html", {
        'form' : forms.FormWrapper(form, data, errors)
    })

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
   

#from django.views.decorators.csrf import csrf_protect
#from django.utils.functional import allow_lazy
#from django.template import resolve_variable
@login_required
def profile(request):
    ''' default after login '''
    #user = resolve_variable('user', user.username)
    userdata = {'username':request.user, 'is':request.user.is_authenticated(), 'email':request.user.email, 'profile':request.user.get_profile()}
    print request.user, request.user.is_authenticated()
    print type(request)
    if request.user.is_authenticated():
        t = get_template(r'registration/profile.html')
        #t = Template("/registration/profile.html")
        c = Context({'userdata':userdata, 'all_data':userdata})
        html =  t.render(c)
        return HttpResponse(html)
        #return render_to_response('registration/profile.html', { 'user.username': 'user.username'})

    else:
        #print('not auth')
        return HttpResponseRedirect("/login/")

'''
def login(request):
    

    if request.method != 'POST':
        raise Http404('Only POSTs are allowed')
    try:
        m = Student.objects.get(username=request.POST['username'])
        if m.password == request.POST['password']:
            request.session['member_id'] = m.id
            return HttpResponseRedirect('/you-are-logged-in/')
    except Member.DoesNotExist:
        return HttpResponse("Your username and password didn't match.")

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
        
        login_correct = False
        return HttpResponseRedirect('/bad_gateway/')
        # return redirect(bad_gateway)
        # return HttpResponse("Please returnYour response is %s" %m)
        
    except:
        login_correct = False
        return HttpResponseRedirect('/bad_gateway/')
        return HttpResponseRedirect('<script>')


        # return redirect(bad_gateway)
    # return render_to_response("Your username and password didn't match.", c)
    
'''
def apply(request):
    # Opens up the main web page.
    t = get_template(r'apply.html')
    html = t.render(Context())
    return HttpResponse(html)

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        m = Member.objects.get(username__exact=request.POST['username'])
        request.session['member_id'] = m.id
        # Redirect to a success page.
        return HttpResponseRedirect("/registration/profile/", user)
    else:
        # Show an error page
        return HttpResponseRedirect("/bad_gateway/")





def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/account/loggedout/")
''' 
def signup(request):
    if request.method != 'POST':
        raise Http404('Only POSTs are allowed')
    t = get_template(r'signup.html')
    html = t.render(Context())
    return HttpResponse(html)    
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

from django.core.mail import send_mail



def art_test(request):
    student_name = 'Michael Clavan'
    student_id = 12341234
    student_email = 'mclavan@fullsail.com'
    student_class = 'RBA'
    test_type = 'Modeling'
    art_director = 'hseewald@fullsail.com'
    course_director = 'hseewald@fullsail.com'
    message1 = '''%s has signed up for the %s art test.\n
    Here is his other vitals:
    Student Name: \tNew Art%s\n
    Student Number:\t%s\n
    Student Email:\t%s\n
    Current Class:\t%s\n''' % (student_name, test_type, student_name, student_id, student_email, student_class)
    
    message2 = '''<h1>New Art Test Submittion. </h1>
    <h3>%s has signed up for the %s art test.\n
  Here is there other vitals:

</h3>
<table width="324" border="1">
  <tr>
    <td width="121">Student Name:</td>
    <td width="187" align="left">%s</td>
  </tr>
  <tr>
    <td>Student Number:</td>
    <td align="left">%s</td>
  </tr>
  <tr>
    <td>Student Email:</td>
    <td align="left">%s</td>
  </tr>
  <tr>
    <td>Current Class:</td>
    <td align="left">%s</td>
  </tr>  
</table>''' % (student_name, test_type, student_name, student_id, student_email, student_class)
    
    message3 = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Untitled Document</title>
</head>

<body>
<h1>New Art Test Submittion. </h1>
<h3>%s has signed up for the %s art test.\n
  Here is there other vitals:

</h3>
<table width="324" border="1">
  <tr>
    <td width="121">Student Name:</td>
    <td width="187" align="left">%s</td>
  </tr>
  <tr>
    <td>Student Number:</td>
    <td align="left">%s</td>
  </tr>
  <tr>
    <td>Student Email:</td>
    <td align="left">%s</td>
  </tr>
  <tr>
    <td>Current Class:</td>
    <td align="left">%s</td>
  </tr>  
</table>
    
   
</body>
</html>''' % (student_name, test_type, student_name, student_id, student_email, student_class)   
    '''
    send_mail('%s Art Test - Sign Up' % test_type, message, student_email,
        [art_director], fail_silently=False)
    
    '''
    
    
    subject, from_email, to = '%s Art Test - Sign Up' % test_type, student_email, art_director
    text_content = message1
    html_content = message2
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
    return HttpResponse('Email Sent.\nBase Info\n%s' % message2)
    
    
