from django.urls import path
from .views import dashbord, process_video,  view_single, view_images,  export_csv

app_name = 'detector'
urlpatterns = [
    path('process_video', process_video, name='process_video'),
    path('view_images', view_images, name='view_images'),
    path('dashbord', dashbord, name='dashbord'),
    path('export_csv', export_csv,  name='export_csv'),
    path('view_single/<str:id>', view_single, name='view_single'),
]