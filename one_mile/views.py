from django import forms
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response

from one_mile.models import *

import simplejson
import time
from datetime import datetime
import hashlib

HASH_STRING = 'yiyayiqipao'

@csrf_exempt
def index(request):
    return render_to_response('index.html');

@csrf_exempt
def login(request):
    response = {}
    try :
        username = request.POST.get("username")
        password = request.POST.get("password")

        users = User.objects.filter(name=username)
        if (len(users) == 1):
            user = users[0]
            if (user.password == __make_password(password)):
                response['result'] = 'success'
                return HttpResponse(simplejson.dumps(response))
            else :
                response['result'] = 'wrong password'
                return HttpResponse(simplejson.dumps(response))

        response['result'] = 'wrong username'
        return HttpResponse(simplejson.dumps(response))

    except Exception as e:
        response['result'] = 'internal error'
        return HttpResponse(simplejson.dumps(response))

@csrf_exempt
def reg_page(request):
    return render_to_response('register.html')

@csrf_exempt
def register(request):
    print ('register')
    response = {}
    try :
        username = request.POST.get("username")
        print (username)
        password = request.POST.get("password")
        print (password)
        password = __make_password(password);

        print (password)

        user = User(name=username, password=password)
        user.save()

        print (user.id)

        response['result'] = 'success'
        return HttpResponse(simplejson.dumps(response))
    except Exception as e:
        print ('Exception', e)
        response['result'] = 'internal error'
        return HttpResponse(simplejson.dumps(response))

@csrf_exempt
def upload_page(request):
    return render_to_response('upload.html')

class PictureForm(forms.Form):
    picture = forms.FileField()

@csrf_exempt
def upload(request):
    try :
        response = {}
        
        user = User.objects.all()[0]
        sport = request.POST.get("sport")
        distance = float(request.POST.get("distance"))
        run_d = time.strptime(request.POST.get("run_date"), "%m/%d/%Y")
        run_date = datetime.fromtimestamp(time.mktime(run_d))
        witness = request.POST.get("witness")
        comment = request.POST.get("comment")
        
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            run_log = RunLog(
                user = user,
                sport = sport,
                run_date = run_date,
                distance = distance,
                picture = request.FILES['picture'],
                witness = witness,
                comment = comment)
            run_log.save()

            print (run_log.id)
        
            response['result'] = 'success'
            return HttpResponse(simplejson.dumps(response))
        else :
            response['result'] = 'form invalid'
            return HttpResponse(simplejson.dumps(response))
        
    except Exception as e:
        print ('Exception', e)
        response['result'] = 'internal error'
        return HttpResponse(simplejson.dumps(response))

def __make_password(password):
    hash_str = password + HASH_STRING
    return hashlib.md5(hash_str.encode('utf-8')).hexdigest()
