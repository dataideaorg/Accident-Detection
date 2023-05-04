from django.contrib import admin
from django.urls import path
from django.urls import include
from .views import home, about, contact

app_name = "accidentdetection"

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path('detector/', include('detector.urls')),
]
