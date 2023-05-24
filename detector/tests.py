from django.test import TestCase
from tools import send_message

# Create your tests here.
api = 'https://geniussmsgroup.com/api/json/messages1/jsonMessagesService'

response = {'confidence': 0.88}
location = 'test location'
date, time = 'd8', 't8st'

send_message(messaging_api=api, response=response,
             location=location, date=date, time=time)
