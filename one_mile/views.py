from django.shortcuts import render
from one_mile.models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response

import simplejson


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
def register(request):
    response = {}
    try :
        username = request.POST.get("username")
        password = request.POST.get("password")
        password = __make_password(password);

        user = User(name=username, password=password)
        user.save()

        print (user.id)

        response['result'] = 'success'
        return HttpResponse(simplejson.dumps(response))
    except Exception as e:
        response['result'] = 'internal error'
        return HttpResponse(simplejson.dumps(response))
        

def __make_password(password):
    hash_str = password + HASH_STRING
    return hashlib.md5(hash_str.encode('utf-8')).hexdigest()
