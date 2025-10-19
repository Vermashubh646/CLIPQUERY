from django.urls import path
from a_home.views import *

urlpatterns = [
    path('', home_view, name="home"),  
    path('yourvideos/', userhome_view , name="myhome"),
    path('delete/<int:pk>', delete , name='delete'),
    path('update/<int:pk>', update , name='update'),
    
]
