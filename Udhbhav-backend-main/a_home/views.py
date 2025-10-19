from django.shortcuts import render,redirect
from videos.models import *
from a_users.models import Profile

def home_view(request):
    allvideos = Video.objects.all()
    profile = Profile.objects.all()
    return render(request, 'home.html', {'videos':allvideos ,'profiles' : profile})


def userhome_view(request):
    allvideos = Video.objects.filter(owner=request.user)
    return render(request, 'userhome.html' , {'videos':allvideos, 'type' : 'user'} )


def delete(request,pk):
    video= Video.objects.get(id = pk)
    if(request.user == video.owner):
        video.delete()
    return redirect('home')


def update(request,pk):
    return redirect('home')