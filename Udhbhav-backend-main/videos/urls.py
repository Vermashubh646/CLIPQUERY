from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_video, name='upload_video'),
    path('videodetail/<int:pk>/', views.video_detail , name = 'viddetail'),
]