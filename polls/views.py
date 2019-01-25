from django.shortcuts import render, redirect
from django.http import HttpResponse
import uuid
from .models import Project, Users, LstUsd
from passlib.hash import pbkdf2_sha256
from datetime import datetime
import json
# Create your views here.

#Render the frontpage
def indx(request):
    if 'usrnme' in request.session:
        return redirect('/userKey')
    return render(request, 'polls/base.html')

#generates the unique key. A while loop is run to make sure that the unique string is not already in use
def unq(request):
    unq_ky = uuid.uuid4().hex[:15].upper()
    chck = True

    while chck:
        sc=Project.objects.filter(unqKey=unq_ky)
        if sc.count() > 0:
            unq_ky = uuid.uuid4().hex[:15].upper()
        else:
            msg = Project()
            msg.unqKey = unq_ky
            msg.actve = "0"
            msg.save()
            chck = False

    if 'usrnme' in request.session:
        PstUsrnme = request.session['usrnme']
        Unq_key = unq_ky

        try:
            t = Users.objects.get(usrnme=PstUsrnme)
            t.unqKey = Unq_key
            t.save()
        except Exception as e:
            return HttpResponse(e)
    return redirect("/workon?scrtKy="+unq_ky)

#render the control panel where can create, delete and edit the features
def wrkon(request):
    my_param = request.GET.get('scrtKy')
    if my_param is None:
        return redirect("/")
    else:
        sc=Project.objects.filter(unqKey=my_param)
        if sc.count() > 0:
            lstUsd = LstUsd.objects.filter(unqKey=my_param)
            if lstUsd.count() > 0:
                t = LstUsd.objects.get(unqKey=my_param)
                t.dte = datetime.now()
                t.save()
            else:
                msg = LstUsd()
                msg.unqKey = my_param
                msg.dte = datetime.now()
                msg.save()
            jsnRsp = sc.values()
            jsnRsp = list(jsnRsp)
            #jsnRsp = json.dumps(list(jsnRsp), cls=DjangoJSONEncoder)
            return render(request, 'polls/wrkon.html',{'content':[jsnRsp]})
        else:
            return HttpResponse("<script>alert('The Secret Key does not exist in our system');window.location.href = '/';</script>")

#add feature
def addFeat(request):
    unq_ky = request.GET.get('scrtKy')
    if unq_ky is None:
        return redirect("/")
    else:
        sc=Project.objects.filter(unqKey=unq_ky)
        if sc.count() > 0:
            msg = Project()
            msg.unqKey = unq_ky
            msg.actve = "0"
            msg.save()
            return HttpResponse("success")
    return HttpResponse("fail")

#delete feature
def dltFeat(request):
    id = request.GET.get('id')
    try:
        Project.objects.filter(id=id).delete()
    except Exception as e:
            return HttpResponse(e)
    return HttpResponse("success")

#update feature
def updFeat(request):
    id = request.GET.get('id')
    nme = request.GET.get('nme')
    cde = request.GET.get('cde')
    act = request.GET.get('act')
    try:
        t = Project.objects.get(id=id)
        t.nme = nme
        t.cde = cde
        t.actve = act
        t.save()
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse("success")

#User creation / log in
def login(request):
    if request.POST.get('usr') and request.POST.get('pswrd'):
        PstUsrnme = request.POST.get('usr').lower().replace(" ", "")
        ChckUsr = Users.objects.filter(usrnme=PstUsrnme)

        if ChckUsr:
            pss = Users.objects.get(usrnme=PstUsrnme).psswrd

            if pbkdf2_sha256.verify(request.POST.get('pswrd'),pss):
                request.session['usrnme'] = PstUsrnme
                return redirect('/userKey')
            else:
                return HttpResponse("<script>alert('Wrong username or password');window.location.href = '/';</script>")

        else:
            post=Users()
            post.usrnme = request.POST.get('usr')
            post.psswrd = pbkdf2_sha256.encrypt(request.POST.get('pswrd'), rounds=12000,salt_size=32)
            post.save()
            request.session['usrnme'] = PstUsrnme
            return HttpResponse("<script>alert('User created');window.location.href = '/userKey';</script>")
    else:
        return redirect("/")

#Associate user profil with unique key
def usrKey(request):
    PstUsrnme = request.session['usrnme']
    Unq_key = Users.objects.get(usrnme=PstUsrnme).unqKey

    if Unq_key != "":
        return redirect("/workon?scrtKy="+Unq_key)

    return render(request, 'polls/userunqkey.html')

#Associate user profil with unique key
def addExst(request):
    PstUsrnme = request.session['usrnme']
    Unq_key = request.GET.get('scrtKy')
    sc=Project.objects.filter(unqKey=Unq_key)
    if sc.count() > 0:
        try:
            t = Users.objects.get(usrnme=PstUsrnme)
            t.unqKey = Unq_key
            t.save()
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("<script>alert('The Secret Key does not exist in our system');window.location.href = '/userKey';</script>")

    return redirect("/workon?scrtKy="+Unq_key)

#sign out
def signout(request):
    if 'usrnme' in request.session:
        del request.session['usrnme']
        request.session.modified = True
    return redirect('/')

#The API backend
def api(request):
    my_param = request.GET.get('scrtKy')
    if my_param is None:
        return redirect("/")
    else:
        sc=Project.objects.filter(unqKey=my_param)
        if sc.count() > 0:
            lstUsd = LstUsd.objects.filter(unqKey=my_param)
            if lstUsd.count() > 0:
                t = LstUsd.objects.get(unqKey=my_param)
                t.dte = datetime.now()
                t.save()
            else:
                msg = LstUsd()
                msg.unqKey = my_param
                msg.dte = datetime.now()
                msg.save()
            jsnRsp = sc.values('nme','cde','actve')
            jsnRsp = list(jsnRsp)
            l = []
            for lst in jsnRsp:
                if lst['actve'] == "0":
                    l.append([lst['nme'],False])
                else:
                    l.append([lst['nme'],lst['cde']])

            #jsnRsp = json.dumps(list(jsnRsp), cls=DjangoJSONEncoder)
            return HttpResponse(json.dumps(l))

