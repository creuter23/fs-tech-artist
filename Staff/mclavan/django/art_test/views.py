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
    if request.method != 'GET':
        raise Http404('Only POSTs are allowed')
    try:
        m = request.GET['user_name']
        
        
        m = Student.objects.get(username=request.GET['user_name'])
        
        result = m.password == request.GET['password']
        print m.password, request.GET['password'], result
        if m.password == request.GET['password']:
                request.session['student_id'] = m.student_id
                return HttpResponseRedirect('/you-are-logged-in/')
        
        return HttpResponse("Your response is %s" %m)
        
    except:
        # Database access
        m = Student.objects.get(username=request.GET['user_name'])
        
        user = m.username
        pasw = m.password
        return HttpResponse("Your username and password didn't match. %s, %s, %s" % (m, user, pasw))
    # return render_to_response("Your username and password didn't match.", c)
    

