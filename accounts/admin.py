from django.contrib import admin
from .models import User

# Register your models here.
admin.site.register(User)

# modify admin
admin.site.site_header = "AccidentDetectionAi"
admin.site.site_title = "AccidentDetectionAi-Admin"