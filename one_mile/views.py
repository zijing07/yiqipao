# -*- coding: utf-8 -*-
from django import forms
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext

from one_mile.models import *

import simplejson
import time
from datetime import datetime
import hashlib

HASH_STRING = 'yiyayiqipao'
SESSION_STATUS = 'paper_white'
SESSION_USER_ID = 'apple_yewww'
ITEM_COUNT = 30

############################################################
## logout
@csrf_exempt
def logout(request):
    if SESSION_STATUS in request.session:
        request.session[SESSION_STATUS] = False
        del request.session[SESSION_USER_ID]
    return HttpResponseRedirect('/index')
        

############################################################
## index/login page
@csrf_exempt
def index(request):
    if SESSION_STATUS in request.session and request.session[SESSION_STATUS] is True:
        user_id = request.session[SESSION_USER_ID]
        users = User.objects.filter(id=user_id)
        user = users[0]
        if user.is_admin is True:
            return HttpResponseRedirect("/audit")
        return HttpResponseRedirect("/profile")

    return render_to_response('index.html')

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
                request.session[SESSION_STATUS] = True
                request.session[SESSION_USER_ID] = user.id
                response['result'] = 'success'

                return HttpResponseRedirect('/profile')
            else :
                response['result'] = 'wrong password'
                return render_to_response('message.html',
                                          {
                                              'message': '密码错误',
                                              'url': '/index'
                                          })

        response['result'] = 'wrong username'
        return render_to_response('message.html',
                                  {
                                      'message': '用户不存在',
                                      'url': '/index'
                                  })

    except Exception as e:
        response['result'] = 'internal error'
        return render_to_response('message.html',
                                  {
                                      'message': '服务器错误，请重试',
                                      'url': '/index'
                                  })

############################################################
## register page
@csrf_exempt
def reg_page(request):
    return render_to_response('register.html')

@csrf_exempt
def register(request):
    print ('register')
    response = {}
    try :
        username = request.POST.get("username")

        users = User.objects.filter(name = username)
        if len(users) > 0:
            return render_to_response('message.html',
                                      {
                                          'message': '用户名已存在',
                                          'url': '/newuser'
                                      })
        
        password = request.POST.get("password")
        password = __make_password(password)

        user = User(name=username, password=password)
        user.save()

        print ('register user id', user.id)

        request.session[SESSION_STATUS] = True
        request.session[SESSION_USER_ID] = user.id
        response['result'] = 'success'
        return HttpResponseRedirect('/profile')
    except Exception as e:
        print ('Exception', e)
        response['result'] = 'internal error'
        return render_to_response('message.html',
                                  {
                                      'message': '服务器错误，请重试',
                                      'url': '/index'
                                  })

############################################################
## upload view
@csrf_exempt
def upload_page(request):
    if SESSION_STATUS not in request.session or request.session[SESSION_STATUS] is not True:
        return render_to_response('index.html')
    user_id = request.session[SESSION_USER_ID]
    users = User.objects.filter(id=user_id)
    if len(users) != 1:
        return HttpResponseRedirect('/index')

    # get notification list
    notifications = Notification.objects.filter(has_seen=False)
    notification_list = [ i for i in notifications if i.run_log.user == users[0] ]

    return render_to_response('upload.html',
                              {
                                  'user': users[0],
                                  'notification_list': notification_list,
                              })

class PictureForm(forms.Form):
    picture = forms.FileField()

