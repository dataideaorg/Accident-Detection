import os
import cv2
import pathlib
import datetime
import requests
from .models import Prediction
from geopy.geocoders import Nominatim
from shafaratoolkit.props import colored
import accidentdetection.settings as settings

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

def get_user_location(request):
    ip = request.META.get('REMOTE_ADDR')
    geolocator = Nominatim(user_agent='myapp')
    location = geolocator.geocode(ip)
    if location:
        return location.address
    else:
        return None

def request_prediction(image, url):
    # if not image and url:
    #     raise Exception('Both image and api url must be provided')
    headers = {}
    payload = {}

    files = [('image', open(f'{image}', 'rb'))]

    try:
        response = requests.post(url, headers, files, payload)
        return response.json()
    except Exception as e:
        print(colored(255, 0, 0, text=f'Error: {e}'))
        return None
    
def get_prediction(request, video, url):
    prediction_objects = []
    if not video and url:
        raise Exception('Both video and api url must be provided')
    
    try:
        location = get_user_location(request)
    except Exception as e:
        print(colored(255, 0, 0, f'Failed getting user location {str(e)}'))
        print(colored(0, 0, 255, f'Setting to default location'))
        location = 'Makerere,Kikoni, Kampala (U)'

    video_footage = cv2.VideoCapture(video)
    print(colored(0, 255, 0, text=f'Video Footage: {video_footage}'))
    frame_count = int(video_footage.get(cv2.CAP_PROP_FRAME_COUNT))

    frequency = 100 
    for i in range(frame_count):
        ret, frame = video_footage.read()
        print(colored(0, 255, 0, text=f'Ret: {str(ret)}'))

        if not ret:
            break

        if i % frequency == 0:
            print(colored(0, 255, 0, text=f'Processing frame {i} of {frame_count}'))
            filename = os.path.join(settings.MEDIA_ROOT, 'frames', f'frame_{i}.jpg')
            cv2.imwrite(filename, frame)
            print(colored(0, 255, 0, text=f'Saved frame {i} to {filename}'))

            response = request_prediction(filename, url)
            date_time = datetime.now()
            prediction_object = Prediction(
                prediction = response['prediction'],
                confidence = response['confidence'],
                location = location,
                time = date_time.time().strftime("%H:%M:%S"),
                date = date_time.date().strftime("%Y-%m-%d"),
                )

            cv2.imwrite(
                # BASE_DIR / f'media/images/predictions/frame_{i}_Pred_{prediction}_Conf_{confidence}.jpg', 
                os.path.join(settings.MEDIA_ROOT, 'frames', f'iframe_{i}_Pred_{prediction}_Conf_{confidence}.jpg'),
                frame
                )
            
            prediction_object.save()
            prediction_objects.append(prediction_object)
    return prediction_objects