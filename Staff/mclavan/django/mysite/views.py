from django.http import HttpResponse
import datetime

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