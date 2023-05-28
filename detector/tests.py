from django.test import TestCase
from tools import send_message, get_user_location

# Create your tests here.
def send_message_test():
    api = 'https://geniussmsgroup.com/api/json/messages1/jsonMessagesService'

    response = {'confidence': 0.88}
    location = 'test location'
    date_time = 'd8_t8st'
    confidence = 0.88

    send_message(messaging_api=api, confidence=confidence, numbers=['256771754118'], location=location, date_time=date_time)

