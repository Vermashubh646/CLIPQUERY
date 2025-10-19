

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import VideoForm
from .models import Video
from .utils import *
from Django_integrate import initialise

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            
            video = form.save(commit=False)
            video.owner = request.user  # 👈 assign the logged-in user
            video.save()
            initialise(video.video_file)
            return redirect('home')
    else:
        form = VideoForm()
    return render(request, 'videos/upload.html', {'form': form})


def video_detail(request,pk):
    video = Video.objects.get(id=pk)
    videos = Video.objects.all()
    return render(request , 'videos/videodetail.html' , {'video':video , 'videos':videos})