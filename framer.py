import cv2
import requests
from shafaratoolkit.props import colored

def request(image_path, url):

    headers = {}
    payload = {}

    files = [('image', open(f"{image_path}", 'rb'))]

    try:
        response = requests.post(url, headers=headers, files=files)
        return response
    except Exception as e:
        print(colored(255, 0, 0, f'An error was encountered {str(e)}'))
        return 999


def get_frames_and_prediction(video, url):
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    frequency = 100  # Extract a frame every 30 frames
    for i in range(frame_count):
        ret, frame = video.read()

        if not ret:
            break

        if i % frequency == 0:
            filename = f"frames/frame_{i}.jpg"
            cv2.imwrite(filename, frame)

            response = request(filename, url)
            
            if response == 999:
                break
            response = response.json()
            # print(colored(0, 0, 255, f"{response}"))
            prediction = response['prediction']
            confidence = response['confidence']
            cv2.imwrite(filename= f'predictions/frame_{i}-Pred{prediction}-Conf({confidence}).jpg', img = frame)

    video.release()
    print(colored(0, 255, 0, "Complete"))



api_endpoint = "http://127.0.0.1:8000/classifier/"
video_footage = cv2.VideoCapture("videos/compilation.mp4")

get_frames_and_prediction(video_footage, api_endpoint)