@csrf_exempt
def upload(request):
    try :
        if SESSION_STATUS not in request.session or request.session[SESSION_STATUS] is not True:
            return HttpResponseRedirect('/index')
        
        response = {}

        user_id = request.session[SESSION_USER_ID]
        users = User.objects.filter(id=user_id)
        if len(users) != 1:
            return HttpResponseRedirect('/index')
        user = users[0]
        sport = request.POST.get("sport")
        distance = float(request.POST.get("distance"))
        run_d = time.strptime(request.POST.get("run_date"), "%m/%d/%Y")
        run_date = datetime.fromtimestamp(time.mktime(run_d))
        witness = request.POST.get("witness")
        comment = request.POST.get("comment")

        pic_file = None
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            pic_file = request.FILES['picture']

        run_log = RunLog(
            user = user,
            sport = sport,
            run_date = run_date,
            distance = distance,
            picture = pic_file,
            witness = witness,
            comment = comment)
        run_log.save()

        print ('runlog id', run_log.id)
        
        response['result'] = 'success'
        return render_to_response("message.html",
                                  {
                                      'user': user,
                                      'message': "上传成功",
                                      'url': '/profile'
                                  })
        
    except Exception as e:
        print ('Exception', e)
        response['result'] = 'internal error'
        return render_to_response("message.html",
                                  {
                                      'user': user,
                                      'message': "上传失败",
                                      'url': '/profile'
                                  })

############################################################
## admin view
@csrf_exempt
def audit_page(request):
    if SESSION_STATUS not in request.session or request.session[SESSION_STATUS] is not True:
        return HttpResponseRedirect('/index')

    user_id = request.session[SESSION_USER_ID]
    users = User.objects.filter(id=user_id)
    if len(users) != 1:
        return HttpResponseRedirect('/index')
    user = users[0]

    if user.is_admin is not True:
        return HttpResponseRedirect('/index')

    all_run_logs = RunLog.objects.filter(status=RunLog.PENDING)
    return render_to_response('audit.html',
                              {'all_run_log': all_run_logs, 'user': user},
                              context_instance=RequestContext(request))

@csrf_exempt
def audit_detail(request):
    response = {}
    try :
        if SESSION_STATUS not in request.session or request.session[SESSION_STATUS] is not True:
            return HttpResponse("not authorized")

        run_log_id = request.POST.get("run_log_id")
        run_logs = RunLog.objects.filter(id=run_log_id)
        if len(run_logs) > 0:
            return HttpResponse(serializers.serialize('json', run_logs))
        else :
            response['result'] = 'fail'
            return HttpResponse(simplejson.dumps(response))
    except Exception as e:
        print ('Exception:', e)
        response['result'] = 'fail'
        return HttpResponse(simplejson(response))

@csrf_exempt
def audit_accept(request):
    response = {}
    try :
        if SESSION_STATUS not in request.session or request.session[SESSION_STATUS] is not True:
            return HttpResponse("not authorized")

        run_log_id = request.POST.get("run_log_id")
        run_logs = RunLog.objects.filter(id=run_log_id, status=RunLog.PENDING)
        if len(run_logs) > 0:
            run_log = run_logs[0]
            run_log.status = RunLog.ACCEPT
            run_log.save()

            # update user run_length 
            user = run_log.user
            user.run_length += float(run_log.distance)
            user.save()

            # push a notification
            notification = Notification(run_log = run_log)
            notification.save()

            response['result'] = 'success'
            return HttpResponse(simplejson.dumps(response))
        else:
            response['result'] = 'fail'
            return HttpResponse(simplejson.dumps(response))
    except Exception as e:
        print ("Exception:", e)
        response['result'] = 'fail'
        return HttpResponse(simplejson.dumps(response))

@csrf_exempt
def audit_reject(request):
    response = {}
    try :
        run_log_id = request.POST.get("run_log_id")
        run_logs = RunLog.objects.filter(id=run_log_id, status=RunLog.PENDING)
        if len(run_logs) > 0:
            run_log = run_logs[0]
            run_log.status = RunLog.REJECT
            run_log.save()
            notification = Notification(run_log = run_log)
            notification.save()

            response['result'] = 'success'
            return HttpResponse(simplejson.dumps(response))
        else:
            response['result'] = 'fail'
            return HttpResponse(simplejson.dumps(response))
    except Exception as e:
        print ("Exception:", e)
        response['result'] = 'fail'
        return HttpResponse(simplejson.dumps(response))

