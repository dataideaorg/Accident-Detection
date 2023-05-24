import os
import cv2
import csv
import pathlib
from datetime import datetime
from .models import Prediction
from django.http import HttpResponse
from shafaratoolkit.props import colored
import accidentdetection.settings as settings
from django.shortcuts import render, redirect
from accounts.models import User, Notification
from django.contrib.auth.decorators import login_required
from .tools import request_prediction, get_user_location, send_message


# Create your views here.
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

model_api = "http://127.0.0.1:8081/classifier/"
messaging_api = 'https://geniussmsgroup.com/api/json/messages1/jsonMessagesService'
# video_name = 'compilation.mp4'
# video_url = os.path.join(settings.STATIC_ROOT, 'videos', video_name)


def save_prediction(response, location, date_time, frame_count):
    prediction_object = Prediction(
        prediction=response['prediction'],
        confidence=str(round(response['confidence'], 2)),
        location=location,
        time=date_time.time().strftime("%H:%M:%S"),
        date=date_time.date().strftime("%Y-%m-%d"),
        image=f'frame_{frame_count}.jpg'
    )

    prediction_object.save()

    return prediction_object

# @login_required(login_url='/accounts/login')


def process_video(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        print(colored(0, 0, 256, f'{video_url  }'))
        video_path = os.path.join(settings.STATIC_ROOT, 'videos', video_url)
        output_dir = os.path.join(settings.MEDIA_ROOT, 'images', 'frames')
        prediction_dir = os.path.join(
            settings.MEDIA_ROOT, 'images', 'predictions')

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if not os.path.exists(prediction_dir):
            os.makedirs(prediction_dir)

        try:
            location = get_user_location(request)
        except Exception as e:
            print(colored(255, 0, 0, f'Failed getting user location {str(e)}'))
            print(colored(0, 0, 255, f'Setting to default location'))
            location = 'Makerere,Kikoni, Kampala (U)'

        date_time = datetime.now()

        video = cv2.VideoCapture(video_path)

        frame_count = 0
        frame_frequency = 1000
        while True:
            success, frame = video.read()

            if not success:
                break

            if frame_count % frame_frequency == 0:
                output_path = os.path.join(
                    output_dir, f'frame_{frame_count}.jpg')
                cv2.imwrite(output_path, frame)

                response = request_prediction(output_path, model_api)

                if response == None:
                    context = {
                        'error_message': 'Can not get response from the model at this time',
                        'status': 500
                    }

                    return render(request, 'detector/error_page.html', context=context)

                if response['prediction'] == 1:
                    send_message(
                        messaging_api=messaging_api,
                        confidence=response['confidence'],
                        location=location,
                        date_time=date_time
                    )

                save_prediction(response, location, date_time, frame_count)

            frame_count += 1

        video.release()

        return redirect('/detector/dashbord')

    if request.method == 'GET':
        context = {}
        return render(request, 'detector/select_video.html', context=context)

# @login_required(login_url='/accounts/login')


def dashbord(request):
    latest_predictions = Prediction.objects.all()
    num_images_processed = len(latest_predictions)
    num_accidents_detected = len(
        [p for p in latest_predictions if p.prediction == 1])

    try:
        prediction_confidence = round(
            sum([float(p.confidence) for p in latest_predictions])/len(latest_predictions), 2)
    except Exception as e:
        prediction_confidence = 0

    context = {
        'latest_predictions': latest_predictions,
        'num_images_processed': num_images_processed,
        'num_accidents_detected': num_accidents_detected,
        'prediction_confidence': prediction_confidence,
    }
    return render(request, 'detector/dashbord.html', context)

# @login_required(login_url='/accounts/login')


def view_single(request, id):
    prediction = Prediction.objects.get(id=id)

    context = {
        'prediction': prediction,
    }
    return render(request, 'detector/view_single.html', context=context)


def view_images(request):
    latest_predictions = Prediction.objects.all()
    context = {
        'latest_predictions': latest_predictions,
    }
    return render(request, 'detector/view_images.html', context=context)


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="predictions.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Prediction', 'Confidence',
                    'Location', 'Time', 'Date', 'Image'])

    for prediction in Prediction.objects.all().values_list(
            'id', 'prediction', 'confidence', 'location', 'time', 'date', 'image'):
        writer.writerow(prediction)

    return response
