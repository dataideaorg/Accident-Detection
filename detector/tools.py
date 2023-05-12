import os
import pathlib
import requests
from geopy.geocoders import Nominatim
from shafaratoolkit.props import colored

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

def is_writable_file(filename):
    return os.access(filename, os.W_OK)

def get_user_location(request):
    ip = request.META.get('REMOTE_ADDR')
    geolocator = Nominatim(user_agent='myapp')
    location = geolocator.geocode(ip)
    if location:
        return location.address
    else:
        return None

def request_prediction(image, url):
    headers = {}
    files = {'image': (open(image, 'rb'))}

    try:
        print(colored(0, 0, 255, "Sending request to API ..."))
        response = requests.post(url, headers=headers, files=files)
        print(response.status_code)
        return response.json()
    except Exception as e:
        print(colored(255, 0, 0, text=f'Error: {e}'))
        return None
    

