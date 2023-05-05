from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .tools import request_prediction, get_prediction

# Create your views here.
# @login_required(login_url='/accounts/login')
def process_video(request):
    if request.method == 'POST':
      video_url = request.POST['video_url']
      return redirect('/detector/dashbord')

    if request.method == 'GET':
      context = {}
      return render(request, 'detector/select_video.html', context)

def dashbord(request):
    context = {}
    return render(request, 'detector/dashbord.html', context)