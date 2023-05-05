from django.urls import path
from .views import dashbord, process_video

app_name = 'detector'
urlpatterns = [
    path('process_video', process_video, name='process_video'),
    path('dashbord', dashbord, name='dashbord')
]