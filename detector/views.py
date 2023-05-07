import os
import cv2
import pathlib
import accidentdetection.settings as settings
from datetime import datetime
from .models import Prediction
from shafaratoolkit.props import colored
from django.shortcuts import render, redirect
from .tools import request_prediction, get_prediction
from django.contrib.auth.decorators import login_required


# Create your views here.
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

model_api = "http://127.0.0.1:8081/classify/"
video_name = 'compilation.mp4'
video_url = os.path.join(settings.STATIC_ROOT, 'videos', video_name)

# @login_required(login_url='/accounts/login')
def process_video(request):
    if request.method == 'POST':
      # video_url = request.POST['video_url']
      print(colored(0, 0, 255,f"video_url: {video_url}"))
      prediction_objects = get_prediction(request, video_url, model_api)
      print(colored(0, 0, 255,f"first prediction object: {prediction_objects[0]}"))
      return redirect('/detector/dashbord')

    if request.method == 'GET':
      context = {}

      return render(request, 'detector/select_video.html', context)

def dashbord(request):
    latest_predictions = Prediction.objects.all()
    context = {'latest_predictions': latest_predictions}
    return render(request, 'detector/dashbord.html', context)