############################################################
## profile view
@csrf_exempt
def profile_page(request):
    try:
        if SESSION_STATUS not in request.session or request.session[SESSION_STATUS] is not True:
            return HttpResponseRedirect('/index')

        # get current user
        user_id = request.session[SESSION_USER_ID]
        users = User.objects.filter(id=user_id)
        if len(users) != 1:
            return HttpResponseRedirect('/index')
        user = users[0]

        # get user run_length rank board
        rank_list = User.objects.filter(is_admin=False).order_by('-run_length')

        # get notification list
        notifications = Notification.objects.filter(has_seen=False)
        notification_list = [ i for i in notifications if i.run_log.user.id == user.id]

        return render_to_response('profile.html',
                                  {
                                      'user':user,
                                      'rank_list':rank_list,
                                      'notification_list': notification_list,
                                  })
    except Exception as e:
        print ('ProfilePage Exception:', e)
        return HttpResponseRedirect('/index')


@csrf_exempt
def profile_detail_page(request):
    try:
        if SESSION_STATUS not in request.session or request.session[SESSION_STATUS] is not True:
            return HttpResponseRedirect('/index')

        # get current user
        user_id = request.session[SESSION_USER_ID]
        users = User.objects.filter(id=user_id)
        if len(users) != 1:
            return HttpResponseRedirect('/index')
        user = users[0]

        # get user run_length rank board
        rank_list = User.objects.filter(is_admin=False).order_by('-run_length')

        # get notification list
        notifications = Notification.objects.filter(has_seen=False)
        notification_list = [ i for i in notifications if i.run_log.user.id == user.id]

        current_user = User.objects.get(id = request.GET.get('user_id'))

        return render_to_response('profile_detail.html',
                                  {
                                      'user':user,
                                      'user_id':request.GET.get('user_id'),
                                      'user_name':current_user.name,
                                      'rank_list':rank_list,
                                      'notification_list': notification_list,
                                  })
    except Exception as e:
        print ('ProfilePage Exception:', e)
        return HttpResponseRedirect('/index')

@csrf_exempt
def more_run_log(request):
    '''
    POST params:
    - current_user: 0 for all, 1 for current user, 2 for other user
    - start_index: return 30 results from index `start_index
    '''
    response = {}
    try:
        if SESSION_STATUS not in request.session or request.session[SESSION_STATUS] is not True:
            response['result'] = "not authorized"
            return HttpResponse(simplejson.dumps(response))

        start_index = int(request.POST.get('start_index'))
        current_user = request.POST.get('current_user')

        

        # get data
        data = []
        if current_user == '0':
            data = RunLog.objects.filter(status=RunLog.ACCEPT).order_by('-run_date')[start_index:start_index+ITEM_COUNT]
        elif current_user == '1':
            # get current user first
            user_id = request.session[SESSION_USER_ID]
            users = User.objects.filter(id=user_id)
            if len(users) != 1:
                response['result'] = "please relogin"
                return HttpResponse(simplejson.dumps(response))
                
            data = RunLog.objects.filter(user=users[0], status=RunLog.ACCEPT).order_by('-run_date')[start_index:start_index+ITEM_COUNT]
        else :
            user_id = request.POST.get('user_id')
            users = User.objects.filter(id=user_id)
            if len(users) != 1:
                response['result'] = "please relogin"
                return HttpResponse(simplejson.dumps(response))
                
            data = RunLog.objects.filter(user=users[0], status=RunLog.ACCEPT).order_by('-run_date')[start_index:start_index+ITEM_COUNT]
                

        # format data
        rst = []
        for item in data:
            tmp = {}
            tmp['runlog_id'] = item.id
            tmp['username'] = item.user.name
            tmp['userid'] = item.user.id
            tmp['date'] = datetime.strftime(item.run_date, '%Y/%m/%d')
            tmp['distance'] = item.distance
            tmp['sport'] = item.sport
            rst.append(tmp)
        return HttpResponse(simplejson.dumps(rst))
    except Exception as e:
        print ('MoreRunLog Exception:', e)
        response['result'] = "please try again"
        return HttpResponse(simplejson.dumps(response))


