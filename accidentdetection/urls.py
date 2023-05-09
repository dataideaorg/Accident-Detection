from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
from .views import home, about, contact

app_name = "accidentdetection"

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path('detector/', include('detector.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
