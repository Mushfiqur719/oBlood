from .forms import RoomForm
from .models import Room,Topic
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
        
        user = authenticate(request, username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect ('home')
        else:
            messages.error(request,'Username of Password does not match')

    context = {}
    return render(request, 'base/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics':topics, 'room_count': room_count}
    
    return render(request, 'base/home.html',context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html',context)

@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='/login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed to edit others post")

    if request.method == 'POST':
        form = RoomForm(request.POST,instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html',context)

def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed to delete someone elses post")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj' : room}
    return render(request, 'base/delete.html',context)
