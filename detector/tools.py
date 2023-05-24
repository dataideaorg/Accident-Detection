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


def send_message(messaging_api, confidence, location, date_time):
    confidence = str(round(confidence, 2))
    location = location
    time = date_time.time().strftime("%H:%M:%S")
    date = date_time.date().strftime("%Y-%m-%d")

    headers = {}
    payload = {
        'user': {
            'username': 'jumashafara',
            'password': 'Chappie256'
        },
        'messages': [
            {
                'numbers': ['256709603955', '256701520768'],
                'senderid': 'AccidentAi',
                'messageBody': f'An accident has been detected in {location} on {date} at {time} with a confidence of {confidence}'
            }
        ]
    }

    try:
        response = requests.post(url=messaging_api, json=payload)
        response = response.json()
        print(
            colored(0, 255, 0, text=f'Messages sent successfully \n {response}'))
    except Exception as e:
        print(
            colored(255, 0, 0, text=f'An error occurred while sending messages \n {e}'))

    return
