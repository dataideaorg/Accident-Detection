from datetime import datetime
from .models import Prediction
from geopy.geocoders import Nominatim
from django.shortcuts import render, redirect
from .tools import request_prediction, get_prediction
from django.contrib.auth.decorators import login_required

# Create your views here.
model_api = ""

def get_user_location(request):
    ip = request.META.get('REMOTE_ADDR')
    geolocator = Nominatim(user_agent='myapp')
    location = geolocator.geocode(ip)
    if location:
        return location.address
    else:
        return None

# @login_required(login_url='/accounts/login')
def process_video(request):
    if request.method == 'POST':
      video_url = request.POST['video_url']
      # prediction = get_prediction(video_url, model_api)
      prediction = {
        'prediction': 1,
        'confidence': 0.78
      }

      date_time = datetime.now()

      try:
        location = get_user_location(request)
      except Exception as e:
        print(colored(f'Failed getting user location {str(e)}'))
        print(colored(f'Setting to default location'))
        location = 'Makerere,Kikoni, Kampala (U)'
        
      prediction_object = Prediction(
        prediction = prediction['prediction'],
        confidence = prediction['confidence'],
        location = location,
        date_time = date_time
      )

      prediction_object.save()
      
      return redirect('/detector/dashbord')

    if request.method == 'GET':
      context = {}
      return render(request, 'detector/select_video.html', context)

def dashbord(request):
    latest_predictions = Prediction.objects.all()
    context = {'latest_predictions': latest_predictions}
    return render(request, 'detector/dashbord.html', context)