@csrf_exempt
def mark_seen(request):
    response = {}
    try:
        if SESSION_STATUS not in request.session or request.session[SESSION_STATUS] is not True:
            response['result'] = 'not authorized'
            return HttpResponse(simplejson.dumps(response))

        # get current user and mark all the unseen notifications
        # to seen
        user_id = request.session[SESSION_USER_ID]
        users = User.objects.filter(id=user_id)
        if len(users) != 1:
            response['result'] = 'need to relogin'
            return HttpResponse(simplejson.dumps(response))
        user = users[0]
        notifications = Notification.objects.filter(has_seen=False)
        unseens = [ i for i in notifications if i.run_log.user == user ]
        for item in unseens:
            item.has_seen = True
            item.save()
        response['result'] = 'success'
        return HttpResponse(simplejson.dumps(response))
    except Exception as e:
        print ("Exception:", e)
        response['result'] = 'fail'
        return HttpResponse(simplejson.dumps(response))

@csrf_exempt
def runlog_detail_page(request):
    try:
        if SESSION_STATUS not in request.session or request.session[SESSION_STATUS] is not True:
            return HttpResponseRedirect('/index')

        # get current user
        user_id = request.session[SESSION_USER_ID]
        users = User.objects.filter(id=user_id)
        if len(users) != 1:
            return HttpResponseRedirect('/index')
        user = users[0]

        # get user run_length rank board
        rank_list = User.objects.filter(is_admin=False).order_by('-run_length')

        # get notification list
        notifications = Notification.objects.filter(has_seen=False)
        notification_list = [ i for i in notifications if i.run_log.user.id == user.id]

        # get the run_log
        runlog = RunLog.objects.get(id=request.GET.get("runlog_id"))
        if runlog is None:
            return render_to_response("message.html",
                                  {
                                      'user': user,
                                      'message': "上传成功",
                                      'url': '/profile'
                                  })

        return render_to_response('runlog_detail.html',
                                  {
                                      'user':user,
                                      'rank_list':rank_list,
                                      'notification_list': notification_list,
                                      'runlog': runlog,
                                  })
    except Exception as e:
        print ('ProfilePage Exception:', e)
        return HttpResponseRedirect('/index')

############################################################
## change password
@csrf_exempt
def change_password(request):
    response = {}
    try:
        if SESSION_STATUS not in request.session or request.session[SESSION_STATUS] is not True:
            response['result'] = '请重新登录'
            return HttpResponse(simplejson.dumps(response))

        username = request.POST.get("username")
        new_password = __make_password(request.POST.get("new_password"))
        old_password = __make_password(request.POST.get("old_password"))
        
        user_id = request.session[SESSION_USER_ID]
        users = User.objects.filter(id=user_id)
        if len(users) != 1:
            response['result'] = '请重新登录'
            return HttpResponse(simplejson.dumps(response))
        user = users[0]

        if old_password != user.password:
            response['result'] = '旧密码错误'
            return HttpResponse(simplejson.dumps(response))
        
        if username != "":
            user.name = username
        user.password = new_password
        user.save()
        response['result'] = '修改成功'
        return HttpResponse(simplejson.dumps(response))
    except Exception as e:
        print ('Exception:', e)
        reseponse['result'] = '服务器错误，请重试'
        return HttpResponse(simplejson.dumps(response))

############################################################
## private functions
def __make_password(password):
    hash_str = password + HASH_STRING
    return hashlib.md5(hash_str.encode('utf-8')).hexdigest()
