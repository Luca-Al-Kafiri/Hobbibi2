from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from ipstack import GeoLookup
import os
from django.db.models import Count
from .models import User, Hobbi, Message, Hobbies

# Create your views here.


def index(request):
    u = User.objects.get(id=request.user.id)
    us = Message.objects.filter(recipient=u, read=False).values("sender").distinct()
    new_msg  = User.objects.filter(id__in=us)
    count = Message.objects.filter(recipient=u, read=False).count()
    c = Message.objects.filter(sender=u).values("recipient").distinct()
    contacts = User.objects.filter(id__in=c)
    return render(request, "hobbibi/index.html", {"count": count, "new_msg": new_msg, "contacts": contacts})


@login_required
@csrf_exempt
def search(request):
    h = Hobbies.objects.filter(user=request.user.id)
    d=[]
    for hobbi in h:
        d.append(hobbi)
    hobbies = Hobbi.objects.filter(name__in=d)
    user = User.objects.get(username=request.user.username)
    users = User.objects.filter(city=user.city, country=user.country)
    matchs = Hobbies.objects.select_related('user').filter(hobbi__in=hobbies, user__in=users).exclude(user=request.user.id).order_by("user")
    if request.method == "POST":
        data = json.loads(request.body)
        h = Hobbi.objects.get(name=data["hobbi"])
        matchs = Hobbies.objects.select_related('user').filter(hobbi=h.id, user__in=users).exclude(user=request.user.id).order_by("user")
        return JsonResponse([match.serialize() for match in matchs], safe=False)
    else:
        u = User.objects.get(id=request.user.id)
        us = Message.objects.filter(recipient=u, read=False).values("sender").distinct()
        new_msg  = User.objects.filter(id__in=us)
        count = Message.objects.filter(recipient=u, read=False).count()
        c = Message.objects.filter(sender=u).values("recipient").distinct()
        contacts = User.objects.filter(id__in=c)
        return render(request, 'hobbibi/search.html', {"matchs": matchs, "hobbies": hobbies, "count": count, "new_msg": new_msg, "contacts": contacts })


def profile(request, user):
    h = Hobbi.objects.all()
    owner = User.objects.get(username=user)
    hobbies = Hobbies.objects.select_related('user').filter(user=owner.id)
    sender = User.objects.get(id=request.user.id)
    messages = Message.objects.filter(sender__in=(sender,owner), recipient__in=(owner, sender)).order_by("timestamp")
    msg = Message.objects.filter(sender=owner, recipient=sender, read=False)
    for m in msg:
        m.read = True
        m.save()
    u = User.objects.get(id=request.user.id)
    us = Message.objects.filter(recipient=u, read=False).values("sender").distinct()
    new_msg = User.objects.filter(id__in=us)
    count = Message.objects.filter(recipient=sender, read=False).count()
    if request.method == "POST":
        image = request.FILES["image"]
        owner.image = image
        owner.save()
        return redirect('profile', user=user)
    c = Message.objects.filter(sender=u).values("recipient").distinct()
    contacts = User.objects.filter(id__in=c)
    return render(request, "hobbibi/profile.html", {"hobbies": hobbies, 'owner': owner, "h":h,"messages": messages, "count": count, "new_msg": new_msg, "contacts": contacts })


@login_required
@csrf_exempt
def add(request):
    if request.method == "POST":
        data = json.loads(request.body)
        hobbi = Hobbi.objects.get(id=data['hobbi'])
        user = User.objects.get(pk=request.user.id)
        hobbies = Hobbies.objects.filter(user=user)
        d = []
        for i in hobbies:
            d.append(i.hobbi)
        if hobbi in d:
            return JsonResponse({"error": "Hobbi already exist"}, status=400)
        else:
            add = Hobbies.objects.create(user=user, hobbi=hobbi)
            add.save()
            id = add.id
            h = Hobbi.objects.get(id=data['hobbi'])
            hobbi = h.name
            return JsonResponse({"hobbi": hobbi , "user": request.user.username, "id": id, "status": 201})

@login_required
@csrf_exempt
def delete(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        hobbies = Hobbies.objects.get(id = data["hobbi"])
        hobbies.delete()
        return JsonResponse({"status": 201})

@login_required
@csrf_exempt
def delete_msg(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        msg = Message.objects.get(id = data["msg"])
        msg.message = "This message was deleted"
        msg.save()
        return JsonResponse({"status": 201})


@login_required
@csrf_exempt
def message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        sender = User.objects.get(id=request.user.id)
        recipient = User.objects.get(username=data["user"])
        message = data["msg"]
        msg = Message.objects.create(sender=sender, recipient=recipient, message=message)
        msg.save()
        return JsonResponse([msg.serialize()], safe=False)


def register(request):
    if request.method == "POST":
        hobbies = Hobbi.objects.all()
        username = request.POST["username"]
        password = request.POST["password"]
        image = request.FILES['profile']
        email = "luca@luca.com"
        h = request.POST["hobby"]
        year = int(request.POST["age"])
        ip = request.POST["ip"]
        geo_lookup = GeoLookup(os.getenv("API_KEY"))
        location = geo_lookup.get_location(ip)
        country = location["country_name"]
        city = location["city"]
        today = datetime.now()
        age = today.year - year
        confirm = request.POST["confirm"]
        if password != confirm:
            return render(request, "hobbibi/register.html", {"message":"Password does not match", "hobbies": hobbies})
        try:
            user = User.objects.create_user(username, email, password)
            user.age = age
            user.city= city
            user.country = country
            user.image = image
            user.save()
            ho = Hobbi.objects.get(id=h)
            hobbi = Hobbies.objects.create(user=user, hobbi=ho)
            hobbi.save()
        except IntegrityError:
            return render(request, "hobbibi/register.html", {"message": "Username already taken", "hobbies": hobbies})
        login(request, user)
        return HttpResponseRedirect(reverse('search'))
    else:
        hobbies = Hobbi.objects.all()
        return render(request, "hobbibi/register.html", {"hobbies": hobbies})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        ip = request.POST["ip"]
        geo_lookup = GeoLookup(os.getenv("API_KEY"))
        location = geo_lookup.get_location(ip)
        country = location["country_name"]
        city = location["city"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user = User.objects.get(username=username)
            user.country = country
            user.city = city
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("search"))
        else:
            return render(request, "hobbibi/login.html", {"message": "Invalid username and/or password."})
    else:
        return render(request, "hobbibi/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))