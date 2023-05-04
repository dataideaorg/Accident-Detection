from django.urls import path
from .views import dashbord, select_video

app_name = 'detector'
urlpatterns = [
    path('select_video', select_video, name='select_video'),
    path('dashbord', dashbord, name='dashbord')
]