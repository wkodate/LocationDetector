 # -*- coding: UTF-8 -*-
from django.template import Context, loader
import googleMaps
from django.http import HttpResponse
 
def home(req):
    t = loader.get_template('views.html')
    c = Context({
        'user': 'user',
        'lat':  35.6909,
        'lng':  139.7002,
        'text': 'text',
    })
    return HttpResponse(t.render(c))
