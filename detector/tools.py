import cv2 
import pathlib
import requests
from shafaratoolkit.props import colored

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

def request_prediction(image, url):
    if not image and url:
        raise Exception('Both image and api url must be provided')
    headers = {}
    payload = {}

    files = [('image', open(f'{image}', 'rb'))]

    try:
        response = requests.post(url, headers, files, payload)
        return response.json()
    except Exception as e:
        print(colored(255, 0, 0, text=f'Error: {e}'))
        return None
    
def get_prediction(video, url):
    if not video and url:
        raise Exception('Both video and api url must be provided')
    
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    frequency = 100 
    for i in range(frame_count):
        ret, frame = video.read()

        if not ret:
            break

        if i % frequency == 0:
            print(colored(0, 255, 0, text=f'Processing frame {i} of {frame_count}'))
            response = request_prediction(frame, url)
            prediction = response['prediction']
            confidence = response['confidence']
            cv2.imwrite(
                BASE_DIR / f'media/images/predictions/frame_{i}_Pred_{prediction}_Conf_{confidence}.jpg', 
                frame
                )
            
            yield prediction   
