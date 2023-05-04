from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/accounts/login')
def select_video(request):
    context = {}
    return render(request, 'detector/select_video.html', context)

def dashbord(request):
    context = {}
    return render(request, 'detector/dashbord.html', context)